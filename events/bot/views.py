import telebot
from django.shortcuts import HttpResponse
from .models import Notification
import api.models as api_models
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import get_user_model


bot = telebot.TeleBot(settings.BOT_TOKEN)
# https://api.telegram.org/bot6180293008:AAGqnW0xsH8jfx9HqZjAp24WR-H7Kbb-j2k/setWebhook?url=https://d350-217-151-229-99.ngrok-free.app


@csrf_exempt
def index(request):
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

    return HttpResponse('<h1>Ты подключился!</h1>')


@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'''Привет, {message.from_user.full_name}!

Я бот, созданный для напоминания об ивентах.

Чтобы начать получать напоминания, пожалуйста, напишите свою почту, указанный при регистрации на сайте.''')
    bot.register_next_step_handler(message, get_login)


def get_login(message: telebot.types.Message):
    login = message.text
    print(login)
    user = get_user_model().objects.get(email=login)
    print(user)
    if not user:
        bot.send_message(message.chat.id, 'Такого пользователя не существует. Попробуйте еще раз.')
        bot.register_next_step_handler(message, get_login)
    else:
        user.telegram_id = message.chat.id
        user.save()
        bot.send_message(message.chat.id, 'Отлично! Вы успешно авторизовались.')


@bot.message_handler(commands=['notify'])
def notify(message: telebot.types.Message):
    #выбрать все букинги, которые связаны с ивентами от сегодняшнего и дальше
    today = datetime.date.today()
    events = api_models.Event.objects.filter(date__gte=today).values('id')
    bookings = []
    for event in events:
        #добавить если нашел
        booking = api_models.Booking.objects.filter(event_id=event['id']).values('user_id')
        if booking:
            bookings.append(booking)
    
    #пройтись по всем букингам и найти уникальные юзеры
    users = []
    for booking in bookings:
        tg_id = get_user_model().objects.get(id=booking.values('user_id')[0]['user_id']).telegram_id
        if tg_id not in users:
            users.append(tg_id)

    #для каждого юзера выбрать ивенты, которые связаны с букингами и проверить совпадает ли дата -1 день с сегодняшней, -3 дня с сегодняшней, -7 дней с сегодняшней
    for user in users:
        events_for_user = {}
        events = []
        bookings = api_models.Booking.objects.filter(user_id=get_user_model().objects.get(telegram_id=user).id).values('event_id')
        for booking in bookings:
            events.append(api_models.Event.objects.get(id=booking['event_id']))
        for event in events:
            if event.date == today + datetime.timedelta(days=1):
                time = event.time
                date = event.date
                title = event.title
                if 'Завтра' not in events_for_user:
                    events_for_user['Завтра'] = [[time, date, title]]
                else:
                    events_for_user['Завтра'].append([time, date, title])
            elif event.date == today + datetime.timedelta(days=3):
                time = event.time
                date = event.date
                title = event.title
                if 'Через 3 дня' not in events_for_user:
                    events_for_user['Через 3 дня'] = [[time, date, title]]
                else:
                    events_for_user['Через 3 дня'].append([time, date, title])
            elif event.date == today + datetime.timedelta(days=7):
                time = event.time
                date = event.date
                title = event.title
                if 'Через неделю' not in events_for_user:
                    events_for_user['Через неделю'] = [[time, date, title]]
                else:
                    events_for_user['Через неделю'].append([time, date, title])
        #создать сообщение с напоминанием
        if events_for_user:
            text = f'Спешим напомнить! У вас есть ивенты на ближайшие дни:\n'
            for i in events_for_user:
                text += f'{i} - {events_for_user[i][0][1]}:\n'
                for j in events_for_user[i]:
                    text += f'{j[0]} - {j[2]}\n'
        bot.send_message(user, text)