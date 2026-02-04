import asyncio
import json
import urllib.request
import os
import hashlib
import edge_tts

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

    async def generate_and_upload_audio(self, note_id, text, voice, audio_field, log_callback=print):
        if not text:
            if log_callback: log_callback(f"Skipping note {note_id}: Source field is empty.")
            return

        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        filename = f"tts_{text_hash}.mp3"
        output_file = f"/tmp/{filename}"

        try:
            if log_callback: log_callback(f"Generating audio for: '{text}'...")
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

    def clean_text_for_tts(self, text):
        import re
        import html
        
        # Remove HTML tags (keeping content)
        text = re.sub('<[^<]+?>', '', text)
        # Remove citations like [1], [2]
        text = re.sub(r'\[\d+\]', '', text)
        # Remove emojis
        text = re.sub(r'[\U0001F300-\U0001F9FF]|[\U0001F600-\U0001F64F]|[\u2600-\u27BF]', '', text)
        # Remove long separators
        text = re.sub(r'[-_=]{3,}', ' ', text)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # XML Escape for SSML (Important!)
        text = html.escape(text)
        
        return text

    # Override generate_and_upload_audio to handle SSML if needed, 
    # but Communicate detects SSML automatically if it starts with <speak> usually.
    # However, to be safe, we will pass the text as is (which will be SSML).

    async def process_notes(self, tag, source_fields, audio_field, voice, log_callback=print, progress_callback=None):
        try:
            if isinstance(source_fields, str):
                source_fields = [f.strip() for f in source_fields.split(',')]

            if log_callback: log_callback(f"Searching for notes with tag: {tag}...")
            note_ids = self.invoke("findNotes", query=f"tag:{tag}")
            
            if not note_ids:
                if log_callback: log_callback("No notes found.")
                return

            if log_callback: log_callback(f"Found {len(note_ids)} notes. Fetching details...")
            notes_info = self.invoke("notesInfo", notes=note_ids)

            total_notes = len(notes_info)
            for i, note in enumerate(notes_info):
                fields = note['fields']
                
                if audio_field in fields and fields[audio_field]['value']:
                     if log_callback: log_callback(f"Note {note['noteId']} already has audio. Skipping.")
                     if progress_callback: progress_callback((i + 1) / total_notes)
                     continue
                
                full_text_parts = []
                for s_field in source_fields:
                    if s_field in fields:
                        raw_text = fields[s_field]['value']
                        cleaned = self.clean_text_for_tts(raw_text)
                        if cleaned:
                            full_text_parts.append(cleaned)
                    else:
                        if log_callback: log_callback(f"Warning: Field '{s_field}' not found in note {note['noteId']}")

                if full_text_parts:
                    # Construct SSML
                    # <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
                    # <voice name='...'>
                    # Part 1 <break time='1s' /> Part 2
                    # </voice> </speak>
                    
                    inner_content = ""
                    for idx, part in enumerate(full_text_parts):
                        inner_content += part
                        if idx < len(full_text_parts) - 1:
                            # Add break between fields
                            inner_content += ' <break time="1500ms" /> '
                    
                    ssml_text = f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='vi-VN'>
<voice name='{voice}'>
{inner_content}
</voice>
</speak>"""
                    
                    await self.generate_and_upload_audio(note['noteId'], ssml_text, voice, audio_field, log_callback)
                else:
                     if log_callback: log_callback(f"Note {note['noteId']}: Text is empty after cleanup.")
                
                if progress_callback: progress_callback((i + 1) / total_notes)

            if log_callback: log_callback("Done!")

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
