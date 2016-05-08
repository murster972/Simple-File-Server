#!/usr/bin/env python3
import os

def segments(data, buff_size):
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
	image_f = open("tst.jpg", "rb")
	image_data = image_f.read()
	image_f.close()

	image_tst = open("tst_copy.jpg", "wb")
	buff_size = 4096
	segs = segments(image_data, buff_size)

	for i in segs:
		image_tst.write(i)

	image_tst.close()

if __name__ == '__main__':
	main()