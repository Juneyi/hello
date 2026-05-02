import re
import unicodedata


def normalize_title(title: str) -> str:
    if title is None:
        return ""
    s = str(title)
    s = unicodedata.normalize("NFKC", s)
    s = s.strip().lower()
    s = s.replace("《", "").replace("》", "").replace("<", "").replace(">", "")
    s = re.sub(r"[\s\u3000]+", "", s)
    s = re.sub(r"[\.,，。!！\?？:：;；\-—_~`'\"“”‘’\(\)（）\[\]【】{}、/\\|]+", "", s)
    return s
