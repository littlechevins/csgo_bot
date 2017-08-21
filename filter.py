# Algorithm from https://github.com/ValvePython/csgo/blob/master/csgo/sharecode.py

import sys, re

my_string = ''
DICTIONARY = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789"
filename = 'recentGamesLog.txt'
file = open(filename)
my_string = file.read()

#swaps storage or high and low endian's
def swap_endianness(num):
	result = 0
	for n in range(0,144,8):
		result = (result << 8) + ((num >> n) & 0xFF)

	return result

# returns lower 16bit
def lower_bits(num):
	return (num & 0xffff)

def combine_high_low_bytes(low, high):
	num = (high << 32) + low
	return num


# Capture tv port

def regex_tvPort():
	regex = r"(\"tv_port\"\: (\d*)\,)"
	tv_port_array = []
	regex = r"(\"tv_port\"\: (\d*)\,)"
	# iterator instead of findall
	for m in re.finditer(regex, my_string):
		tv_port_array.append(lower_bits(int(m.group(2))))
	return tv_port_array

# Capture reservation id

def regex_reservationID():
	reservation_id_array = []
	regex = r"(\"reservationid\": \{(.*?)\}\,)"
	# iterator instead of findall
	for d in re.finditer(regex, my_string, re.DOTALL):

		text = d.group(2)
		regex_low = r"(\"low\": (.*?)\,)"
		regex_high = r"(\"high\": (.*?)\,)"
		l = re.search(regex_low, text)
		h = re.search(regex_high, text)
		output = combine_high_low_bytes(int(l.group(2)), int(h.group(2)))
		reservation_id_array.append(output)

	return reservation_id_array

# Capture match id

def regex_matchID():
	match_id_array = []

	regex = r"(\"matchid\": \{(.*?)\}\,)"
	# iterator instead of findall
	for f in re.finditer(regex, my_string, re.DOTALL):

		text = f.group(2)
		regex_low = r"(\"low\": (.*?)\,)"
		regex_high = r"(\"high\": (.*?)\,)"
		l = re.search(regex_low, text)
		h = re.search(regex_high, text)
		output = combine_high_low_bytes(int(l.group(2)), int(h.group(2)))
		match_id_array.append(output)

	return match_id_array

# Encodes into CSGO-XXXXX-XXXXX-XXXXX-XXXXX using given inputs

def encode(matchid, reservationid, tv):
	a = swap_endianness((tv << 128) | (reservationid << 64) | matchid)
	code = ''
	for _ in range(25):
		a,r = divmod(a, len(DICTIONARY))
		code += DICTIONARY[r]

	return "CSGO-%s-%s-%s-%s-%s" % (code[:5], code[5:10], code[10:15], code[15:20], code[20:])


# Calling fn

match_id_8 = regex_matchID()
reservation_id_8 = regex_reservationID()
tv_port_8 = regex_tvPort()


# print("Reading from " + filename)

# print("Encoding..")

for i in range (0,8):
	print(encode(int(match_id_8[i]), int(reservation_id_8[i]), int(tv_port_8[i])))
