from src.normalizer import normalize_title


def test_normalize_title():
    assert normalize_title("《 总裁 的替嫁新娘 》") == "总裁的替嫁新娘"
