import sys, re

my_string = ''
DICTIONARY = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789"
file = open('recentGamesLog.txt')
my_string = file.read()
_bitmask64 = 2**64 - 1


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

# m = re.findall(regex, my_string)
# print(m.string)

def regex_tvPort():
	regex = r"(\"tv_port\"\: (\d*)\,)"
	# print("*******tv_port's*******")
	tv_port_array = []
	regex = r"(\"tv_port\"\: (\d*)\,)"
	# iterator instead of findall
	for m in re.finditer(regex, my_string):
		tv_port_array.append(lower_bits(int(m.group(2))))
	# 	print(m.group(2))
	return tv_port_array

def regex_reservationID():
	# print("*******reservation_id's*******")
	reservation_id_array = []
	#\"low\"\: \-*(\d*),
	# regex = r"(\"reservationid\"\: \{.*(\d+),)"
	regex = r"(\"reservationid\": \{(.*?)\}\,)"
	# iterator instead of findall
	for d in re.finditer(regex, my_string, re.DOTALL):
		# print(d.group(1))
		# print(d.group(2))
		text = d.group(2)
		regex_low = r"(\"low\": (.*?)\,)"
		regex_high = r"(\"high\": (.*?)\,)"
		l = re.search(regex_low, text)
		# print("low:  " + l.group(2))
		h = re.search(regex_high, text)
		# print("high: " + h.group(2))
		output = combine_high_low_bytes(int(l.group(2)), int(h.group(2)))
		reservation_id_array.append(output)
		# print(output)
		# print("****************NEXT************")
		# print(reservation_id_array)
	return reservation_id_array


def regex_matchID():
	match_id_array = []
	# print("*******match_id's*******")
	#\"low\"\: \-*(\d*),
	# regex = r"(\"reservationid\"\: \{.*(\d+),)"
	regex = r"(\"matchid\": \{(.*?)\}\,)"
	# iterator instead of findall
	for f in re.finditer(regex, my_string, re.DOTALL):
		# match_id.append(f.group(2))
		# print(f.group(2))
		text = f.group(2)
		regex_low = r"(\"low\": (.*?)\,)"
		regex_high = r"(\"high\": (.*?)\,)"
		l = re.search(regex_low, text)
		# print("low:  " + l.group(2))
		h = re.search(regex_high, text)
		# print("high: " + h.group(2))
		output = combine_high_low_bytes(int(l.group(2)), int(h.group(2)))
		match_id_array.append(output)
		# print(output)
		# print("****************NEXT************")
		# print(match_id_array)
	return match_id_array


def encode(matchid, reservationid, tv):
	a = swap_endianness((tv << 128) | (reservationid << 64) | matchid)
	code = ''
	for _ in range(25):
		a,r = divmod(a, len(DICTIONARY))
		code += DICTIONARY[r]

	return "CSGO-%s-%s-%s-%s-%s" % (code[:5], code[5:10], code[10:15], code[15:20], code[20:])



match_id_8 = regex_matchID()
reservation_id_8 = regex_reservationID()
tv_port_8 = regex_tvPort()


print("*******match_id's*******")
print(match_id_8)

print("*******reservation_id's*******")
print(reservation_id_8)

print("*******tv_port's*******")
print(tv_port_8)

print("#############Encoding###############")
# print(encode(int(match_id_8[1]), int(reservation_id_8[1]), int(tv_port_8[1])))
# print(encode(int("3195305763127951438"), int("3195310206271619248"), int("50694")))

# print("testing low bits: -> " + tv_port_8[0])
# print(lower_bits(int(tv_port_8[0])))
# CSGO-p9WoE-aotud-CPnvH-VcnCW-rG64E

for i in range (0,8):
	print(encode(int(match_id_8[i]), int(reservation_id_8[i]), int(tv_port_8[i])))

