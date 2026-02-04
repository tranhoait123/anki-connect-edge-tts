import streamlit as st
import asyncio
import edge_tts
from anki_audio_generator import AnkiGenerator

st.set_page_config(page_title="Anki TTS Generator", page_icon="🎧")

st.title("🎧 Anki TTS Generator")
st.markdown("Generate audio for your Anki cards using Edge TTS.")

# Sidebar Configuration
with st.sidebar:
    st.header("Configuration")
    anki_url = st.text_input("AnkiConnect URL", value="http://localhost:8765")
    
    st.divider()
    st.markdown("### Status")
    try:
        generator = AnkiGenerator(anki_url)
        # Simple check to see if Anki is reachable
        version = generator.invoke("version")
        st.success(f"Connected to Anki (v{version})")
        connected = True
    except Exception as e:
        st.error(f"Cannot connect to Anki: {e}")
        st.info("Make sure Anki is running and AnkiConnect is installed.")
        connected = False

# Main Content
if connected:
    col1, col2 = st.columns(2)
    with col1:
        note_tag = st.text_input("Note Tag", value="vocab_korean", help="The tag of the notes to process")
        source_fields = st.text_input("Source Fields (Text)", value="Front, Back", help="Fields to read, comma-separated (e.g. 'Front, Back')")
    with col2:
        audio_field = st.text_input("Target Field (Audio)", value="TTS", help="Field to save the audio tag")
        
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
        
        # Default to Vietnamese if available
        default_lang_idx = 0
        if "vi-VN" in sorted_langs:
            default_lang_idx = sorted_langs.index("vi-VN")
            
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
            
        with col_l2:
            voice_1 = st.selectbox("Select Voice", current_lang_voices, index=get_voice_index(current_lang_voices, "NamMinhNeural"))
            # For single voice mode, voice_2 is just voice_1
            voice_2 = voice_1
            
        st.subheader("⏩ Audio Settings")
        speed = st.slider("Reading Speed", -50, 50, 0, format="%d%%")
        
        # Convert speed to string format e.g. "+10%" or "-10%"
        rate_str = f"{speed:+d}%"

    st.divider()
    
    col_act1, col_act2 = st.columns([1, 1])
    
    with col_act1:
        force_overwrite = st.checkbox("Force overwrite existing audio", value=False, help="If checked, audio will be regenerated even if the target field is not empty.")
        start_btn = st.button("Start Batch Generation", type="primary", disabled=not connected, use_container_width=True)
        
    with col_act2:
        st.write("") # Spacer
        st.write("") # Spacer
        preview_btn = st.button("🔊 Preview Sample (1 Note)", disabled=not connected, use_container_width=True)

    if preview_btn:
        with st.spinner("Generating preview..."):
             try:
                gen = AnkiGenerator(anki_url)
                
                async def run_preview():
                    return await gen.process_notes(
                        tag=note_tag,
                        source_fields=source_fields,
                        audio_field=audio_field,
                        voice_1=voice_1,
                        voice_2=voice_2,
                        rate=rate_str,
                        log_callback=None, # No UI logs for preview
                        preview_only=True
                    )
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                preview_file = loop.run_until_complete(run_preview())
                
                if preview_file:
                    st.audio(preview_file)
                    st.success("Playing preview of the first note found.")
                else:
                    st.warning("No notes found or generation failed.")

             except Exception as e:
                st.error(f"Error: {e}")

    if start_btn:
        progress_bar = st.progress(0, text="Starting...")
        log_area = st.empty()
        
        logs = []
        def log_callback(message):
            logs.append(message)
            # update log area with last few lines
            log_area.code("\n".join(logs[-10:]), language="text")

        def progress_callback(value):
            progress_bar.progress(value, text=f"Processing... {int(value*100)}%")

        try:
            # Re-instantiate generator to be safe inside button click
            gen = AnkiGenerator(anki_url)
            
            async def run_process():
                await gen.process_notes(
                    tag=note_tag,
                    source_fields=source_fields,
                    audio_field=audio_field,
                    voice_1=voice_1,
                    voice_2=voice_2,
                    rate=rate_str,
                    overwrite=force_overwrite,
                    log_callback=log_callback,
                    progress_callback=progress_callback
                )
            
            # Run the process
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_process())
            
            st.success("Generation Complete!")
            progress_bar.progress(1.0, text="Done!")
            
        except Exception as e:
            st.error(f"Error during execution: {e}")

else:
    st.warning("Please verify your AnkiConnect configuration in the sidebar to proceed.")
