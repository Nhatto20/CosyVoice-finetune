from cosyvoice.cli.cosyvoice import CosyVoice2

model_dir = r"c:\Users\Admin\Documents\repo\CosyVoice\models\CosyVoice2-0.5B\CosyVoice2-0.5B"

cosy = CosyVoice2(
    model_dir,
    load_jit=False,
    load_onnx=False,
    load_trt=False,
)

print("Available speakers:", list(cosy.frontend.spk2info.keys()))
