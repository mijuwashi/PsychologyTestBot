import telebot


bot = telebot.TeleBot('1836468433:AAHb1uYUISkmb0S4wJKvGv8ZUC4NOfeeSqk')
global score
score = []


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Добрый день, {0.first_name} {0.last_name}!\nМеня зовут {1.first_name}. '
                     'Я помогаю сформировать психологическое состояние человека.\n'
                     'На основе ваших предоставленных данных я покажу вам ваше '
                     'психологическое состояние'.format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')
    bot.send_message(message.from_user.id, 'Желаете пройти тест для определения вашего психологического состояния?')
    bot.register_next_step_handler(message, get_otv)


@bot.message_handler(content_types='text')
def get_otv(message):
    global otv
    global a
    a = 'Да'
    otv = message.text
    if otv == str(a):
        bot.send_message(message.from_user.id, 'Отлично!, тогда начнем!\nСколько вам лет?')
        bot.register_next_step_handler(message, get_pointAge)
    elif message.text != str(a):
        bot.send_message(message.from_user.id, 'Как скажете! Всего доброго!')
        bot.stop_bot()


def get_pointAge(message):
    global pointAge
    pointAge = message.text
    if message.text.isdigit() and float(pointAge) > 0:
        score.append(float(pointAge))
        bot.send_message(message.from_user.id, 'Сколько дней в неделю вы выходите погулять, отдохнуть?')
        bot.register_next_step_handler(message, get_pointRest)
    else:
        bot.send_message(message.from_user.id, 'Извините, не могу понять ваш ответ...')
        bot.register_next_step_handler(message, get_pointAge)


def get_pointRest(message):
    global pointRest
    pointRest = message.text
    if message.text.isdigit() and float(pointRest) > 0:
        score.append(float(pointRest))
        bot.send_message(message.from_user.id, 'На сколько баллов из 10 вы оцените своё нынешнее состояние?')
        bot.register_next_step_handler(message, get_pointStatus)
    else:
        bot.send_message(message.from_user.id, 'Извините, не могу понять ваш ответ...')
        bot.register_next_step_handler(message, get_pointRest)


def get_pointStatus(message):
    global pointStatus
    pointStatus = message.text
    if message.text.isdigit() and float(pointStatus) > 0:
        score.append(float(pointStatus))
        bot.send_message(message.from_user.id, 'Сколько дней в неделю вы едите вредную пищу?')
        bot.register_next_step_handler(message, get_pointFood)
    else:
        bot.send_message(message.from_user.id, 'Извините, не могу понять ваш ответ...')
        bot.register_next_step_handler(message, get_pointStatus)


def get_pointFood(message):
    global pointFood
    pointFood = message.text
    if message.text.isdigit() and float(pointFood) > 0:
        score.append(float(pointFood))
        bot.send_message(message.from_user.id, 'Один момент, обрабатываю ваши данные по суперкрутому алгоритму')
        bot.send_message(message.from_user.id, 'Ваше эмоциональное состояние:')
        bot.send_message(message.from_user.id, finalScore(score[0], score[1], score[2], score[3]), parse_mode='html')
        finalMessage(message)


def finalScore(age, rest, status, food):
    global allPoint
    allPoint = age / (food * 2) + food + status + rest
    if allPoint < 15:
        return 'Ой-ой! У вас замечен очень низкий уровень серотонина. Вы слишком печальны! Советую срочно обратиться ' \
               'к психологу! Могу предложить ссылку: https://psi.mchs.gov.ru/ '
    elif 15 <= allPoint <= 30:
        return 'Вы вполне довольны жизнью! Не переставайте радоваться событиям, которые происходят с вами, ' \
               'и вы никогда не будете унывать!'
    elif allPoint > 25:
        return 'Ого! Вы очень-очень счастливы! С вами точно всё нормально? Посмотрите грустное видео, чтобы стабилизировать состояние: https://youtu.be/SvPSLvAZfYs'


def finalMessage(message):
    score.clear()
    bot.send_message(message.from_user.id, 'Благодарю за прохождение психологического теста. Надеюсь он вам помог! '
                                           'Нажмите /start, если хотите повторить тест.')


bot.infinity_polling()
