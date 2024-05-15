#!/usr/bin/env python3

import sounddevice
import pyaudio
import wave

PATH='./audio_files/'

def record_audio(lang:str="yoruba") -> str:
    """
    Record audio from the microphone and save it to a file
    """
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024
    )

    frames = []

    try:
        while True:
            data = stream.read(1024)
            frames.append(data)

    except KeyboardInterrupt:
        print("\r", end="")
        print("audio recording finished...")

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

    audio_file = wave.open('{}{}.wav'.format(PATH, lang), 'wb')
    audio_file.setnchannels(1)
    audio_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    audio_file.setframerate(44100)
    audio_file.writeframes(b''.join(frames))
    audio_file.close()

    return '{}{}.wav'.format(PATH, lang)
