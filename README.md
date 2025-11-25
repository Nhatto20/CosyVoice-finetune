🎙️ Vietnamese Text-to-Speech với CosyVoice – Fine-tuning & Zero-Shot Voice Cloning
TTS tiếng Việt với CosyVoice + Web Demo (Zero-Shot & SFT Mode)
📌 Giới thiệu

Đây là dự án xây dựng hệ thống Text-to-Speech tiếng Việt dựa trên mô hình CosyVoice, một mô hình TTS hiện đại sử dụng kỹ thuật speech token và Flow Matching để sinh ra âm thanh tự nhiên, mượt mà và hỗ trợ zero-shot voice cloning.

Dự án thực hiện:

Fine-tuning mô hình CosyVoice trên 10.000 mẫu đầu tiên của bộ dữ liệu viVoice.

Xây dựng web demo gồm 2 chế độ:

Zero-Shot Voice Cloning: bắt chước giọng từ file WAV tham chiếu.

SFT Mode: chuyển văn bản sang giọng đã fine-tuned (male/female).

Triển khai backend API bằng FastAPI/Flask để sinh âm thanh theo thời gian thực.

Đánh giá mô hình bằng WER, CER, SIM, MOS.

🚀 Tính năng chính
1️⃣ Fine-tuning CosyVoice cho tiếng Việt

Sử dụng dataset viVoice từ HuggingFace.

Tiền xử lý: chuẩn hóa văn bản, cắt/trimming audio, chuẩn hóa sampling rate.

Huấn luyện với Supervised Fine-Tuning (SFT).

2️⃣ Zero-Shot Voice Cloning

Người dùng upload:

File audio.wav

Transcript audio

Text muốn chuyển sang giọng nói

CosyVoice trích xuất speaker embedding và mô phỏng giọng nói.

3️⃣ SFT Mode – Giọng mặc định

Nhập văn bản → chọn giọng male/female → sinh audio.

4️⃣ Web demo trực quan

Hai tab tương ứng hai chế độ hoạt động.

Hỗ trợ nghe/lưu file .wav.

Hướng dẫn cài đặt:

git clone:

``` sh
!git clone https://github.com/Nhatto20/CosyVoice-finetune.git
%cd CosyVoice-finetune
!git submodule update --init --recursive
```


``` sh
mkdir -p pretrained_models

cd pretrained_models

git lfs install
git clone https://huggingface.co/o6Dool/CosyVoice2-VN-Finetune CosyVoice2-0.5B-VN
```

tạo conda env:

``` sh
conda create -n cosyvoice -y python=3.10
conda activate cosyvoice
!pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

Weight: https://huggingface.co/o6Dool/CosyVoice2-VN-Finetune
Tải về và đặt folder "CosyVoice2-0.5B-VN" trong folder pretrained_models


để chạy ứng dụng web:

``` sh
python .\backend\app.py
```

``` sh
cd cd .\frontend
npm start
```
