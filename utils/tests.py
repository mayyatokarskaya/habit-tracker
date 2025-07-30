from unittest.mock import patch, MagicMock
from utils.telegram import send_telegram_message


def test_send_message_no_token(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    # Проверяем, что функция просто возвращается и выводит предупреждение
    send_telegram_message("Hello")


@patch("utils.telegram.requests.post")
def test_send_message_success(mock_post, monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    send_telegram_message("Hello")

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    # Проверяем URL
    assert "fake_token" in args[0]
    # Проверяем данные payload
    assert kwargs["data"]["chat_id"] == "12345"
    assert kwargs["data"]["text"] == "Hello"


@patch("utils.telegram.requests.post")
def test_send_message_raises_exception(mock_post, monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")

    mock_post.side_effect = Exception("Network error")

    send_telegram_message("Hello")
