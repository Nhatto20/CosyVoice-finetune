#!/bin/bash
# start.sh

echo "🚀 Starting CosyVoice2 TTS Server"
echo "=================================="

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate cosyvoice

# Check if model exists
if [ ! -d "models/CosyVoice2-0.5B" ]; then
    echo "❌ Model not found. Downloading..."
    python backend/download_model.py
fi

# Start backend
echo "🔧 Starting backend server..."
cd backend
python app.py