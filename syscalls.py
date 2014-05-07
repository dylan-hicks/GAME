import matplotlib.pyplot as plt
import math
import json
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

def graph(x, y, color, style, lbl):
    
    mode = ""
    if (color == "green"):
        mode += 'g'
    elif (color == "blue"):
        mode += 'g'
    elif (color == "red"):
        mode += 'r'
    elif (color == "cyan"):
        mode += 'c'
    elif (color == "magenta"):
        mode += 'm'
    elif (color == "yellow"):
        mode += 'y'
    elif (color == "white"):
        mode += 'w'
    else:
        mode += 'k'
    
    
    if (style == "solid"):
        mode += '-'
    elif (style == "dashed"):
        mode += '--'
    elif (style == "circle"):
        mode += 'o'
    elif (style == "triangle"):
        mode += '^'
    elif (style == "x"):
        mode += 'x'
    else:
        mode += '-'


    plt.plot(x, y, mode, label= lbl)

def display():
    plt.legend(loc='upper right')
    plt.show()

def label(loc, name):
    if (loc == "x"):
        plt.xlabel(name)
    elif (loc == "y"):
        plt.ylabel(name)
    else:
        plt.title(name)

def axis(x, y):
    plt.axis(x + y)

def export_GAME(obj):
  attr_obj = get_attr_and_obj(obj)
  attributes = attr_obj['attributes']
  objects = attr_obj['objects']
  hash_obj = {}
  #iterate through attributes
  for attr in attributes:
    hash_obj[attr] = getattr(obj, attr)
  #iterate through objects
  for attr in objects:
    hash_obj[attr] = export_GAME(getattr(obj, attr))
  return hash_obj

def export_function(obj, file_name):
  hash_obj = {}
  hash_obj['GAME'] = export_GAME(obj)
  with open("{}.json".format(file_name), 'w') as outfile:
    json.dump(hash_obj, outfile)