import importlib


def test_import_app():
    m = importlib.import_module('bot.app')
    assert hasattr(m, 'main')


def test_import_handlers():
    for mod in [
        'bot.handlers.start', 'bot.handlers.help', 'bot.handlers.ping',
        'bot.handlers.feedback', 'bot.handlers.callbacks', 'bot.handlers.whoami',
        'bot.handlers.health', 'bot.handlers.admin', 'bot.handlers.items',
    ]:
        importlib.import_module(mod)


def test_settings_defaults():
    from bot.core.settings import settings
    assert settings.bot_token is not None
    assert isinstance(settings.log_level, str)


def test_runtime_uptime():
    from bot.services.runtime import mark_started, uptime_seconds
    mark_started()
    u1 = uptime_seconds()
    assert isinstance(u1, int)
