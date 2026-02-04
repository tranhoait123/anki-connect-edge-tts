import streamlit as st
import asyncio
import edge_tts
import json
import os
from anki_audio_generator import AnkiGenerator

st.set_page_config(page_title="Anki TTS Generator", page_icon="🎧")

st.title("🎧 Anki Flashcard Audio Generator")
st.markdown("Generate AI audio for your Anki cards using Microsoft Edge TTS.")

# Settings File
SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)
    except Exception as e:
        print(f"Failed to save settings: {e}")

defaults = load_settings()

# Sidebar Configuration
with st.sidebar:
    st.header("Configuration")
    anki_url = st.text_input("AnkiConnect URL", value=defaults.get("anki_url", "http://localhost:8765"))
    
    st.divider()
    st.markdown("### Status")
    try:
        generator = AnkiGenerator(anki_url)
        # Simple check to see if Anki is reachable
        version = generator.invoke("version")
        st.success(f"Connected to Anki (v{version})")
        connected = True
    except Exception as e:
        st.error("Could not connect to Anki.")
        st.info("Make sure Anki is open and AnkiConnect is installed.")
        st.caption(f"Error: {e}")
        connected = False

# Main Content
if connected:
    # Fetch Decks
    try:
        decks = AnkiGenerator(anki_url).invoke("deckNames")
    except:
        decks = []
    
    col1, col2 = st.columns(2)
    with col1:
        # Deck Selector
        deck_options = ["(All Decks)"] + sorted(decks)
        
        # Restore selected deck
        default_deck_idx = 0
        saved_deck = defaults.get("deck", "(All Decks)")
        if saved_deck in deck_options:
            default_deck_idx = deck_options.index(saved_deck)
            
        selected_deck = st.selectbox("Filter by Deck", deck_options, index=default_deck_idx)
        actual_deck = None if selected_deck == "(All Decks)" else selected_deck
        
        note_tag = st.text_input("Filter by Tag (Optional)", value=defaults.get("tag", "vocab_korean"), help="Leave empty to use only Deck filter")
        source_fields = st.text_input("Source Fields (Text)", value=defaults.get("source_fields", "Front, Back"), help="Fields to read, comma-separated (e.g. 'Front, Back')")
        
    with col2:
        audio_field = st.text_input("Target Field (Audio)", value=defaults.get("audio_field", "TTS"), help="Field to save the audio tag")
        
        # Async function to get voices
        async def get_voices():
            voices = await edge_tts.list_voices()
            return sorted(voices, key=lambda v: v['ShortName'])

        # Run async function to get voices
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        voices = loop.run_until_complete(get_voices())
        
        # Helper to format voice options and languages
        # Voice structure example: {'Name': 'Microsoft Server Speech Text to Speech Voice (vi-VN, NamMinhNeural)', 'ShortName': 'vi-VN-NamMinhNeural', ...}
        
        languages = set()
        voices_by_lang = {}
        
        for v in voices:
            # Extract language code (e.g., vi-VN) from ShortName (vi-VN-NamMinhNeural)
            parts = v['ShortName'].split('-')
            if len(parts) >= 3:
                lang_code = f"{parts[0]}-{parts[1]}"
                if lang_code not in languages:
                    languages.add(lang_code)
                    voices_by_lang[lang_code] = []
                voices_by_lang[lang_code].append(v['ShortName'])
        
        sorted_langs = sorted(list(languages))
        
        # UI for Language Selection
        st.subheader("🔊 Voice Settings")
        
        col_l1, col_l2 = st.columns(2)
        
        # Default to Vietnamese if available or restored
        default_lang_idx = 0
        saved_lang = defaults.get("language", "vi-VN")
        if saved_lang in sorted_langs:
            default_lang_idx = sorted_langs.index(saved_lang)
            
        with col_l1:
            selected_lang = st.selectbox("Language", sorted_langs, index=default_lang_idx)
            
        # UI for Voice Selection (filtered by language)
        current_lang_voices = voices_by_lang.get(selected_lang, [])
        
        # Default voice index logic
        def get_voice_index(voice_list, name_part):
            for idx, v in enumerate(voice_list):
                if name_part in v:
                    return idx
            return 0
        
        saved_voice = defaults.get("voice", "NamMinhNeural")
        default_voice_idx = get_voice_index(current_lang_voices, saved_voice)
            
        with col_l2:
            voice_1 = st.selectbox("Select Voice", current_lang_voices, index=default_voice_idx)
            # For single voice mode, voice_2 is just voice_1
            voice_2 = voice_1
            
        st.subheader("⏩ Audio Settings")
        speed = st.slider("Reading Speed", -50, 50, defaults.get("speed", 0), format="%d%%")
        
        # Convert speed to string format e.g. "+10%" or "-10%"
        rate_str = f"{speed:+d}%"

    st.divider()
    
    # Abbreviation Section
    default_abbr ="BN=Bệnh nhân\nTHA=Tăng huyết áp\nK=Ung thư"
    with st.expander("📝 Medical Abbreviations (Expansion)", expanded=False):
        abbr_text = st.text_area("Enter substitutions (one per line, e.g., BN=Bệnh nhân)", value=defaults.get("abbreviations", default_abbr), height=100)
    
    # Parse abbreviations
    abbreviations = {}
    if abbr_text:
        for line in abbr_text.split('\n'):
            if '=' in line:
                parts = line.split('=', 1)
                short, full = parts[0].strip(), parts[1].strip()
                if short and full:
                    abbreviations[short] = full

    col_act1, col_act2 = st.columns([1, 1])
    
    with col_act1:
        force_overwrite = st.checkbox("Force overwrite existing audio", value=defaults.get("overwrite", False), help="If checked, audio will be regenerated even if the target field is not empty.")
        start_btn = st.button("Start Batch Generation", type="primary", disabled=not connected, use_container_width=True)
        # The start_btn is replaced by the new "Start Generation" button below
        # start_btn = st.button("Start Batch Generation", type="primary", disabled=not connected, use_container_width=True)
        
    with col_act2:
        st.write("") # Spacer
        st.write("") # Spacer
        preview_btn = st.button("🎲 Preview Random Note", disabled=not connected, use_container_width=True)

    # Simple Mode Checkbox
    simple_mode = st.checkbox("⚠️ Chế độ đơn giản (Simple Mode)", help="Chọn cái này nếu bị lỗi máy đọc mã lệnh (SSML). Chế độ này sẽ tắt giọng địa phương và ngắt nghỉ nâng cao, chỉ đọc văn bản thuần.")

    if preview_btn:
        with st.spinner("Generating preview..."):
             try:
                gen = AnkiGenerator(anki_url)
                
                async def run_preview():
                    return await gen.process_notes(
                        tag=note_tag,
                        deck=actual_deck,
                        source_fields=source_fields,
                        audio_field=audio_field,
                        voice_1=voice_1,
                        voice_2=voice_2,
                        rate=rate_str,
                        abbreviations=abbreviations,
                        log_callback=None, # No UI logs for preview
                        preview_only=True,
                        simple_mode=simple_mode
                    )
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                preview_file = loop.run_until_complete(run_preview())
                
                if preview_file:
                    st.audio(preview_file)
                    
                    with open(preview_file, "rb") as f:
                        btn = st.download_button(
                            label="📥 Download Preview",
                            data=f,
                            file_name="preview.mp3",
                            mime="audio/mpeg"
                        )
                    
                    st.success("Playing preview of a random note.")
                else:
                    st.warning("No notes found or generation failed.")

             except Exception as e:
                st.error(f"Error: {e}")

    # Generate Button
    if st.button("🚀 Start Generation", type="primary", disabled=not connected, use_container_width=True):
        if not source_fields:
            st.error("Please enter at least one source field.")
        else:
            # SAVE SETTINGS
            new_settings = {
                "anki_url": anki_url,
                "deck": selected_deck,
                "tag": note_tag,
                "source_fields": source_fields,
                "audio_field": audio_field,
                "language": selected_lang,
                "voice": voice_1,
                "speed": speed,
                "abbreviations": abbr_text,
                "overwrite": force_overwrite
            }
            save_settings(new_settings)

            log_container = st.empty()
            progress_bar = st.progress(0, text="Starting...")
            
            def update_log(msg):
                log_container.code("\n".join(logs[-10:]), language="text") # Re-using the original log display logic
            
            logs = [] # Initialize logs for the new logging mechanism
            def log_callback(message): # Re-using the original log_callback
                logs.append(message)
                update_log(message)

            try:
                gen = AnkiGenerator(anki_url)
                
                async def run_gen():
                    await gen.process_notes(
                        tag=note_tag,
                        deck=actual_deck,
                        source_fields=source_fields,
                        audio_field=audio_field,
                        voice_1=voice_1,
                        voice_2=voice_2,
                        rate=rate_str,
                        overwrite=force_overwrite,
                        abbreviations=abbreviations,
                        log_callback=log_callback,
                        progress_callback=progress_bar.progress,
                        simple_mode=simple_mode
                    )

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(run_gen())
                
                st.success("Generation Complete!")
                progress_bar.progress(1.0, text="Done!") # Ensure progress bar completes
                
            except Exception as e:
                st.error(f"Error during execution: {e}")

else:
    st.warning("Please verify your AnkiConnect configuration in the sidebar to proceed.")
