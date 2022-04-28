import telebot
from MTG_parser import MTG_bot
bot = telebot.TeleBot('5323342777:AAH9sVsJPU8r474PQPZz7MqaHps2eAMco08')
mtg_bot=MTG_bot()
@bot.message_handler(commands=["start"])
def start(m, res=False):
	bot.send_message(m.chat.id, 'Bot is activated')
@bot.message_handler(content_types=["text"])
def handle_text(message):
	msg = message.text
	if(msg.startswith('get_price ')):
		i1= msg.replace('get_price','')
		i2 = mtg_bot.search_mtg_ru(i1)
		i3 = mtg_bot.get_price_Goldfish(i2)
		i4 = bot.send_message(message.chat.id, str(i3))
	else:
		bot.send_message(message.chat.id, 'invalid command')
bot.polling(none_stop=True, interval=0)
