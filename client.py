#!/usr/bin/env python3
import os
import sys
import socket

def get_file(sock, buff_size):
	f_name = input("File Name (Select from file name shown above): ")
	send_request(sock, f_name.encode("utf-8"))
	valid_f_name = sever_response(sock, buff_size).decode("utf-8")

	if valid_f_name == "VALID":
		#downloads all segments of file and then copies segments to new file
		segments = []
		str_seg_r = ""

		while True:
			seg = sock.recv(buff_size)
			#checks end of stream for the chars
			#'EOF' which significances the end of the file
			str_seg_r = str(seg)[::-1][1:4][::-1]
			if str_seg_r == "EOF":
				segments.append(seg[:len(seg) - 3])
				break
			else:
				segments.append(seg)

		f = open("received_files/{}".format(f_name), "wb")
		for i in segments: f.write(i)
		f.close()

		print("File received: received_files/{}".format(f_name))

	else:
		print("ERROR: INVALID FILE NAME")

	x = int(input("Continue[1] or Exit[2]: "))
	if x != 1:
		sock.close()
		print("Connection Closed.")
		sys.exit()

def send_request(sock, r):
	sock.send(r)

def sever_response(sock, buff_size):
	return sock.recv(buff_size)

def main():
	os.system("clear")
	server_addr = ("127.0.0.1", int(input("Server Port Number: ")))
	buff_size = 4096
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(server_addr)

	connected_msg = sever_response(client, buff_size).decode("utf-8")
	print(connected_msg)

	while True:
		get_file(client, buff_size)

if __name__ == '__main__':
	main()