import sys
import os

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'third_party', 'Matcha-TTS'))

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io
import torch
import torchaudio
import logging
from typing import Optional, Dict
import tempfile

from cosyvoice.cli.cosyvoice import CosyVoice2
from cosyvoice.utils.file_utils import load_wav

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CosyVoice2 TTS API",
    description="Text-to-Speech API với CosyVoice2 Fine-tuned Model",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: thay bằng domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
cosyvoice_model = None
MODEL_PATH = r"C:\Users\japan\datasets\pretrained_models\CosyVoice2-0.5B--"
DEFAULT_PROMPT_TEXT = "cả hai bên hãy cố gắng hiểu cho nhau"

# Speaker configurations
SPEAKERS_CONFIG: Dict[str, Dict[str, str]] = {
    "male_voice": {
        # b thay đường dẫn 2 file và text tương ứng nhé
        "audio_path": r"C:\Users\japan\datasets\Speech\viVoice-train\@AnimeRewind.Official___000891.wav",
        "prompt_text": 'nhưng tại sao hắn lại được ca tụng là vua của nguyên hôn?'
    },
    "female_voice": {
        "audio_path": r"C:\Users\japan\Workspaces\AI\NLP\Speech\ref.wav",
        "prompt_text": 'cả hai bên hãy cố gắng hiểu cho nhau'
    },
    # Thêm các speaker khác tại đây
}

# Cache for loaded prompt audios
prompt_audio_cache: Dict[str, torch.Tensor] = {}

@app.on_event("startup")
async def load_model():
    """Load model và preload prompt audios khi khởi động"""
    global cosyvoice_model, prompt_audio_cache
    
    try:
        logger.info("=" * 60)
        logger.info("🚀 Starting CosyVoice2 TTS Server")
        logger.info("=" * 60)
        
        # Check model exists
        if not os.path.exists(MODEL_PATH):
            logger.error(f"❌ Model not found at: {MODEL_PATH}")
            logger.error("Please run: python backend/download_model.py")
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        
        logger.info(f"📂 Loading model from: {MODEL_PATH}")
        
        # Detect device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"🖥️  Device: {device}")
        
        # Load model
        cosyvoice_model = CosyVoice2(
            MODEL_PATH,
            load_jit=False,
            load_trt=False,
            load_vllm=False,
            fp16= False
        )
        
        logger.info("✅ Model loaded successfully!")
        logger.info(f"🎵 Sample rate: {cosyvoice_model.sample_rate} Hz")
        
        # Preload prompt audios
        logger.info("📢 Loading speaker configurations...")
        for speaker_name, config in SPEAKERS_CONFIG.items():
            audio_path = config["audio_path"]
            if os.path.exists(audio_path):
                try:
                    prompt_audio_cache[speaker_name] = load_wav(audio_path, 16000)
                    logger.info(f"  ✓ Loaded speaker: {speaker_name} from {audio_path}")
                except Exception as e:
                    logger.warning(f"  ⚠ Failed to load speaker {speaker_name}: {e}")
            else:
                logger.warning(f"  ⚠ Audio not found for speaker {speaker_name}: {audio_path}")
        
        logger.info(f"✅ Loaded {len(prompt_audio_cache)} speakers")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        logger.exception(e)
        raise

@app.on_event("shutdown")
async def shutdown():
    """Cleanup khi tắt server"""
    logger.info("🛑 Shutting down server...")
    global cosyvoice_model, prompt_audio_cache
    if cosyvoice_model:
        del cosyvoice_model
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
    prompt_audio_cache.clear()

class SFTRequest(BaseModel):
    text: str
    speaker: str = "default"

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CosyVoice2 TTS API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "speakers": "/speakers",
            "zero_shot": "/synthesize/zero-shot",
            "sft": "/synthesize/sft"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if cosyvoice_model else "unhealthy",
        "model_loaded": cosyvoice_model is not None,
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "sample_rate": cosyvoice_model.sample_rate if cosyvoice_model else None,
        "model_path": MODEL_PATH,
        "speakers_loaded": len(prompt_audio_cache)
    }

@app.get("/speakers")
async def list_speakers():
    """Liệt kê các speakers có sẵn"""
    return {
        "speakers": list(SPEAKERS_CONFIG.keys()),
        "loaded": list(prompt_audio_cache.keys()),
        "details": {
            name: {
                "prompt_text": config["prompt_text"],
                "audio_loaded": name in prompt_audio_cache
            }
            for name, config in SPEAKERS_CONFIG.items()
        }
    }

@app.post("/synthesize/zero-shot")
async def synthesize_zero_shot(
    text: str,
    prompt_text: str = DEFAULT_PROMPT_TEXT,
    prompt_audio: UploadFile = File(...)
):
    """
    Zero-shot TTS với reference audio
    
    Args:
        text: Văn bản cần tổng hợp
        prompt_text: Transcript của audio tham chiếu
        prompt_audio: File audio tham chiếu (WAV, 16kHz khuyến nghị)
    
    Returns:
        Audio file (WAV format)
    """
    if cosyvoice_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    temp_audio_path = None
    
    try:
        logger.info(f"🎙️  Zero-shot synthesis: '{text[:50]}...'")
        
        # Save uploaded audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_audio_path = temp_file.name
            content = await prompt_audio.read()
            temp_file.write(content)
        
        logger.info(f"📁 Saved reference audio: {temp_audio_path}")
        
        # Load reference audio (16kHz)
        prompt_speech_16k = load_wav(temp_audio_path, 16000)
        logger.info(f"🔊 Reference audio shape: {prompt_speech_16k.shape}")
        
        # Generate speech
        results = list(cosyvoice_model.inference_zero_shot(
            text,
            prompt_text,
            prompt_speech_16k,
            stream=False
        ))
        
        if not results:
            raise HTTPException(status_code=500, detail="No audio generated")
        
        # Get audio tensor
        audio_tensor = results[0]['tts_speech']
        duration = audio_tensor.shape[1] / cosyvoice_model.sample_rate
        
        logger.info(f"✅ Generated audio: {duration:.2f}s, shape: {audio_tensor.shape}")
        
        # Convert to WAV bytes
        audio_buffer = io.BytesIO()
        torchaudio.save(
            audio_buffer,
            audio_tensor,
            cosyvoice_model.sample_rate,
            format="wav"
        )
        audio_buffer.seek(0)
        
        return StreamingResponse(
            audio_buffer,
            media_type="audio/wav",
            headers={
                "Content-Disposition": "inline; filename=cozyvoice_output.wav",
                "X-Audio-Duration": str(duration),
                "X-Sample-Rate": str(cosyvoice_model.sample_rate)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Synthesis error: {e}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup temp file
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
                logger.debug(f"🗑️  Removed temp file: {temp_audio_path}")
            except:
                pass

@app.post("/synthesize/sft")
async def synthesize_sft(request: SFTRequest):
    """
    SFT mode - sử dụng giọng từ speaker configurations
    Thực chất sử dụng zero-shot với prompt audio và text đã được cấu hình
    
    Args:
        text: Văn bản cần tổng hợp
        speaker: Tên speaker (default: "default")
    
    Returns:
        Audio file (WAV format)
    """
    if cosyvoice_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Check if speaker exists
    if request.speaker not in SPEAKERS_CONFIG:
        available_speakers = list(SPEAKERS_CONFIG.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Speaker '{request.speaker}' not found. Available speakers: {available_speakers}"
        )
    
    # Check if speaker audio is loaded
    if request.speaker not in prompt_audio_cache:
        raise HTTPException(
            status_code=503,
            detail=f"Speaker '{request.speaker}' audio not loaded. Please check audio file path."
        )
    
    try:
        logger.info(f"🎤 SFT synthesis with speaker '{request.speaker}': '{request.text[:50]}...'")
        
        # Get speaker configuration
        speaker_config = SPEAKERS_CONFIG[request.speaker]
        prompt_text = speaker_config["prompt_text"]
        prompt_speech_16k = prompt_audio_cache[request.speaker]
        
        logger.info(f"🔊 Using speaker: {request.speaker}")
        logger.info(f"📝 Prompt text: {prompt_text}")
        logger.info(f"🎵 Prompt audio shape: {prompt_speech_16k.shape}")
        
        # Generate speech using zero-shot with configured speaker
        results = list(cosyvoice_model.inference_zero_shot(
            request.text,
            prompt_text,
            prompt_speech_16k,
            stream=False
        ))
        
        if not results:
            raise HTTPException(status_code=500, detail="No audio generated")
        
        audio_tensor = results[0]['tts_speech']
        duration = audio_tensor.shape[1] / cosyvoice_model.sample_rate
        
        logger.info(f"✅ Generated audio: {duration:.2f}s")
        
        # Convert to WAV
        audio_buffer = io.BytesIO()
        torchaudio.save(
            audio_buffer,
            audio_tensor,
            cosyvoice_model.sample_rate,
            format="wav"
        )
        audio_buffer.seek(0)
        
        return StreamingResponse(
            audio_buffer,
            media_type="audio/wav",
            headers={
                "Content-Disposition": f"inline; filename=cozyvoice_{request.speaker}_output.wav",
                "X-Audio-Duration": str(duration),
                "X-Speaker": request.speaker
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ SFT synthesis error: {e}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,  # Tắt reload cho production
        log_level="info"
    )