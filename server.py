from fastapi import FastAPI, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from pocket_tts import TTSModel
import scipy.io.wavfile
import io
import uvicorn

app = FastAPI()

# Allow CORS for extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model on startup
print("Loading TTS Model...")
tts_model = TTSModel.load_model()
# Use 'alba' as seen in tts.py, or fall back to HF URL if needed
voice_state = tts_model.get_state_for_audio_prompt("alba")
print("TTS Model Loaded successfully.")

@app.post("/tts")
async def tts_endpoint(text: str = Form(...)):
    print(f"Received request for: {text[:30]}...")

    # Generate
    audio = tts_model.generate_audio(voice_state, text)

    # Convert to WAV
    buffer = io.BytesIO()
    # sample_rate is typically 24000
    scipy.io.wavfile.write(buffer, tts_model.sample_rate, audio.numpy())
    buffer.seek(0)

    return Response(content=buffer.read(), media_type="audio/wav")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
