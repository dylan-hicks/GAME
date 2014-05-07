import math
def num_form(format, number):
	if (format == "#"):
		return str(math.floor(number))
	else:
		pieces = format.split('.', 1)
		decimalplaces = pieces[1]
		printformat = "%" + "1." + str(len(decimalplaces)) + "f"
		return printformat % number

type_boolean = False
type_str = "test"
type_float = 10.0
type_list = []

#ele is the string of the attribute
#attr is the actual attribute
def is_primitive(ele, attr):
  is_prim = False
  if attr.__class__ == type_boolean.__class__:
    is_prim = True
  elif attr.__class__ == type_str.__class__:
    is_prim = True
  elif attr.__class__ == type_float.__class__:
    is_prim = True
  elif attr.__class__ == type_list.__class__:
    is_prim = True
  if id_has_underscore_tag(ele):
    is_prim = False
  return is_prim

def id_has_underscore_tag(ele_name):
  has_tag = True
  #attribute name is 4 or less so can't be underscore attr
  if len(ele_name) <= 4:
    has_tag = False
  elif ele_name[:2] != "__":
    has_tag = False
  return has_tag

def get_attr_and_obj(obj):
  attributes = []
  objects = []
  for ele in dir(obj):
    actual = getattr(obj, ele)
    #is method, don't add
    if hasattr(actual, '__call__'):
      continue
    #attr is autoattribute with __
    elif id_has_underscore_tag(ele):
      continue
    #if is primitive attribute, we add to attributes
    elif is_primitive(ele, actual):
      attributes.append(ele)
    #if is object attribute, we add to objects
    else:
      objects.append(ele)
  attr_obj = {}
  attr_obj['attributes'] = attributes
  attr_obj['objects'] = objects
  return attr_obj