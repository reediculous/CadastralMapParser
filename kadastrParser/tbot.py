import telebot
import os
from kadastrParser.excel import *
from kadastrParser.scraper import *

TOKEN = ""
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=["text", "document"])
def start(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "загрузите файл")
        bot.register_next_step_handler(message, get_doc)
    elif message.text == "/ping":
        bot.send_message(message.from_user.id, "pong!")
    else:
        bot.send_message(message.from_user.id, "такой команды нет!")


def get_doc(message):
    '''

    :param message: .xlsx file from user
    :return: .xlsx file with filled data
    '''
    try:
        tgfile = bot.get_file(file_id=message.document.file_id)  # Забираем файл из следующего сообщения пользователя
    except AttributeError:
        bot.send_message(message.from_user.id, "видимо, это не .xlsx файл. Попробуй снова")
        return
    except Exception:
        bot.send_message(message.from_user.id, "что-то пошло не так")
        return
    bot.send_message(message.from_user.id, "работаю, подождите")
    downloaded_file = bot.download_file(tgfile.file_path)
    with open('xlsfiles/test.xlsx', 'wb') as new_file:
        new_file.write(downloaded_file)
        new_file.close()
    file = Excel('xlsfiles/test.xlsx')
    driver = KadastrScraper()
    kads = file.get_col()
    pl = 1
    for kad in kads:
        if kad is None:
            continue
        a, c = driver.get_data(kad)
        file.write((pl, 2), a)
        file.write((pl, 3), c)
        pl += 1
    driver.close()
    file.close()
    bot.send_document(message.from_user.id, open('xlsfiles/test.xlsx', 'rb'))


bot.polling(none_stop=True, interval=0)

