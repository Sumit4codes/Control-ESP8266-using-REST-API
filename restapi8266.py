import wave
import json
from vosk import Model, KaldiRecognizer
# import librosa
# import soundfile as sf
import sounddevice as sd
from scipy.io.wavfile import write
import requests

# Path to the downloaded Vosk model
model_path = "vosk-model-small-en-us-0.15"

# Load the Vosk model
model = Model(model_path)

# Initialize the recognizer with the model and sample rate
recognizer = KaldiRecognizer(model, 16000)

# Parameters
sample_rate = 16000  # Sample rate in Hz
duration = 5  # Duration of recording in seconds
filename = "output.wav"  # Output file name

# Record audio from microphone
print("Recording...")
audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
sd.wait()  # Wait until recording is finished
print("Recording finished!")

# Save the recorded audio as a WAV file
write(filename, sample_rate, audio_data)

esp8266_ip = "http://192.168.175.139"
def send_led_command(state):
    # Send a GET request with the state (0 or 1)
    url = f"{esp8266_ip}/{state}"
    try:
        response = requests.get(url)
        print(f"Sent {state} to ESP8266, response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")


file_path= filename

# Open an audio file for recognition
with wave.open(file_path, "rb") as wf:
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print(json.loads(result)["text"])

    # Print the final result
gttext= json.loads(result)["text"]
text2list = gttext.split()
print(text2list)
if "on" in text2list:
    send_led_command(1)
else:
    send_led_command(0)


