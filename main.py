from datetime import datetime, date
import hashlib
import random

def normalize_date_str(d: str) -> str:
    """把 YYYY-MM-DD 转为标准 ISO 并做基本校验；非法返回空串。"""
    d = (d or "").strip()
    try:
        dt = datetime.strptime(d, "%Y-%m-%d").date()
        if dt.year < 1900 or dt > date.today():
            raise ValueError("日期范围不合理")
        return dt.isoformat()
    except Exception:
        return ""

def lucky_number_for(dob_iso: str, day_iso: str):
    """
    基于 生日 + 日期 生成一个当日固定的 4 位幸运号码（0000–9999）。
    """
    if not dob_iso:
        return None, "请输入正确的生日（YYYY-MM-DD）"
    if not day_iso:
        return None, "今天日期异常"

    key = f"{dob_iso}|{day_iso}"
    md5hex = hashlib.md5(key.encode("utf-8")).hexdigest()
    seed = int(md5hex[:12], 16)  # 稳定种子
    rng = random.Random(seed)

    digits = [str(rng.randint(0, 9)) for _ in range(4)]
    number = "".join(digits)
    return number, None

def gen_numbers(dob: str, today: str):
    """
    供 JS 调用的桥接函数：返回 {dob, today, number} 或 {error}.
    """
    dob_iso = normalize_date_str(dob)
    if not dob_iso:
        return {"error": "请先选择有效的生日（YYYY-MM-DD）。"}
    number, err = lucky_number_for(dob_iso, today)
    if err:
        return {"error": err}
    return {"dob": dob_iso, "today": today, "number": number}
