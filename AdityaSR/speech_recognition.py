try:
    import whisper
except:
    print("Please install whisper")

try:
    import sounddevice as sd
except:
    print("Please install sounddevice")

try:
    import numpy as np
except:
    print("Please install numpy")

try:
    import asyncio
except:
    print("Can't import asyncio")

global model

def loadModel(modeel="base"):
    global model
    model = whisper.load_model(modeel)

async def speechRecognition(duration=1, exit=True):
    sample_rate = 16000

    print("Listening... Say 'exit' to quit.")

    print("Recording...")
    recording = sd.rec(int(duration * sample_rate),
                        samplerate=sample_rate,
                        channels=1,
                        dtype='float32')
    
    sd.wait()

    print("Transcribing...")
    audio = np.squeeze(recording)
    result = model.transcribe(audio, fp16=False)
    text = result["text"].strip()
    print("You said:", text)

    if "exit" in text.lower() and exit:
        print("Exiting...")
        quit()

    return result
