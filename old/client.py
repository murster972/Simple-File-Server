#!/usr/bin/env python3
import os
import socket

def main():
	os.system("clear")
	server_addr = ("192.168.1.123", int(input("Server Port Number: ")))
	buff_size = 4096

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(server_addr)

	welcome_msg = client.recv(buff_size).decode("utf-8")
	print(welcome_msg)

	while True:	
		request = input("request: ")

		if not len(request): break

		client.send(request.encode("utf-8"))
		response = client.recv(buff_size).decode("utf-8")
		if response[:11] == "Select File":
			print(response)
			f_name = input("File Name: ")
			client.send(f_name.encode("utf-8"))
			valid_f_name = client.recv(buff_size).decode("utf-8")

			if valid_f_name == "VALID":
				segements = []
				str_seg_r = ""

				while True:
					seg = client.recv(buff_size)
					#checks end of stream for the chars
					#'EOF' which significes the end of the file
					str_seg_r = str(seg)[::-1][1:4][::-1]
					if str_seg_r == "EOF":
						segements.append(seg[:len(seg) - 3])
						break
					else:
						segements.append(seg)

				f = open("tst_files_received/{}".format(f_name), "wb")
				for i in segements: f.write(i)
				f.close()

				print("FILE HAS BEEN RECEIVED")
			else:
				print("ERROR: INVALID FILE NAME.")
				continue

		else:
			print(response)

	client.send("".encode("utf-8"))
	print("Client Closed")
	client.close()

if __name__ == '__main__':
	main()