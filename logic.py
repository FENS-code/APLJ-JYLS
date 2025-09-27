from datetime import datetime, date
import hashlib
import random

def normalize_date_str(d: str) -> str:
    """把 YYYY-MM-DD 字符串转标准 ISO 格式并做基本校验。"""
    d = (d or "").strip()
    try:
        dt = datetime.strptime(d, "%Y-%m-%d").date()
        if dt.year < 1900 or dt > date.today():
            raise ValueError("日期范围不合理")
        return dt.isoformat()
    except Exception:
        return ""

def lucky_numbers_for(dob_iso: str, day_iso: str, count: int = 4):
    """
    基于 生日 + 指定日期 生成当日固定、不重复的幸运数字（1..99）。
    """
    if not dob_iso:
        return None, "请输入正确的生日（YYYY-MM-DD）"
    if not day_iso:
        return None, "今天日期异常"

    key = f"{dob_iso}|{day_iso}"
    md5hex = hashlib.md5(key.encode("utf-8")).hexdigest()
    seed = int(md5hex[:12], 16)  # 稳定种子
    rng = random.Random(seed)
    nums = sorted(rng.sample(range(1, 100), count))
    return nums, None
