import pytest
from unittest.mock import Mock
from file_without_pep8_and_not_fixed import welcome, help_command, unknown, send_reminder


class Tests:
    def test_help_command(self):
        update = Mock()
        context = Mock()

        update.message.text = "/help"
        help_command(update, context)

        # Проверяем, что была вызвана функция reply_text с ожидаемыми аргументами
        update.message.reply_text.assert_called_once_with("Используйте `/start` для тестирования.")

    def test_welcome_command(self):
        update = Mock()
        update.message.text = "welcome"
        welcome(update)
        update.message.reply_text.assert_called_once_with('Привет! Я бот-помощник в изучении английского языка.')

    def test_unknown_command(self):
        update = Mock()
        context = Mock()

        # Имитируем обновление с неизвестной командой
        update.message.text = "/unknown_command"
        unknown(update, context)

        # Проверяем, что была вызвана функция send_message с ожидаемыми аргументами
        context.bot.send_message.assert_called_once_with(
            chat_id=update.effective_chat.id,
            text="Sorry, I didn't understand that command."
        )

    def test_send_reminder(self):
        context = Mock()
        context.job = Mock()
        context.job.context = 'some_chat_id'

        send_reminder(context)

        context.bot.send_message.assert_called_once_with(
            chat_id='some_chat_id', text='Повторите слова!'
        )

if __name__ == '__main__':
    pytest.main()
