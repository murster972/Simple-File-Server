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

def main():
	os.system("clear")
	addr = ("192.168.1.123", randint(1000, 2000))
	buff_size = 4096

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(addr)
	server.listen(5)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	file_names = ["coursework.zip", "johnLegend.mp3", "tst.jpg", "tst.pdf"]

	while True:
		os.system("clear")
		print("Server Address: {}\nWaiting for client...".format(addr))
		client, client_addr = server.accept()

		print("INTIAL CONNET :: Client connected with address {}".format(client_addr))
		client.send("Connected to file server at: {}".format(str(addr)).encode("utf-8"))

		while True:
			try:
				client_request = client.recv(buff_size).decode("utf-8")
			except ConnectionResetError: break
			if not len(client_request): break

			print(client_request)

			if client_request == "GET":
				client.send("Select File. Files Available: {}".format(str(file_names)).encode("utf-8"))
				f_name_request = client.recv(buff_size).decode("utf-8")
				try:
					f_name = file_names[file_names.index(f_name_request)]
					client.send("VALID".encode("utf-8"))
					msg = "SENDING FILE {}".format(f_name_request)
					print(msg)
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
					err = "INVALID FILE NAME: {}. FILE DOESN'T EXIST".format(f_name_request)
					print(err)
					client.send("INVALID".encode("utf-8"))
			else:
				client.send("RECIEVED: {}".format(client_request).encode("utf-8"))

		print("Client Connection Closed")
		client.close()
		c = int(input("Listen[1] or Close[2]: "))
		if c != 1: break

	print("Server Connection Closed")
	server.close()


if __name__ == '__main__':
	main()