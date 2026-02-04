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
        
        # Filter for Vietnamese by default or just show all
        # Helper to format voice options
        voice_options = [v['ShortName'] for v in voices]
        default_index = 0
        try:
             # Try to set a default Vietnamese voice
             default_index = voice_options.index("vi-VN-NamMinhNeural")
        except ValueError:
             pass
             
        selected_voice = st.selectbox("Select Voice", voice_options, index=default_index)

    st.divider()
    
    start_btn = st.button("Start Generation", type="primary", disabled=not connected)

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
                    voice=selected_voice,
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
