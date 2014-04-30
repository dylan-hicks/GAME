import math
def num_form(format, number):
	if (isinstance(format, basestring) and isinstance(number, (int, long, float, complex))):
		if (format == "#"):
			return str(math.floor(number))
		else:
			pieces = format.split('.', 1)
			decimalplaces = pieces[1]
			printformat = "%" + "1." + str(len(decimalplaces)) + "f"
			return printformat % number
	else:
		msg = (format + " must be of type text" + " and " + number + " must be of type num")
		raise TypeError(msg)
