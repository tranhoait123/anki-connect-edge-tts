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

    async def process_notes(self, tag, source_field, audio_field, voice, log_callback=print, progress_callback=None):
        try:
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
                if source_field not in fields:
                    if log_callback: log_callback(f"Note {note['noteId']} does not have field '{source_field}'. Skipping.")
                    continue
                
                # Check if Audio field already has content
                if audio_field in fields and fields[audio_field]['value']:
                     if log_callback: log_callback(f"Note {note['noteId']} already has audio. Skipping.")
                     if progress_callback: progress_callback((i + 1) / total_notes)
                     continue
                
                source_text = fields[source_field]['value']
                import re
                clean_text = re.sub('<[^<]+?>', '', source_text).strip()
                
                if clean_text:
                    await self.generate_and_upload_audio(note['noteId'], clean_text, voice, audio_field, log_callback)
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
    SOURCE_FIELD = "Front"
    AUDIO_FIELD = "Audio"
    VOICE = "vi-VN-NamMinhNeural"  

    generator = AnkiGenerator(ANKI_CONNECT_URL)
    await generator.process_notes(NOTE_TAG, SOURCE_FIELD, AUDIO_FIELD, VOICE)

if __name__ == "__main__":
    asyncio.run(main())
