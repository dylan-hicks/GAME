import sys
import re

reserved = { 
   'include' : 'INCLUDE',
   'if' : 'IF',
   'else' : 'ELSE',
   'loop' : 'LOOP',
   'start' : 'START',
   'while' : 'WHILE',
   'set' : 'SET',
   'and' : 'AND',
   'or' : 'OR',
   'not' : 'NOT',
   'number' : 'NUM_TYPE',
   'text' : 'TEXT_TYPE',
   'bool' : 'BOOL_TYPE',
   'class' : 'CLASS',
   'break' : 'BREAK',
   'continue' : 'CONTINUE',
   'class' : 'CLASS',
   'extends' : 'EXTENDS',
   'function' : 'FUNCTION',
   'return' : 'RETURN',
   'foreach' : 'FOREACH',
   'in' : 'IN',
   'geteach' : 'GETEACH',
   'where' : 'WHERE',
   'load' : 'LOAD',
   'export' : 'EXPORT',
   'from' : 'FROM',
   'to' : 'TO',
   'new' : 'NEW',
   'list' : 'LIST',
   'false' : 'FALSE',
   'true' : 'TRUE'
}

tokens = [
    'ID','NUM','EQ','EXCL', 'TXT',
    'PLUS','MINUS','TIMES','DIVIDE', 'MOD',
    'LPAREN','RPAREN', 'NL' , 'LBRACK', 'RBRACK', 
    'COMMA', 'GT', 'LT', 'EQEQ' , 'DOT' , 'LSQ' , 'RSQ'
    ] + list(reserved.values())

# Tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MOD     = r'%'
t_EQEQ    = r'=='
t_EQ      = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NL      = r'\n+'
t_LBRACK  = r'\{'
t_RBRACK  = r'\}'
t_COMMA   = r'\,'
t_GT      = r'>'
t_LT      = r'<'
t_EXCL    = r'!'
t_DOT     = r'\.'
t_LSQ     = r'\['
t_RSQ     = r'\]'
t_TXT     = r'"[^"]*"'

def t_NUM(t):
    r'\d+\.?d*'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    print(t.value)
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
# TODO: check length of ID
#    if(t.type=='ID'):
#        p = re.compile('[a-zA-Z_][a-zA-Z0-9_]{0, 99}')
#        if(not p.match(t.value)):
#            t.value = ""
    print(t.type)
    return t

# Ignored characters
t_ignore = " \t"

def t_COMMENT(t):
    r'\#.*\n'
    t.type = 'NL'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules (lowest to highest)

precedence = (
    ('left','NL'),
    ('left','COMMA'),
    ('right','EQ'),
    ('left','OR'),
    ('left','AND'),
    ('left','EQEQ','NOTEQ'),
    ('left','GT','LT','LTEQ','GTEQ'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE', 'MOD'),
    ('left','UMINUS','NOT'),
    ('left','DOT'),
    )

# dictionary of names
names = { }

# defining the Node class

class program_lines_node(object):

    def __init__(self, children): 
        self.children = children
             
    def __str__(self):
        s = ""
        s += children[0].__str__() + " " + children[1].__str__()
        
#        print s # TESTING
        return s

class constant_node(object):

    def __init__(self, children, value=None): 

        
        self.children = children
        if value:
            self.value = value

    def __str__(self):
        s = ""
        if value:
            s += value #CHECK IF LEX CONVERTS THIS AUTOMATICALLY
        else:
            S += '{' + children[0].__str__() + '}' # can we just use LBRACK instead?
        return s

class constant_list_node(object):
    def __init__(self, children):
        
        self.children = children

    def __str__(self):
        s = ""
        if len(children) == 2:
            s += children[0].__str__() + ', ' + children[1].__str__()
        else: 
            s += children[0].__str__()
        return s

class var_type_node(object):

    def __init__(self, children, value=None): 
        
        self.children = children
        if value:
            self.value = value

    def __str__(self):
        s = ""
        if value:
            s += value #CHECK IF LEX CONVERTS THIS AUTOMATICALLY
        else:
            s += 'list(' + children[0].__str__() + ')'  
        return s

class mul_variable_def_node(object):

    def __init__(self, children):
        self.children = children
        
    def __str__(self):
        s = ""
        for x in children:
            s += x.__str__() + " "
        
        s += "\n"
        return s

class variable_def_node(object):

    def __init__(self, children, value=None):
        self.children = children
        if value: 
            self.value = value

    def __str__(self):
        s = ""

        if len(children) == 1:
            s += children[0].__str__() + " " + value # what does ID evaluate to? 
        elif len(children) == 2 and value:
            s += children[0].__str__() + " " + value + " = new " + children[1].__str__() # same question
        elif len(children) == 2: 
            s += children[0].__str__() + children[1].__str__()
        else:
            s += children[0].__str__() + " " + value + " = new " + children[1].__str__() + "{\n" + children[2].__str__() + "}"
            
        return s;

class obj_expression_node(object):

    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value

    def __str__(self):
        s = ""

        if len(children) == 1:
            s += children[0].__str__() + "." + value
        else: 
            s += value

        return s

class assignment_node(object):

    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value

    def __str__(self):
        s = ""

        s += value + " = " + children[0].__str__()

        return s

class expression_node(object): # if this messes up, look for prec as the cause

    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value

    def __str__(self):
        s = ""

        if len(children) == 1 and value and len(value) == 1:
            s += value[0] + " " + children[0].__str__() # will value be NOT?
        elif len(children) == 1 and value and len(value) == 3:
            s+= value[0] + " " + value[1]+ " " + children[0].__str__()+ " " + value[2]
        elif len(children) == 1: 
            s += children[0].__str__()
        elif len(children) == 2 and value and len(value) == 1:
            s += children[0].__str__() + " " + value[0] + " " + children[1].__str__()
        elif len(children) == 2 and value and len(value) == 2:
            s += children[0].__str__() + " " + value[0] + " " + value[1] + " " + children[1].__str__()
        elif len(children) == 2 and value and len(value) == 4:
            s += children[0].__str__() + "." + value[1] + "(" + children[1].__str__() + ")"
        else:
            s += children[0].__str__() + "[" + children[1].__str__() + "]"

        return s

class import_lines_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value

    def __str__(self):
        s = ""
        if value: 
            s += children[0].__str__() + " import " + value + "\n"
        else:
            s += children[0].__str__() + "\n"

        return s


class lines_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value

    def __str__(self):
        s = ""
        if len(children) == 0:
            s = ""
        elif len(children) == 1:
            s += children[0].__str__() + "\n"
        else:
            s += children[0].__str__() + " " + children[1].__str__() + "\n"
        
        print s # TESTING
        return s

class class_lines_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value

    def __str__(self):
        s = ""
        if len(children) == 0:
            s = ""
        elif len(children) == 1:
            s += children[0].__str__() + "\n"
        else:
            s += children[0].__str__() + " " + children[1].__str__() + "\n"

        return s

class function_lines_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value

    def __str__(self):
        s = ""
        if len(children) == 0:
            s = ""
        elif len(children) == 1:
            s += children[0].__str__() + "\n"
        else:
            s += children[0].__str__() + " " + children[1].__str__() + "\n"
            
        print s # TESTING
        return s

class statement_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""
        if len(children) == 0:
            s += value
        elif len(children) == 1:
            if value:
                s += value + "(" + children[0].__str__() + ")"
            else:
                s += children[0].__str__()
        elif len(children) == 2:
            s += children[0].__str__() + "." + value + "(" + children[1].__str__() + ")"

        return s

class class_def_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""
        if len(value) == 1:
            s += "class " + value + "{\n" + children[0].__str__() + "}"
        else:
            s += "class " + value + " extends" + value[0] + "{\n" + children[0].__str__() + "}" 

        return s

class function_def_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""
        
        if len(children) == 2:
            s += "function " + value + "(" + children[0].__str__() + "){\n" + children[1].__str__() + "}"
        else:
            s += children[0].__str__() + " function " + value + "(" + children[1].__str__() + "){\n" + children[2].__str__() + "return " + children[3].__str__() + "\n}"

        print s # TESTING
        return s

class function_args_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""
        
        if len(children) == 0:
            s = ""
        else:
            s += children[0].__str__()

        return s

class function_arg_values_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""
        
        if len(children) == 1: 
            s += children[0].__str__() + value
        else:
            s += children[0].__str__() + "," + children[1].__str__()

        return s

class function_run_args_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""
        
        if len(children) == 0:
            s = ""
        else:
            s += children[0].__str__()

        return s


class function_run_arg_values_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""
        
        if len(children) == 1:
            s += children[0].__str__()
        else:
            s += children[0].__str__() + "," + children[1].__str__()

        return s


class loop_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""
        
        if len(children) == 2:
            if value:
                s += "foreach (" + children[0].__str__() + value[0] + " in " + value[1] + "){\n" + children[1].__str__() + "}"
            else:
                s += "loop (" + children[0].__str__() + "){\n" + children[1].__str__() + "}"
        else:
            s += children[0].__str__() + value[0] + " = geteach (" + children[1].__str__() + value[0] + " in " + value[1] + " where " + children[2].__str__() + ")"

        return s

class loop_expression_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""

        if len(children) == 0:
            s = ""
        elif len(children) == 1:
            s += children[0].__str__()
        else:
            s += children[0].__str__() + "," + children[1].__str__()

        return s

class loop_expression_values_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""

        s += value + children[0].__str__()
        return s

class if_statement_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""
        if len(children) == 2:
            s += "if (" + children[0].__str__() + "){\n" + children[1].__str__() + "}"
        else:
            s += "if (" + children[0].__str__() + "){\n" + children[1].__str__() + "} else {\n" + children[2].__str__() + "}"

        return s

class data_statement_node:
    def __init__(self, children, value=None):
        self.children = children
        if value:
            self.value = value
    
    def __str__(self):
        s = ""

        s += value[0] + " " + children[0].__str__() + value[1] + " " + children[1].__str__()

        return s

# grammar stuff below

def p_program_lines(p):
    '''program_lines : include_lines lines'''
    p[0] = program_lines_node([p[1], p[2]])
    print p[0] # TESTING

def p_include_lines(p):
    '''include_lines : include_lines INCLUDE TXT NL
                     | include_lines NL
                     | '''
    if len(p) == 3:
        p[0] = import_lines_node([p[1]])
    elif len(p) == 1:
        p[0] = class_lines_node([ ])
    else:
        p[0] = import_lines_node([p[1]], p[3].value)

def p_lines(p):
    '''lines : lines class_def NL
             | lines function_def NL
             | lines NL
             | '''
    print('lines')
    if len(p) == 3:
        p[0] = lines_node([p[1]])
    elif len(p) == 1:
        p[0] = class_lines_node([ ])
    else:
        p[0] = lines_node([p[1], p[2]])


def p_class_lines(p):
    '''class_lines : class_lines function_def NL
                   | class_lines variable_def NL
                   | class_lines NL
                   | '''
    print('class lines')
    if len(p) == 3:
        p[0] = class_lines_node([p[1]])
    elif len(p) == 1:
        p[0] = class_lines_node([ ])
    else:
        p[0] = class_lines_node([p[1], p[2]])

def p_function_lines(p):
    '''function_lines : function_lines statement NL
                      | function_lines NL
                      | '''
    print('function lines')
    if len(p) == 3:
        p[0] = function_lines_node([p[1]])
    elif len(p) == 1:
        p[0] = class_lines_node([ ])
    else:
        p[0] = function_lines_node([p[1], p[2]])
    

def p_statement(p):
    '''statement : variable_def
                 | assignment
                 | loop
                 | if_statement
                 | data_statement
                 | obj_expression DOT ID LPAREN function_run_args RPAREN
                 | ID LPAREN function_run_args RPAREN
                 | BREAK
                 | CONTINUE'''
    print('statement')
    if len(p) == 2:
        if p[1].value == "BREAK" or p[1].value == "CONTINUE":
            p[0] = statement_node([ ], [p[1]])
        else:
            p[0] = statement_node([p[1]])
    elif len(p) == 5:
        p[0] = statement_node([p[3]], p[1])
    else:
        p[0] = statement_node([p[1], p[5]], p[3])


def p_class_def(p):
    '''class_def : CLASS ID LBRACK NL class_lines RBRACK
                 | CLASS ID EXTENDS ID LBRACK NL class_lines RBRACK'''
    print('class def')
    if len(p) == 7:
        p[0] = class_def_node([p[5]], [p[2]])
    else:
        p[0] = class_def_node([p[5]], [p[2], p[4]])


def p_function_def(p):
    '''function_def : FUNCTION ID LPAREN function_args RPAREN LBRACK NL function_lines RBRACK
                    | var_type FUNCTION ID LPAREN function_args RPAREN LBRACK NL function_lines RETURN expression NL RBRACK'''
    print('function def')
    if len(p) == 10:
        p[0] = function_def_node([p[4], p[8]], p[2])
    else:
        p[0] = funciton_def_node([p[1], p[5], p[9], p[11]], p[3])

def p_function_args(p):
    '''function_args : function_arg_values
                     | '''
    print('function args')
    if len(p) == 1:
        p[0] = function_args_node([ ])
    else:
        p[0] = function_args_node([p[1]])

def p_function_arg_values(p):
    '''function_arg_values : function_arg_values COMMA function_arg_values
                           | var_type ID'''
    print('function arg values')
    if len(p) == 3:
        p[0] = function_arg_values_node([p[1]], p[2])
    else:
        p[0] = function_arg_values_node([p[1], p[3]])

def p_function_run_args(p):
    '''function_run_args : function_run_arg_values
                         | '''
    print('function run args')
    if len(p) == 1:
        p[0] = function_run_args_node([ ])
    else:
        p[0] = function_run_args_node([p[1]])

def p_function_run_arg_values(p):
    '''function_run_arg_values : function_run_arg_values COMMA function_run_arg_values
                               | expression'''
    print('function run arg values')
    if len(p) == 2:
        p[0] = function_run_arg_values_node([p[1]])
    else:
        p[0] = function_run_arg_values_node([p[1], p[3]])

def p_loop(p):
    '''loop : LOOP LPAREN loop_expression RPAREN LBRACK NL function_lines RBRACK
            | FOREACH LPAREN var_type ID IN ID RPAREN LBRACK NL function_lines RBRACK
            | var_type ID EQ GETEACH LPAREN var_type ID IN ID WHERE expression RPAREN'''
    print('loop')
    if len(p) == 9:
        p[0] = loop_node([p[3], p[7]])
    elif len(p) == 12:
        p[0] = loop_node([p[3], p[10]], [p[4], p[6]])
    else:
        p[0] = loop_node([p[1], p[6], p[11]], [p[2], p[7], p[9]])

def p_loop_expression(p):
    '''loop_expression : loop_expression COMMA loop_expression
                       | loop_expression_values
                       | '''
    print('loop expression')
    if len(p) == 1:
        p[0] = loop_expression_node([ ])
    elif len(p) == 2:
        p[0] = loop_expression_node([p[1]])
    else:
        p[0] = loop_expression_node([p[1], p[3]])
        

def p_loop_expression_values(p):
    '''loop_expression_values : START variable_def
                              | WHILE expression
                              | SET assignment'''
    print('loop expression values')
    p[0] = loop_expression_values_node([p[2]], p[1].value)

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACK NL function_lines RBRACK
                    | IF LPAREN expression RPAREN LBRACK NL function_lines RBRACK ELSE LBRACK NL function_lines RBRACK'''
    print('if statement')
    if len(p) == 9:
        p[0] = if_statement_node([p[3], p[7]])
    else:
        p[0] = if_statement_node([p[3], p[7], p[12]])

def p_data_statement(p):
    '''data_statement : LOAD expression FROM expression
                      | EXPORT expression TO expression'''
    print('data statement')
    p[0] = data_statement_node([p[2], p[4]], [p[1], p[3]])

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | expression GT expression
                  | expression GT EQ expression %prec GTEQ
                  | expression LT expression
                  | expression LT EQ expression %prec LTEQ
                  | expression EQEQ expression
                  | expression EXCL EQ expression %prec NOTEQ
                  | expression AND expression
                  | expression OR expression
                  | NOT expression 
                  | MINUS expression %prec UMINUS
                  | constant
                  | assignment
                  | obj_expression DOT ID LPAREN function_run_args RPAREN
                  | ID LPAREN function_run_args RPAREN
                  | obj_expression LSQ expression RSQ
                  | obj_expression'''
    print('expression')
    if len(p) == 2:
        p[0] = expression_node([p[1]])
    elif len(p) == 3:
        p[0] = expression_node([p[2]], [p[1].value])
    elif len(p) == 4:
        p[0] = expression_node([p[1], p[3]], [p[2].value])
    elif len(p) == 5:
        if p[3] == "=":
            p[0] = expression_node([p[1], p[4]], [p[2].value, p[3].value])
        elif p[1] == ID: # ID evaluates to?
            p[0] = expression_node([p[3]], [p[1].value, p[2].value, p[4].value])
        else:
            p[0] = expression_node([p[1], p[3]])
    else:
        p[0] = expression_node([p[1], p[5]], [p[2].value, p[3].value, p[4].value, p[6].value])
            

def p_assignment(p):
    '''assignment : ID EQ expression'''
    print('assignment')
    p[0] = assignment_node([p[3]], p[1].value)

def p_obj_expression(p):
    '''obj_expression : obj_expression DOT ID
                      | ID'''
    print('obj expression')
    if len(p) == 2:
        p[0] = obj_expression_node([ ], p[1].value)
    else:
        p[0] = obj_expression_node([p[1]], p[3].value)

def p_variable_def(p):
    '''variable_def : var_type ID
                    | var_type assignment
                    | var_type ID EQ NEW var_type
                    | var_type ID EQ NEW var_type LBRACK NL mul_variable_def RBRACK'''
    print('variable def')
    if len(p) == 3:
        if p[2].type == 'ID': #NOT SURE WHAT ID EVALUATES TO
            p[0] = variable_def_node([p[1]], p[2].value)
        else:
            p[0] = variable_def_node([p[1], p[2]])
    elif len(p) == 6:
        p[0] = variable_def_node([p[1], p[5]], p[2].value)
    else:
        p[0] = variable_def_node([p[1], p[5], p[8]], p[2].value)


def p_mul_variable_def(p):
    '''mul_variable_def : mul_variable_def variable_def NL
                        | variable_def NL'''
    print('mul variable def')
    if len(p) == 3:
        p[0] = mul_variable_def_node([p[1], p[2]])
    else:
        p[0] = mul_variable_def_node([p[1]])

def p_var_type(p):
    '''var_type : TEXT_TYPE
                | NUM_TYPE
                | BOOL_TYPE
                | ID
                | LIST LPAREN var_type RPAREN'''
    print('var type')
    if len(p) == 4:
        p[0] = var_type_node([p[3]])
    else:
        p[0] = var_type_node([ ], p[1].value)

def p_constant(p):
    '''constant : LBRACK constant_list RBRACK
                | NUM
                | TXT
                | FALSE
                | TRUE'''            
    print('constant')
    if len(p) == 4:
        p[0] = constant_node([p[2]])
    else: 
        p[0] = constant_node([ ], p[1])

def p_constant_list(p):
    '''constant_list : constant_list COMMA constant_list
                     | constant'''
    print('constant list')
    if len(p) == 4:
        p[0] = constant_list_node([p[1], p[2]])
    else:
        p[0] = constant_list_node([p[1]])

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc

yacc.yacc()

if len(sys.argv) > 1 :
    inputfile = open(sys.argv[1],'r')
    yacc.parse(inputfile.read())
