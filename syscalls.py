import math
def num_form(format, number):
	if (format == "#"):
		return str(math.floor(number))
	else:
		pieces = format.split('.', 1)
		decimalplaces = pieces[1]
		printformat = "%" + "1." + str(len(decimalplaces)) + "f"
		return printformat % number
