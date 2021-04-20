import os
import lzma
import glob
import json
import subprocess

import pyrogram
from pyrogram.errors import UnknownError

from config import (
	PYROGRAM_OPTIONS,
	BOOKS_CHAT
)

tracked_files = [
	(
		file.split(sep="/")[2].split(sep=".")[0]
	) for file in glob.glob(pathname="../covers/*")
]

with lzma.open(filename="books.json.xz", mode="r") as file:
	books = orjson.loads(file.read())

client = pyrogram.Client(**PYROGRAM_OPTIONS)
client.start()

total_files = 0

for book in books:
	if book["cover"]["file_unique_id"] not in tracked_files:
		
		path_name = "../covers/" + book["cover"]["file_unique_id"] + ".jpg"
		
		upload_file = None
		
		# Baixo a imagem do Telegram e salvo localmente
		while not upload_file:
			try:
				message = client.get_messages(BOOKS_CHAT, book["cover"]["message_id"])
				upload_file = client.download_media(message, path_name)
			except UnknownError:
				pass
		
		total_files += 1
		
		command = [
			"git",
			"add",
			path_name
		]
		
		subprocess.call(command)
		
		if total_files >= 10000:
			command = [
				"git",
				"commit",
				"-m",
				"Add more covers"
			]
			subprocess.call(command)
			total_files = 0

client.log_out()
