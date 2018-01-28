
import pyaudio
import wave

import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def record_stuff():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 8000
    RECORD_SECONDS = 5

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    #wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    #wf.setnchannels(CHANNELS)
    #wf.setsampwidth(p.get_sample_size(FORMAT))
    #wf.setframerate(RATE)
    #wf.writeframes(b''.join(frames))
    #wf.close()

    return b''.join(frames);


def recognize(sndwav):
    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio into memory
    audio = types.RecognitionAudio(content=sndwav)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    recognized = ""
    for result in response.results:
        #print('Transcript: {}'.format(result.alternatives[0].transcript))
        recognized = result.alternatives[0].transcript

    return recognized


