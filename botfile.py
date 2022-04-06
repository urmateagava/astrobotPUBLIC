import telebot
from telebot import types
import xmlfile
import database


token = 'nicetokenbot'
bot = telebot.TeleBot(token)
signscb = {"Овен": "aries", "Телец": "taurus", "Близнецы": "gemini", "Рак": "cancer", "Лев": "leo",
           "Дева": "virgo", "Весы": "libra", "Скорпион": "scorpio", "Стрелец": "sagittarius",
           "Козерог": "capricorn", "Водолей": "aquarius", "Рыбы": "pisces"}
signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев",
         "Дева", "Весы", "Скорпион", "Стрелец",
         "Козерог", "Водолей", "Рыбы"]

days = ['На вчера', 'На сегодня', 'На завтра', 'На послезавтра']
dayscb = {'На вчера': 'yesterday', 'На сегодня': 'today', 'На завтра': 'tomorrow', 'На послезавтра': 'tomorrow02'}

wars = ['Личный гороскоп', 'Гороскоп', 'Рассылка']
warscb = {'Личный гороскоп': 'private_horoscope', 'Гороскоп': 'horoscope', 'Рассылка': 'mailing list'}


def main():
    @bot.message_handler(commands=['start'])
    def start_function(message):
        user_id = message.from_user.id
        if database.checker(user_id) is None:
            markup = types.InlineKeyboardMarkup(row_width=2)
            for sign in signs:
                btn = types.InlineKeyboardButton(sign, callback_data=signscb.get(sign))
                markup.add(btn)
            bot.send_message(user_id, 'Выберите знак', reply_markup=markup)
            user_name = message.from_user.username
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            database.set_user(user_id, user_name, first_name, last_name)
            database.set_user_j_day(user_id)
        else:
            descript = """
            🔮 AAB может:
        
            Составлять ваш личный гороскоп(/ph) 🦋
            **********************************************************
            При первом вводе данных бот запоминает ваш знак
            зодиака и использует его в будущем (если в первый
            раз вы выбрали не свой знак, его можно изменить
            командой /reset_sign)
            
            
            Составлять гороскоп на любой из знаков зодиака
            **********************************************************
            (Команда /h)
            Расскажите близкому о его судьбе 🌅
            
            
            Рассылать гороскопы ежедневно 
            **********************************************************
            Для того что бы бот сам отправлял вам гороскоп 
            каждый день, подпишитесь на рассылку
            (команда /m)
            Это бесплатно ☘
            Отписаться от рассылки можно командой /m_end️ 
            """
            bot.send_message(user_id, descript)

    @bot.message_handler(commands=['ph'])
    def personal_horoscope(message):
        user_id = message.from_user.id
        markup = types.InlineKeyboardMarkup(row_width=2)
        for day in days:
            btn = types.InlineKeyboardButton(day, callback_data=dayscb.get(day))
            markup.add(btn)
        bot.send_message(user_id, 'Выберите день', reply_markup=markup)

    @bot.message_handler(commands=['reset_sign'])
    def resetsign(message):
        user_id = message.from_user.id
        bot.reply_to(message, """
        Введите знак начиная с большой буквы 
        (Овен, Телец, Близнецы, Рак, Лев,
             Дева, Весы, Скорпион, Стрелец,
             Козерог, Водолей, Рыбы)
             """)
        @bot.message_handler(content_types=['text'])
        def msgresetsign(message):
            global text
            text = message.text
            if text in signs:
                database.power_set_sign(user_id, signscb.get(text))
                bot.send_message(user_id, 'Знак успешно изменен')
            elif text not in signs:
                bot.send_message(user_id, 'Знак введен не правильно, попробуйте ещё раз')
        bot.register_next_step_handler(message, msgresetsign)

    @bot.message_handler(commands=['h'])
    def horoscope(message):
        user_id = message.from_user.id
        markup = types.InlineKeyboardMarkup(row_width=2)
        for sign in signs:
            btn = types.InlineKeyboardButton(sign, callback_data=signscb.get(sign))
            markup.add(btn)
        bot.send_message(user_id, 'Выберите знак', reply_markup=markup)

    @bot.message_handler(commands=['m'])
    def mailing(message):
        user_id = message.from_user.id
        if database.check_mailling(user_id)[0]:
            bot.send_message(user_id, 'Вы уже подписаны на рассылку')
        else:
            database.upmailling(user_id)
            bot.send_message(user_id, 'Вы успешно подписались на рассылку')

    @bot.message_handler(commands=['m_end'])
    def mailingdown(message):
        user_id = message.from_user.id
        if database.check_mailling(user_id)[0]:
            database.downmailling(user_id)
            bot.send_message(user_id, 'Вы отписались от рассылки')
        else:
            bot.send_message(user_id, 'Вы не подписаны на рассылку')

    @bot.callback_query_handler(func=lambda call: True)
    def markups(call):
        user_id = call.from_user.id
        if call.data in dayscb.values():
            day = call.data
            sign = database.take_sign(user_id)
            resp = xmlfile.astro(sign[0], day)
            bot.send_message(user_id, resp)
        else:
            if call.data in signscb.values():
                markup = types.InlineKeyboardMarkup(row_width=2)
                for day in days:
                    btn = types.InlineKeyboardButton(day, callback_data=call.data + "/" + dayscb.get(day))
                    markup.add(btn)
                bot.send_message(user_id, 'Выберите день', reply_markup=markup)
            else:
                call_data = str(call.data).split('/')
                day = call_data[1]
                sign = call_data[0]
                resp = xmlfile.astro(sign, day)
                if database.checker_f_sign(user_id, user_id) is None:
                    database.set_user_sign(user_id, sign)
                bot.send_message(user_id, resp)
