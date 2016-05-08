#!/usr/bin/env python3
import os
import socket
from random import randint

def get_segments(data, buff_size):
	'returns segmented version of data'
	segs = []
	x = 0

	for i in range(buff_size, len(data), buff_size):
		segs.append(data[i - buff_size:i])
		x = i
	segs.append(data[x:])
	return segs

def send_file(client, buff_size):
	file_names = ["pythonLogo.jpg", "pythonScript.py", "coursework.zip", "pythonNetworking.pdf"]
	f_name_request = client.recv(buff_size).decode("utf-8")
	try:
		f_name = file_names[file_names.index(f_name_request)]
		client.send("VALID".encode("utf-8"))
		print("SENDING FILE {}".format(f_name_request))

		f = open("tst_files/{}".format(f_name_request), "rb")
		f_data = f.read()
		f.close()
		if len(f_data) > buff_size:
			segements = get_segments(f_data, buff_size)
			for i in segements:	client.send(i)
		else:
			client.send(f_data)

		client.send("EOF".encode("utf-8"))
		print("FILE SENT")

	except ValueError:
		print("INVALID FILE NAME: {}. FILE DOESN'T EXIST".format(f_name_request))
		client.send("INVALID".encode("utf-8"))

def main():
	os.system("clear")
	addr = ("127.0.0.1", randint(1000, 2000))
	buff_size = 4096

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(addr)
	server.listen(5)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	file_names = ["pythonLogo.jpg", "pythonScript.py", "coursework.zip", "notorious.2009.mp4", "pythonNetworking.pdf"]

	while True:
		os.system("clear")
		print("Server Address: {}\nWaiting for client to connect...".format(addr))
		client, client_addr = server.accept()

		client.send("Connected to File Server. Files available: {}".format(str(file_names)).encode("utf-8"))

		while True:
			send_file(client, buff_size)

if __name__ == '__main__':
	main()
