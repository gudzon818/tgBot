from bot.i18n.translator import t


def test_translate_known_key_default_ru():
    assert t("start_greeting", "ru").startswith("Привет")


def test_translate_known_key_en():
    assert t("start_greeting", "en").startswith("Hi")


def test_translate_formatting():
    s = t("ping_pong", "en", ms=123)
    assert s == "Pong! 123 ms"


def test_translate_unknown_key_returns_key():
    assert t("__nope__", "en") == "__nope__"
