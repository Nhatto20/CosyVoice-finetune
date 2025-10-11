import argparse
import glob
import os
from tqdm import tqdm


def find_diff_segment(orig: str, norm: str, window: int = 1):
    """
    Tìm vị trí khác nhau token-wise giữa orig và norm.
    Trả về (orig_segment, norm_segment) gồm window token trước + token khác + window token sau.
    Nếu hoàn toàn giống nhau trả về (None, None).
    """
    orig_tokens = orig.split()
    norm_tokens = norm.split()
    min_len = min(len(orig_tokens), len(norm_tokens))

    # tìm index token khác đầu tiên
    idx = None
    for i in range(min_len):
        if orig_tokens[i] != norm_tokens[i]:
            idx = i
            break

    # nếu tất cả token đến min_len giống nhau nhưng độ dài khác -> khác vì thêm/bớt token
    if idx is None:
        if len(orig_tokens) != len(norm_tokens):
            idx = min_len
        else:
            return None, None

    start = max(0, idx - window)
    end = idx + 1 + window  # exclusive

    orig_segment = orig_tokens[start:end] if start < len(orig_tokens) else []
    norm_segment = norm_tokens[start:end] if start < len(norm_tokens) else []

    return ' '.join(orig_segment), ' '.join(norm_segment)


def main():
    wavs = list(glob.glob(f'{args.src_dir}/*/*/*wav'))

    if not wavs:
        print(f"No wav files found with pattern: {args.src_dir}/*/*/*wav")
        return

    for wav in wavs:
        txt_norm = wav.replace('.wav', '.normalized.txt')
        txt_orig = wav.replace('.wav', '.original.txt')

        # Check file normalized tồn tại
        if not os.path.exists(txt_norm):
            print(f"Missing normalized file: {txt_norm}")
            continue

        # Check file original tồn tại
        if not os.path.exists(txt_orig):
            print(f"Missing original file: {txt_orig}")
            continue

        # Đọc nội dung normalized
        with open(txt_norm, encoding="utf8") as f:
            norm_content = f.read().strip()

        # Đọc nội dung original
        with open(txt_orig, encoding="utf8") as f:
            orig_content = f.read().strip()

        # So sánh
        if norm_content != orig_content:
            orig_seg, norm_seg = find_diff_segment(orig_content, norm_content, window=1)
            if orig_seg is not None:
                print(f'original : "{orig_seg}"')
                print(f'normalized : "{norm_seg}"')
                print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_dir', type=str, required=True,
                        help="Thư mục chứa dữ liệu wav + text (expect structure: src_dir/<spk_id>/<chapter_id>/*.wav)")
    args = parser.parse_args()
    main()
