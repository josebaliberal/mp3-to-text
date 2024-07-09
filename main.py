import speech_recognition as sr
import easygui
import tempfile
import os
import uuid
from pydub import AudioSegment

LANGUAGE = 'en-GB' # Audio language

dir_path = os.path.dirname(os.path.abspath(__file__))
google_application_credentials = os.path.join(dir_path, 'credentials.json')

if not os.path.isfile(google_application_credentials):
    raise FileNotFoundError("Google Credentials file missing")

source_path = easygui.fileopenbox("Select audio file", "MP3 to TEXT", filetypes=['*.mp3'])
tmp_file_wav = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
output_path = os.path.splitext(source_path)[0] + '.txt'

# mp3 to wav
AudioSegment.from_mp3(source_path).export(tmp_file_wav, format='wav')

# wav to text
recognizer = sr.Recognizer()
with sr.AudioFile(tmp_file_wav) as source:
    audio_data = recognizer.record(source)

text = recognizer.recognize_google_cloud(
    audio_data=audio_data,
    credentials_json=google_application_credentials,
    language=LANGUAGE
)

# write output
with open(output_path, '+w') as writer:
    writer.write(text)
