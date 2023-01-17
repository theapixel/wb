import wb
import time
import telebot

from config import *


bot = telebot.TeleBot(api_token)


if __name__ == '__main__':
	notifyed = dict()
	while True:
		begin_time = time.time()

		with open('cards.txt', 'r') as file:
			cards_ids = file.read().split()

		with open('stars_count.txt', 'r') as file:
			stars_count = int(file.read())

		for card_id in cards_ids:
			feedback = wb.get_last_feedback(int(card_id))
			if feedback <= stars_count:
				if card_id in notifyed:
					if ((time.time() - notifyed[card_id]) / 3600) >= 1:
						notifyed[card_id] = time.time()
						bot.send_message(admin_id, 'Feedback: ' + str(feedback) + '\nLink:\nhttps://www.wildberries.ru/catalog/' + card_id + '/feedbacks')
					else:
						print('Notifyed', card_id)
				else:
					notifyed[card_id] = time.time()
					bot.send_message(admin_id, 'Feedback: ' + str(feedback) + '\nLink:\nhttps://www.wildberries.ru/catalog/' + card_id + '/feedbacks')
			else:
				print('Passed', card_id)
		with open('timeout.txt', 'r') as file:
			timeout = float(file.read())

		print('\nwaiting\n')
		while (time.time() - begin_time) < (timeout * 60):
			time.sleep(1)