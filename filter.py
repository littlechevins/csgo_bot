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

def regex_tvPort():
	regex = r"(\"tv_port\"\: (\d*)\,)"
	tv_port_array = []
	regex = r"(\"tv_port\"\: (\d*)\,)"
	# iterator instead of findall
	for m in re.finditer(regex, my_string):
		tv_port_array.append(lower_bits(int(m.group(2))))
	return tv_port_array

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

for i in range (0,8):
	print(encode(int(match_id_8[i]), int(reservation_id_8[i]), int(tv_port_8[i])))
