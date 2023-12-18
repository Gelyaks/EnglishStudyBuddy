import datetime
import psycopg2
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from googletrans import Translator
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup,\
    InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler


TOKEN = 'СЮДА ТОКЕН БОТА'
reply_keyboard = [['Грамматика английского языка', 'Упражнения'],
                  ['Мои слова', 'Переводчик']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
state = 0
conn = psycopg2.connect(dbname='English_bot', user='юзернейм',
                        password='пароль.', host='localhost')
cursor = conn.cursor()
scheduler = BackgroundScheduler()


def welcome(update):
    """
    Responds to the /welcome command by sending a welcome message.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    update.message.reply_text('Привет! Я бот-помощник в изучении \
                                английского языка.')


def start(update, context):
    """
    Creates a custom keyboard with options such as
    'Грамматика английского языка',
    'Упражнения', 'Мои слова', and 'Переводчик',
    and sends a message
    inviting the user to explore the available options.

    :param update: An object representing information
    about the incoming message/event.
    :type update: object of type Update from
    the python-telegram-bot library
    :param context: An object representing the
    context of the current chat.
    :type context: object of type CallbackContext
    from the python-telegram-bot library
    :return: None
    """
    reply_keyboard = [['Грамматика английского языка', 'Упражнения'],
                      ['Мои слова', 'Переводчик']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Воспользуйся клавиатурой и посмотри, \
                             что я умею!', reply_markup=markup)


def choose_type_of_rules(update):
    """
    Sends a message and offers a keyboard to choose a specific type of
    English language rules.

    :param update: An object representing information
    about the incoming message/event.
    :type update: object of type Update from
    the python-telegram-bot library
    :return: None
    """
    global state
    group_keyboard = [['Tenses', 'Conditionals'], ['Modals'],
                      ['Gerund', 'Relative Clause'], ['Articles', 'Used To'],
                      ['Вернуться в главное меню']]
    markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=True)
    update.message.reply_text('Какое конкретно правило вы хотите вспомнить?',
                              reply_markup=markup)
    state = 0


def choose_tense(update):
    """
    Sends a message and offers a keyboard to choose a rule for specific
    English tense.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global state
    group_keyboard = [['Present Simple', 'Present Continuous'],
                      ['Present Perfect', 'Present Perfect Continuous'],
                      ['Past Simple', 'Past Continuous'],
                      ['Past Perfect', 'Past Perfect Continuous'],
                      ['Future Simple', 'Future Perfect Continuous'],
                      ['Назад']]
    markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=False)
    update.message.reply_text('Какое правило, связанное с временами \
                               английского языка, вы хотите узнать?',
                              reply_markup=markup)
    state = 1


def choose_conditionals(update):
    """
    Sends a message and offers a keyboard to choose a specific rule for types
    of English conditionals for reminding to
    the user.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global state
    group_keyboard = [['Zero Conditional', 'First Conditional'],
                      ['Second Conditional', 'Third Conditional'], ['Назад']]
    markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=False)
    update.message.reply_text('Какой type of conditionals вам напомнить?',
                              reply_markup=markup)
    state = 1


def choose_modal(update):
    """
    Sends a message and offers a keyboard to choose a rule if specific modal
    verbs for reminding to the user.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global state
    group_keyboard = [['Must Have Done', 'Should Have Done'],
                      ['Could Have Done', 'Need Not Have Done'], ['Назад']]
    markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=False)
    update.message.reply_text('Какие модальные глаголы вам напомнить?',
                              reply_markup=markup)
    state = 1


def choose_gerund(update):
    """
    Sends a message and offers a keyboard to choose between the rules of ING
    Gerund and TO Infinitive for reminding to
    the user.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global state
    group_keyboard = [['ING Gerund', 'TO Infinitive'], ['Назад']]
    markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=False)
    update.message.reply_text('Выберите нужную опцию.', reply_markup=markup)
    state = 1


def choose_relative_clause(update):
    """
    Sends a message and offers a keyboard to choose between the rules of
    Defining and Non-defining relative clauses for reminding to the user

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global state
    group_keyboard = [['Defining', 'Non-defining'], ['Назад']]
    markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=False)
    update.message.reply_text('Выберите тип relative clause.',
                              reply_markup=markup)
    state = 1


def choose_article(update):
    """
    Sends a message and offers a keyboard to choose a rule of setting the
    specific article(the, a) or its absence for reminding to the user.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global state
    group_keyboard = [['the', 'a'], ['-'], ['Назад']]
    markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=False)
    update.message.reply_text('Какой артикль хотите повторить?',
                              reply_markup=markup)
    state = 1


def choose_used_to(update):
    """
     Sends a message and offers a keyboard to choose a rule between 'Used To',
     'Would', 'Be Used To', 'Get Used To' for reminding to the user.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global state
    group_keyboard = [['Used To', 'Would'], ['Be Used To', 'Get Used To'],
                      ['Назад']]
    markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=False)
    update.message.reply_text('Выберите, что конкретно хотите узнать.',
                              reply_markup=markup)
    state = 1


def return_chosen_rule_from_db(update):
    """
    Retrieves and sends the explanation and example for the chosen grammar rule
    from the database postgres.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    cursor.execute(f"SELECT subsectionid FROM grammarsubsections"
                   f" WHERE subsectionname = '{update.message.text}'")
    section_id = cursor.fetchall()[0][0]
    cursor.execute(f"SELECT explanation, example FROM grammar_rules"
                   f" WHERE subsectionid = {section_id}")
    res = cursor.fetchall()[0][0]
    update.message.reply_text(res)


def exercises_choose(update):
    """
    Sends a message and a keyboard to choose a grammar topic for practicing
    exercises.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global state, markup
    group_keyboard = [['Tenses', 'Conditionals'], ['Modals'],
                      ['Gerund', 'Relative Clause'],
                      ['Articles', 'Used To'], ['Вернуться в главное меню']]
    markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=False)
    update.message.reply_text('Выберите тему, чтобы '
                              'поупражняться в грамматике!'
                              'Чтобы поупражняться,'
                              'выполните сначала все упражнения на одну тему,'
                              'а затем все упражнения на другую и т.д.',
                              reply_markup=markup)
    state = 2


def exercises(update, context):

    """
    Sends a grammar exercise to the user, including a sentence with a blank
    space and multiple options for filling the blank, in the same message
    offers the right answer in spoiler format.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :param context: Context object for the callback.
    :type context: telegram.ext.CallbackContext
    :return: None
    """
    user_id = update.effective_user.id
    current_index = context.user_data.get(user_id, 0)
    cursor.execute(f"SELECT sectionid FROM grammarsections "
                   f"WHERE sectionname = '{update.message.text}'")
    section_id = cursor.fetchall()[0][0]
    cursor.execute(f"SELECT task_text, option1, option2, option3, correct"
                   f" FROM grammar_tasks WHERE sectionid = {section_id}")
    res = cursor.fetchall()

    if current_index >= len(res):
        update.message.reply_text("Вы прошли все упражнения. Можете начать"
                                  "сначала или выбрать другую тему.")
        context.user_data[user_id] = 0
        return

    task, answer1, answer2, answer3, corr_answ = res[current_index]
    context.user_data[user_id] = current_index + 1
    context.user_data[f'{user_id}_corr_answ'] = corr_answ
    update.message.reply_text(f'Заполните пропуск: \n '
                              f'{task} \n словами: {answer1}, '
                              f'{answer2}, {answer3}. '
                              f'\n Кстати, правильный ответ'
                              f' <tg-spoiler>{corr_answ}</tg-spoiler>.',
                              reply_markup=markup, parse_mode=ParseMode.HTML)


def my_vocab_options(update):
    """
    Sends a message and a keyboard to choose options for managing a personal
    vocabulary list.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global markup, state
    vocab_options = [['Добавить новые слова для повторения',
                     'Удалить слово из списка'], ['Повторить слова'],
                     ['Установить напоминание', 'Вернуться в главное меню']]
    markup = ReplyKeyboardMarkup(vocab_options, one_time_keyboard=False)
    update.message.reply_text('Выберите, что конкретно хотите сделать.',
                              reply_markup=markup)


def new_word(update):
    """
    Sends a message prompting the user to write a new word they want to add to
    their personal vocabulary list.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global state
    update.message.reply_text('Напишите новое слово, которое хотите добавить',
                              reply_markup=markup)
    state = 4


def add_new_word_to_list(update):
    """
    Adds a new word with its definition to the user's personal vocabulary list
    to the table in database.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global markup, state
    user_id = update.message.chat.id
    word_and_definition = update.message.text
    word_and_definition = word_and_definition.split(' - ', 1)
    if len(word_and_definition) >= 2:
        word = word_and_definition[0].strip()
        definition = ' '.join(word_and_definition[1:]).strip()
        cursor.execute('SELECT * FROM user_vocabulary '
                       'WHERE user_id = %s AND word = %s', (user_id, word))
        existing_word = cursor.fetchone()
        if existing_word:
            update.message.reply_text(f'Слово "{word}" уже существует в \
                                      вашем списке.')
        else:
            cursor.execute(f"INSERT INTO user_vocabulary "
                           f"VALUES ({user_id}, '{word}', '{definition}')")
            conn.commit()
            update.message.reply_text(f"Слово {word} с объяснением "
                                      f"{definition} добавлено",
                                      reply_markup=markup)
    else:
        update.message.reply_text('Пожалуйста, введите и слово, и его '
                                  'объяснение в одном сообщении в формате: '
                                  'слово - объяснение.')
    state = 3


def old_word(update):
    """
    Sends a message prompting the user to write a word they want
    to delete from their personal vocabulary list saved in
    the table in the database.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global state, markup
    update.message.reply_text('Напишите новое слово, '
                              'которое хотите удалить', reply_markup=markup)
    state = 5


def remove_word(update):
    """
    Removes a word from the user's personal vocabulary
    list in the table in database.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    global state
    user_id = update.message.from_user.id
    word_delete = update.message.text
    cursor.execute('SELECT * FROM user_vocabulary '
                   'WHERE user_id = %s AND word = %s', (user_id, word_delete))
    existing_word = cursor.fetchone()
    if existing_word:
        cursor.execute('DELETE FROM user_vocabulary '
                       'WHERE user_id = %s AND word = %s',
                       (user_id, word_delete))
        conn.commit()
        update.message.reply_text(f'Слово "{word_delete}" '
                                  f'удалено из вашего списка.')
    else:
        update.message.reply_text(f'Слова "{word_delete}" '
                                  f'нет в вашем списке.')
    state = 3


def start_repeat(update, context):
    """
    Initiates the process of repeating words for the user.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :param context: Context object for the callback.
    :type context: telegram.ext.CallbackContext
    :return: Output of the repeat_words function
    """
    user_id = update.message.from_user.id
    context.user_data['user_id'] = user_id
    return repeat_words(update, context)


def create_review_keyboard():
    """
    Creates and returns an inline keyboard for reviewing
    words during repetition.

    :return: InlineKeyboardMarkup
        The inline keyboard with "Помню" and "Не помню" buttons.
    """
    keyboard = [
        [InlineKeyboardButton("Помню", callback_data='remember')],
        [InlineKeyboardButton("Не помню", callback_data='forget')],
    ]
    return InlineKeyboardMarkup(keyboard)


def repeat_words(update, context):
    """
    Handles the repetition of words from the user's vocabulary
    list in the table in the database.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :param context: Context object for the callback.
    :type context: telegram.ext.CallbackContext
    :return: None
    """
    user_id = context.user_data.get('user_id')
    cursor.execute(f"SELECT word, definition "
                   f"FROM user_vocabulary "
                   f"WHERE user_id = {user_id}")
    word_list = cursor.fetchall()
    if not word_list:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Ваш список слов пока пуст. '
                                      'Добавьте новые слова!')
        return
    current_index = context.user_data.get('current_index', 0)
    if current_index >= len(word_list):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Вы повторили все слова в списке. '
                                      'Начинаю заново')
        current_index = 0
    current_word, current_explanation = word_list[current_index]
    context.user_data['current_word'] = current_word
    context.user_data['current_explanation'] = current_explanation
    context.user_data['current_index'] = current_index + 1
    reply_markup = create_review_keyboard()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'Слово: {current_word}',
                             reply_markup=reply_markup)


def handle_review(update, context):
    """
    Handles the user's response during word review.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :param context: Context object for the callback.
    :type context: telegram.ext.CallbackContext
    :return: None
    """
    query = update.callback_query.data
    if 'current_word' not in context.user_data or\
            'current_explanation' not in context.user_data:
        return
    current_explanation = context.user_data['current_explanation']
    if query == 'forget':
        update.callback_query.message.reply_text('Объяснение: '
                                                 f'{current_explanation}')
    repeat_words(update, context)


def set_reminder(update, context):
    """
    Sets a daily reminder for the user.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update

    :param context: Context object for the callback.
    :type context: telegram.ext.CallbackContext

    :return: None
    """
    context.job_queue.run_daily(send_reminder, datetime.time(hour=18, minute=0,
                                tzinfo=pytz.timezone('Europe/Moscow')),
                                days=(0, 1, 2, 3, 4, 5, 6),
                                context=update.message.chat_id)
    update.message.reply_text('Напоминание установлено! Вы будете получать '
                              'напоминание каждый вечер в 18:00.')


def send_reminder(context):
    """
    Sends a reminder message to the user.

    :param context: Context object for the scheduled job.
    :type context: apscheduler.schedulers.base.BaseJobContext
    :return: None
    """
    context.bot.send_message(chat_id=context.job.context,
                             text='Повторите слова!')


def start_translate(update):
    """
    Initiates the process of translating a word between Russian and English.

    :param update: An object representing information about the incoming message/event.
    :type update: object of type Update from the python-telegram-bot library

    Sends a prompt for the user to enter a new word for translation.
    """
    global state
    update.message.reply_text('Напишите новое слово, которое '
                              'хотите перевести на английский'
                              'язык с русского или с английского '
                              'на русский язык',
                              reply_markup=markup)
    state = 6


# начало заимствования шаблона кода с сайта:
# https://hccoder.info/category/python/post-884?ysclid=lq9z011ik8571044807
def translator_google(update):
    """
    Initiates the process of translating words between Russian and English.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    translator = Translator()
    user_message = update.message.text
    user_language = translator.detect(user_message).lang
    if user_language == 'ru':
        sent = translator.translate(user_message)
    elif user_language == 'en':
        sent = translator.translate(user_message, dest='ru')
    else:
        sent = translator.translate(user_message, dest='en')
    update.message.reply_text(f'Перевод: {sent.text}')
# конец заимствования


def text(update, context):
    """
    Handles text messages received by the bot and processes user input based on the current state.

    :param update: An object representing information about the incoming message/event.
    :type update: object of type Update from the python-telegram-bot library
    :param context: An object representing the context of the current chat.
    :type context: object of type CallbackContext from the python-telegram-bot library

    Global variables:
    - state: Defines the current state of the conversation.
    - markup: Markup for custom keyboards.

    Processes user input and performs actions based on the content of the message
    and the current state of the conversation.
    :return: None
    """
    global state, markup
    key_words = ['Present', 'Past', 'Future', 'Have', 'Gerund', "Infinitive",
                 'Conditional', 'Defining', 'Non-defining', 'the', 'a', '-',
                 'Used', 'Would']
    key_exercises_words = ['Tenses', 'Modals', 'Gerund', 'Conditionals',
                           'Relative Clause', 'Articles', 'Used To']
    if update.message.text == 'Грамматика английского языка' or \
            update.message.text == 'Назад':
        choose_type_of_rules(update)
    elif update.message.text == 'Вернуться в главное меню':
        start(update, context)
    elif state == 0 and update.message.text == 'Tenses':
        choose_tense(update)
    elif state == 0 and update.message.text == 'Conditionals':
        choose_conditionals(update)
    elif state == 0 and update.message.text == 'Modals':
        choose_modal(update)
    elif state == 0 and update.message.text == 'Gerund':
        choose_gerund(update)
    elif state == 0 and update.message.text == 'Relative Clause':
        choose_relative_clause(update)
    elif state == 0 and update.message.text == 'Articles':
        choose_article(update)
    elif state == 0 and update.message.text == 'Used To':
        choose_used_to(update)
    elif state == 1 and any(word in update.message.text for word in key_words):
        return_chosen_rule_from_db(update)
    elif update.message.text == 'Упражнения':
        exercises_choose(update)
    elif state == 2 and any(word in update.message.text
                            for word in key_exercises_words):
        exercises(update, context)
    elif update.message.text == 'Мои слова':
        my_vocab_options(update)
    elif update.message.text == 'Добавить новые слова для повторения':
        new_word(update)
    elif state == 4:
        add_new_word_to_list(update)
    elif update.message.text == 'Удалить слово из списка':
        old_word(update)
    elif state == 5:
        remove_word(update)
    elif update.message.text == 'Повторить слова':
        start_repeat(update, context)
    elif update.message.text == 'Установить напоминание':
        set_reminder(update, context)
    elif update.message.text == 'Переводчик':
        start_translate(update)
    elif state == 6:
        translator_google(update)


def help_command(update):
    """
    Sends a help message in response to the "/help" command.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update
    :return: None
    """
    update.message.reply_text("Используйте `/start` для тестирования.")


def unknown(update, context):
    """
    Sends a message indicating that the command is not recognized.

    :param update: Update object representing an incoming update.
    :type update: telegram.Update

    :param context: Context object for the callback.
    :type context: telegram.ext.CallbackContext

    :return: None
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


def main():
    """
    Main function to initialize and run the Telegram bot.

    Uses the python-telegram-bot library to set up the bot, add command handlers,
    and start polling for incoming updates.
    The main function of the Telegram bot.

    :return: None
    """
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("welcome", welcome))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CallbackQueryHandler(handle_review))
    scheduler.start()
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

