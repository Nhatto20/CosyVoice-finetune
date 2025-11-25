import re
from vi_cleaner.vi_cleaner import ViCleaner

# =========================
# 1) BỘ ĐỌC SỐ TIẾNG VIỆT
# =========================

read_units = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]

def read_two_digit(num: int):
    if 10 <= num <= 19:
        teen_map = {
            10: "mười",
            11: "mười một",
            12: "mười hai",
            13: "mười ba",
            14: "mười bốn",
            15: "mười lăm",
            16: "mười sáu",
            17: "mười bảy",
            18: "mười tám",
            19: "mười chín"
        }
        return teen_map[num]

    tens = num // 10
    unit = num % 10

    tens_word = [
        "", "", "hai mươi", "ba mươi", "bốn mươi",
        "năm mươi", "sáu mươi", "bảy mươi", "tám mươi", "chín mươi"
    ][tens]

    if unit == 0:
        return tens_word
    if unit == 5:
        return f"{tens_word} lăm"
    return f"{tens_word} {read_units[unit]}"

def read_number(num: int):
    if num < 10:
        return read_units[num]
    if num < 100:
        return read_two_digit(num)
    s = str(num)
    if len(s) == 3:
        return f"{read_units[num//100]} trăm {read_number(num%100)}"
    if len(s) == 4:
        return f"{read_units[num//1000]} nghìn {read_number(num%1000)}"
    return s


# =========================
# 2) ĐỌC NGÀY – THÁNG – NĂM
# =========================

def read_date(text: str):
    # 1) dd/mm/yyyy | dd-mm-yyyy | dd.mm.yyyy
    pattern_full = r"\b(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{2,4})\b"

    def repl_full(m):
        d, mth, y = map(int, m.groups())
        return f"ngày {read_number(d)} tháng {read_number(mth)} năm {read_number(y)}"

    text = re.sub(pattern_full, repl_full, text)

    # 2) dd/mm | d/m (chỉ ngày và tháng, không có năm)
    pattern_dm = r"\b(\d{1,2})[\/\-.](\d{1,2})\b"

    # Lưu ý: tránh trùng với pattern năm đã xử lý
    def repl_dm(m):
        d, mth = map(int, m.groups())
        return f"ngày {read_number(d)} tháng {read_number(mth)}"

    # Chỉ áp dụng cho những match không nằm trong pattern_full đã thay thế
    # Vì đã thay thế pattern_full, dd/mm/yyyy sẽ không còn nữa
    text = re.sub(pattern_dm, repl_dm, text)

    return text


# =========================
# 3) ĐỌC GIỜ – PHÚT – GIÂY
# =========================

def read_time(text: str):
    # hh:mm:ss
    pattern_hms = r"\b(\d{1,2}):(\d{1,2}):(\d{1,2})\b"
    def repl_hms(m):
        h, mi, s = map(int, m.groups())
        return f"{read_number(h)} giờ {read_number(mi)} phút {read_number(s)} giây"
    text = re.sub(pattern_hms, repl_hms, text)

    # hh:mm
    pattern_hm = r"\b(\d{1,2}):(\d{1,2})\b"
    def repl_hm(m):
        h, mi = map(int, m.groups())
        return f"{read_number(h)} giờ {read_number(mi)} phút"
    text = re.sub(pattern_hm, repl_hm, text)
    return text


# =========================
# 4) FIX SỐ 2 CHỮ SỐ CÒN LẠI
# =========================

def convert_two_digit_remaining(text: str):
    def repl(m):
        num = int(m.group())
        return read_two_digit(num)
    return re.sub(r"(?<!\d)(\d{2})(?!\d)", repl, text)


# =========================
# 5) TỔNG HỢP PIPELINE
# =========================

def vn_fix_all(text: str):
    text = read_date(text)
    text = read_time(text)
    text = convert_two_digit_remaining(text)
    return text


# =========================
# 6) LỚP WRAPPER VNCleaner
# =========================

class VNCleaner(ViCleaner):
    def clean_text(self, text: str, *args, **kwargs):
        if isinstance(text, str):
            text = vn_fix_all(text)
        return super().clean_text(text, *args, **kwargs)

    def clean(self, text: str, *args, **kwargs):
        return self.clean_text(text, *args, **kwargs)
