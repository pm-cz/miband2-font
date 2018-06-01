#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Simple python command line tool to pack / unpack the Mifit2 font firmware files

# Based on codes provided
# by José Rebelo
# https://gist.github.com/joserebelo/b9be41b7b88774f712e2f864fdd39878
# and
# https://github.com/amazfitbip/tools/blob/master/bipfont.py

from PIL import Image
from pathlib import Path
import math
import binascii
import sys
import os
import glob

# Unpack the Amazfit Bip font file
# Creates 1bpp bmp images
def unpackFont(font_path):
	print('Unpacking', font_path)
	
	font_file = open(font_path, 'rb')
	font_path.join(font_path.split(os.sep)[:-1])
	if not os.path.exists('bmp'):
		os.makedirs('bmp')
	# header = 16 bytes
	header = font_file.read(16)
	num_bytes_characters = (header[15] << 8) + header[14]
	num_characters = num_bytes_characters // 2
	chars = font_file.read(num_bytes_characters)

	for i in range (0, num_characters):

		img = Image.new('1', (16, 16), 0)
		pixels = img.load()
		char_bytes = font_file.read(32)
		
		x = 0
		y = 0
		# big endian
		for byte in char_bytes:
			#print (byte)
			bits = [(byte >> bit) & 1 for bit in range(8 - 1, -1, -1)]
			for b in bits:
				pixels[x, y] = b
				x += 1
				if x == 16:
					x = 0
					y += 1
		img.save("bmp" + os.sep + '{:04x}'.format((chars[2*i+1] << 8) + chars[2*i]) + '0.bmp')

# Create a Amazfit Bip file from bmps
def packFont(font_path, english):
	print('Packing', font_path)
	font_file = open(font_path, 'wb')
	header = bytearray(binascii.unhexlify('484D5A4B01FFFFFFFF00FFFFFFFFCA00'))
	if (english == False):
		header[9] = 0xff;
	bmps = bytearray()
	
	range_nr = 0
	seq_nr = 0
	startrange = -1
	
	bmp_files = sorted(glob.glob('bmp' +  os.sep + '*.bmp'))
	header2 = bytearray(len(bmp_files) * 2);
	for i in range (0, len(bmp_files)):
		unicode = int(bmp_files[i][4:-5],16)
		header2[2*i] = unicode & 0xff
		header2[2*i+1] = unicode >> 8

	for i in range (0, len(bmp_files)):
		img = Image.open(bmp_files[i])
		img_rgb = img.convert('RGB')
		pixels = img_rgb.load()

		x = 0
		y = 0

		while y < 16:
			b = 0
			for j in range(0, 8):
				if pixels[x, y] != (0, 0, 0):
					b = b | (1 << (7 - j))
				x += 1
				if x == 16:
					x = 0
					y += 1
			bmps.extend(b.to_bytes(1, 'big'))
	rnr = (len(bmp_files)*2).to_bytes(2, byteorder='big')
	header[0xe] = rnr[1]
	header[0xf] = rnr[0]

	font_file.write(header)	
	font_file.write(header2)	
	font_file.write(bmps)		

if len(sys.argv) == 3 and sys.argv[1] == 'unpack':
	unpackFont(sys.argv[2])
elif len(sys.argv) == 3 and sys.argv[1] == 'pack':
	packFont(sys.argv[2], False)
elif len(sys.argv) == 4 and sys.argv[1] == 'pack':
	packFont(sys.argv[2], sys.argv[3] == 'en')
else:
	print('Usage:')
	print('   python', sys.argv[0], 'unpack Mili_chaohu.ft')
	print('   python', sys.argv[0], 'pack new_Mili_chaohu.ft en')
