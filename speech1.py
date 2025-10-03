import azure.cognitiveservices.speech as speechsdk
import streamlit as st
from datetime import datetime

# --- SECRET HANDLING ---
# This block correctly reads from the [azure_speech] section in your secrets.toml
try:
    speech_key = st.secrets["azure_speech"]["speech_key"]
    service_region = st.secrets["azure_speech"]["service_region"]
    
    if not speech_key or not service_region:
        raise ValueError("Azure Speech key or region is empty in secrets.")

except (KeyError, ValueError) as e:
    st.error(f"🚨 Error accessing Azure Speech secrets: {e}")
    st.info("Please check that your .streamlit/secrets.toml file is in the correct location and contains the correct keys.")
    st.stop()

def speech_recognize_once_from_mic():
    """Captures and recognizes a single utterance from the default microphone."""
    try:
        # Set up the speech config and audio config
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        audio_config = speechsdk.AudioConfig(use_default_microphone=True)

        # Create a speech recognizer with the given settings
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        # Blocking recognition call (no Streamlit UI calls here)
        result = speech_recognizer.recognize_once_async().get()

        # Check the result and return the appropriate message
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return f"**Recognized:** {result.text}"
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech could be recognized. Please try again."
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            # This provides a more detailed error from Azure
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                return f"**Error:** {cancellation_details.error_details}"
            return f"**Error:** Speech Recognition canceled. Reason: {cancellation_details.reason}"
        else:
            return "**Error:** An unknown error occurred."
    except Exception as e:
        return f"An application error occurred: {e}"


def delete_transcript(idx: int):
    """Delete transcript by index (safe callback for Streamlit on_click)."""
    if 'transcripts' in st.session_state and 0 <= idx < len(st.session_state['transcripts']):
        st.session_state['transcripts'].pop(idx)


st.title("Azure Speech-to-Text with Streamlit")
# Initialize session state to hold saved transcripts across reruns
if 'transcripts' not in st.session_state:
    st.session_state['transcripts'] = []

col1, col2 = st.columns([1, 1])

with col1:
    if 'is_recording' not in st.session_state:
        st.session_state['is_recording'] = False

    if st.button('🎤 Start Recognition', disabled=st.session_state.get('is_recording', False)):
        # set flag so UI shows microphone prompt across the rerun
        st.session_state['is_recording'] = True
        with st.spinner('Listening...'):
            recognition_result = speech_recognize_once_from_mic()
            # Append only non-empty results
            st.session_state['transcripts'].append({
                # store UTC epoch seconds; we'll render in local timezone for display
                'ts': datetime.utcnow().timestamp(),
                'text': recognition_result,
            })
        # recording finished
        st.session_state['is_recording'] = False

    # Show the microphone prompt when recording flag is set (persists across reruns)
    if st.session_state.get('is_recording', False):
        st.info('Speak into your microphone...')

with col2:
    if st.button('X Clear saved transcripts', disabled=st.session_state.get('is_recording', False)):
        st.session_state['transcripts'].clear()

# Display saved transcripts (most recent first)
st.subheader('Saved transcripts')
if st.session_state['transcripts']:
    # Iterate in reverse so newest appear first and we can delete by index
    for i in range(len(st.session_state['transcripts']) - 1, -1, -1):
        item = st.session_state['transcripts'][i]
        # convert stored UTC ts to local time for display
        try:
            dt_local = datetime.fromtimestamp(item['ts']).astimezone()
            # Build a friendly label without relying on platform-specific %-I
            date_str = dt_local.strftime('%b %d, %Y')
            hour = dt_local.strftime('%I').lstrip('0') or '0'
            minute = dt_local.strftime('%M')
            ampm = dt_local.strftime('%p')
            tz = dt_local.strftime('%Z')
            label = f"{date_str} • {hour}:{minute} {ampm} {tz}"
        except Exception:
            label = str(item.get('ts', ''))

        # layout: transcript text on left, small delete button on right
        left_col, right_col = st.columns([0.95, 0.05])
        with left_col:
            st.markdown(f"**{label}** — {item['text']}")
        with right_col:
            # unique key per item so Streamlit can track buttons across reruns
            # use on_click to delete immediately
            st.button('X', key=f"del_{i}", on_click=delete_transcript, args=(i,), disabled=st.session_state.get('is_recording', False))

    # No pending delete logic needed when using on_click callbacks
else:
    st.info('No transcripts saved yet. Click 🎤 Start Recognition to capture audio.')