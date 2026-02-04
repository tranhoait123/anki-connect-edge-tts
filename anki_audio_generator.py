import asyncio
import json
import urllib.request
import os
import hashlib
import edge_tts
import re

class AnkiGenerator:
    def __init__(self, anki_connect_url):
        self.anki_connect_url = anki_connect_url

    def invoke(self, action, **params):
        requestJson = json.dumps(self.request(action, **params)).encode('utf-8')
        response = json.load(urllib.request.urlopen(urllib.request.Request(self.anki_connect_url, requestJson)))
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']

    def request(self, action, **params):
        return {'action': action, 'params': params, 'version': 6}

    async def generate_and_upload_audio(self, note_id, text, voice, audio_field, log_callback=print, is_ssml=False):
        if not text:
            if log_callback: log_callback(f"Skipping note {note_id}: Source field is empty.")
            return

        # Ensure text is clean
        text = text.strip().lstrip('\ufeff')
        
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        filename = f"tts_{text_hash}.mp3"
        output_file = f"/tmp/{filename}"

        try:
            if log_callback: log_callback(f"Generating audio for note {note_id}...")
            
            # If explicit SSML flag is set, or if it looks like SSML, treat as SSML
            # edge_tts.Communicate handles SSML detection automatically, so we just pass the text.
            # The is_ssml flag here primarily indicates that the text is already formatted SSML
            # and doesn't need further wrapping/escaping by this function.
            communicate = edge_tts.Communicate(text, voice)
                
            await communicate.save(output_file)

            with open(output_file, "rb") as file:
                data = file.read()
                import base64
                b64_data = base64.b64encode(data).decode('utf-8')

            self.invoke("storeMediaFile", filename=filename, data=b64_data)
            if log_callback: log_callback(f"Uploaded {filename} to Anki.")

            audio_tag = f"[sound:{filename}]"
            self.invoke("updateNoteFields", note={"id": note_id, "fields": {audio_field: audio_tag}})
            if log_callback: log_callback(f"Updated note {note_id} with audio.")

        except Exception as e:
            if log_callback: log_callback(f"Error processing note {note_id}: {e}")
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

    def clean_text_for_tts(self, text, abbreviations=None):
        import re
        import html
        
        # Remove control characters (e.g. null bytes, etc.) that might break XML
        text = "".join(ch for ch in text if ch.isprintable())

        # Remove script and style tags WITH their content
        text = re.sub(r'<(style|script)[^>]*>.*?</\1>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags (keeping content of other tags like div, span)
        text = re.sub('<[^<]+?>', '', text)
        
        # Decode HTML entities (e.g. &nbsp; -> space, &gt; -> >) so we can clean them
        text = html.unescape(text)

        # Remove citations like [1], [2]
        text = re.sub(r'\[\d+\]', '', text)
        # Remove emojis
        text = re.sub(r'[\U0001F300-\U0001F9FF]|[\U0001F600-\U0001F64F]|[\u2600-\u27BF]', '', text)
        # Remove long separators
        text = re.sub(r'[-_=]{3,}', ' ', text)
        # Remove URLs (http, https, www)
        text = re.sub(r'http[s]?://\S+|www\.\S+', '', text)
        # Remove filenames that might leak (e.g. .jpg, .png) if they aren't in tags
        text = re.sub(r'\S+\.(jpg|png|gif|jpeg|mp3|mp4)\b', '', text, flags=re.IGNORECASE)
        
        # Optimize for Cloze Deletions: {{c1::Answer}} -> Answer
        # Handles {{c1::Answer::Hint}} as well, taking the Answer part.
        text = re.sub(r'\{\{c\d+::(.*?)(?:::[^}]*)?\}\}', r'\1', text)
        
        # Abbreviation Expansion
        if abbreviations:
            # Sort by length descending to replace longer phrases first (though simple dict iter is usually fine for 1-word codes)
            for short, full in abbreviations.items():
                # Word boundary check to avoid replacing inside words (e.g., BN in BNA)
                # Escape the short term just in case
                pattern = r'\b' + re.escape(short) + r'\b'
                text = re.sub(pattern, full, text, flags=re.IGNORECASE)

        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # XML Escape for SSML (Important!)
        text = html.escape(text)
        
        return text

    async def generate_preview(self, text, voice, rate="+0%", is_ssml=False):
        text = text.strip().lstrip('\ufeff')
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        filename = f"preview_{text_hash}.mp3"
        output_file = f"/tmp/{filename}"
        
        # Extract lang from voice (e.g. vi-VN-NamMinhNeural -> vi-VN)
        try:
            lang_code = "-".join(voice.split("-")[:2])
        except:
            lang_code = "en-US"

        if is_ssml or text.startswith("<speak"):
            ssml_text = text
        else:
             ssml_text = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{lang_code}">
<voice name="{voice}">
<prosody rate="{rate}">
{html.escape(text)}
</prosody> 
</voice>
</speak>"""

        communicate = edge_tts.Communicate(ssml_text, voice)
        await communicate.save(output_file)
        return output_file

    async def process_notes(self, tag, source_fields, audio_field, voice_1, voice_2=None, rate="+0%", overwrite=False, deck=None, abbreviations=None, log_callback=print, progress_callback=None, preview_only=False):
        try:
            if isinstance(source_fields, str):
                source_fields = [f.strip() for f in source_fields.split(',')]
            
            if not voice_2:
                voice_2 = voice_1

            # Build query
            query_parts = []
            if deck:
                query_parts.append(f'deck:"{deck}"')
            
            if tag:
                query_parts.append(f'tag:{tag}')
            
            # If neither tag nor deck is specified, warn? Or just fetch nothing?
            # Anki usually requires at least one constraint or it returns everything (dangerous)
            if not query_parts:
                full_query = "" # This might fetch ALL notes if not careful.
            else:
                full_query = " ".join(query_parts)

            if log_callback: log_callback(f"Searching: {full_query}...")
            
            if not full_query:
                if log_callback: log_callback("Please specify a Deck or a Tag.")
                return

            note_ids = self.invoke("findNotes", query=full_query)
            
            if not note_ids:
                if log_callback: log_callback("No notes found.")
                return

            if log_callback: log_callback(f"Found {len(note_ids)} notes. Fetching details...")
            
            if preview_only:
                import random
                # Pick a random note for preview to verify different cards
                target_notes = [random.choice(note_ids)]
            else:
                target_notes = note_ids

            notes_info = self.invoke("notesInfo", notes=target_notes)
            total_notes = len(notes_info)
            
            # Extract lang from voice name for strict SSML
            try:
                lang_code = "-".join(voice_1.split("-")[:2])
            except:
                lang_code = "en-US"

            for i, note in enumerate(notes_info):
                fields = note['fields']
                
                if not preview_only and not overwrite:
                    if audio_field in fields and fields[audio_field]['value']:
                         if log_callback: log_callback(f"Note {note['noteId']} already has audio. Skipping.")
                         if progress_callback: progress_callback((i + 1) / total_notes)
                         continue
                
                # Extract snippet for logging
                snippet = ""
                if source_fields and source_fields[0] in fields:
                    snippet = fields[source_fields[0]]['value']
                    # Clean snippet for display (remove html)
                    snippet = re.sub('<[^<]+?>', '', snippet).strip()[:30] + "..."
                
                if log_callback and not preview_only: 
                    log_callback(f"Processing ({i+1}/{total_notes}): {snippet}")

                full_ssml_parts = []
                
                for idx, s_field in enumerate(source_fields):
                    if s_field in fields:
                        raw_text = fields[s_field]['value']
                        # Pass abbreviations here
                        cleaned = self.clean_text_for_tts(raw_text, abbreviations)
                        
                        if cleaned:
                            current_voice = voice_1 if idx == 0 else voice_2
                            # Use double quotes for standard XML
                            part_ssml = f'<voice name="{current_voice}"><prosody rate="{rate}">{cleaned}</prosody></voice>'
                            full_ssml_parts.append(part_ssml)
                            
                    else:
                        if log_callback: log_callback(f"Warning: Field '{s_field}' not found in note {note['noteId']}")

                if full_ssml_parts:
                    # Join with break using standard double quotes
                    inner_content = ' <break time="1000ms" /> '.join(full_ssml_parts)
                    final_ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{lang_code}">{inner_content}</speak>'
                    
                    if preview_only:
                        if log_callback: log_callback(f"Generating preview for note {note['noteId']}...")
                        # Pass IS_SSML=True
                        return await self.generate_preview(final_ssml, voice_1, rate, is_ssml=True)
                    else:
                        # Pass IS_SSML=True
                        await self.generate_and_upload_audio(note['noteId'], final_ssml, voice_1, audio_field, log_callback, is_ssml=True)
                else:
                     if log_callback: log_callback(f"Note {note['noteId']}: Text is empty after cleanup.")
                
                if progress_callback: progress_callback((i + 1) / total_notes)

            if log_callback and not preview_only: log_callback("Done!")

        except Exception as e:
            if log_callback: log_callback(f"An error occurred: {e}")
            if log_callback: log_callback("Ensure Anki is running and AnkiConnect is installed.")

# Wrapper for CLI usage
async def main():
    # Default configuration for CLI
    ANKI_CONNECT_URL = "http://localhost:8765"
    NOTE_TAG = "vocab_korean" 
    SOURCE_FIELDS = ["Front", "Back"] # List of fields
    AUDIO_FIELD = "TTS"
    VOICE = "vi-VN-NamMinhNeural"  

    generator = AnkiGenerator(ANKI_CONNECT_URL)
    await generator.process_notes(NOTE_TAG, SOURCE_FIELDS, AUDIO_FIELD, VOICE)

if __name__ == "__main__":
    asyncio.run(main())
