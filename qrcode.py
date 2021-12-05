import cv2
from help_func2 import *
from pyzbar import pyzbar
import random


def qr_code(message):
	f_id = message.photo[len(message.photo)-1].file_id
	file_name=bot.get_file(f_id)
	down_file=bot.download_file(file_name.file_path)
	with open(f'img_ {random.randint(1, 1000)}'+'.jpg', 'wb') as file:
		file.write(down_file)
	img = cv2.imread("img_.jpg")
	barcodes = pyzbar.decode(img)

	for barcode in barcodes:
         barcodeData = barcode.data.decode('utf-8')
         print(f'Result: {barcodeData}')
         bot.send_message(message.chat.id, text = barcodeData)
