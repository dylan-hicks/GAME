import sys

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'loop' : 'LOOP',
   'start' : 'START',
   'while' : 'WHILE',
   'set' : 'SET',
   'and' : 'AND',
   'or' : 'OR',
   'not' : 'NOT'
}

tokens = [
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE', 'MOD',
    'LPAREN','RPAREN', 'NL' , 'LBRACK', 'RBRACK', 
    'COMMA', 'GT', 'LT', 'NOTEQ' , 'GTEQ', 'LTEQ',
    'EQEQ',
    ] + list(reserved.values())

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MOD     = r'%'
t_EQEQ    = r'=='
#t_EQ      = r'='
t_GTEQ    = r'>='
t_LTEQ    = r'<='
t_NOTEQ   = r'!='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]{0, 99}'
t_NL      = r'\n+'
t_LBRACK  = r'\{'
t_RBRACK  = r'\}'
t_COMMA   = r'\,'
t_GT      = r'>'
t_LT      = r'<'
# should be a better way to do this
t_IF      = r'if' 
t_ELSE    = r'else'
t_LOOP    = r'loop'
t_START   = r'start'
t_WHILE   = r'while'
t_SET     = r'set'
t_AND     = r'and'
t_OR      = r'or'
t_NOT     = r'not'


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
###
#This code is to differentiate between variables and reserved words
#
#def t_ID(t):
#    r'[a-zA-Z_][a-zA-Z_0-9]*'
#    t.type = reserved.get(t.value,'ID')    # Check for reserved words
#    return t
###

# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules (lowest to highest)

precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','EQEQ','NOTEQ'),
    ('left','GT','LT','LTEQ','GTEQ'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE', 'MOD'),
    ('right','UMINUS','NOT'),
    ('left','COMMA'),
    )

# dictionary of names
names = { }

def p_lines(t):
    '''lines : lines statement NL
             | lines NL
             | '''

def p_statement(t):
    '''statement : expression
                 | loop
                 | if_statement'''

def p_opt_statement(t):
    '''opt_statement : statement
                     | '''
                 
def p_loop(t):
    '''loop : LOOP LPAREN loop_expression RPAREN LBRACK lines opt_statement RBRACK'''

#def p_newlines(t):
#    '''newlines : newlines NL
#                | '''

def p_loop_expression(t):
    '''loop_expression : loop_expression COMMA loop_expression
                       | START LPAREN expression RPAREN
                       | WHILE LPAREN expression RPAREN
                       | SET LPAREN expression RPAREN
                       | '''

def p_if_statement(t):
    '''if_statement : IF LPAREN expression RPAREN LBRACK lines opt_statement RBRACK
                    | IF LPAREN expression RPAREN LBRACK lines opt_statement RBRACK ELSE LBRACK lines opt_statement RBRACK'''

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression'''
#    if t[2] == '+'  : t[0] = t[1] + t[3]  
#    elif t[2] == '-': t[0] = t[1] - t[3]
#    elif t[2] == '*': t[0] = t[1] * t[3]
#    elif t[2] == '/': t[0] = t[1] / t[3]
#    elif t[2] == '%': t[0] = t[1] % t[3]

def p_expression_conditional(t):
    '''expression : expression GT expression
                  | expression GTEQ expression
                  | expression LT expression
                  | expression LTEQ expression
                  | expression EQEQ expression
                  | expression NOTEQ expression
                  | expression AND expression
                  | expression OR expression
                  | NOT expression'''
#    if t[2] == '>'  : t[0] = t[1] > t[3]
#    elif t[2] == '<': t[0] = t[1] < t[3]
#    elif t[2] == '>=': t[0] = t[1] >= t[4]
#    elif t[2] == '<=': t[0] = t[1] <= t[4]
#    elif t[2] == '==': t[0] = t[1] == t[4]
#    elif t[2] == 'and': t[0] = t[1] and t[3]
#    elif t[2] == 'or' : t[0] = t[1] or t[3]
#    elif t[2] == 'not' : t[0] = not t[1]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
#    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
#    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
#    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
#    try:
#        t[0] = names[t[1]]
#    except LookupError:
#        print("Undefined name '%s'" % t[1])
#        t[0] = 0
   
def p_error(t):
#    print("Syntax error at '%s'" % t.value)
    print("syntax error")

import ply.yacc as yacc
yacc.yacc()

if len(sys.argv) > 1 :
    inputfile = open(sys.argv[1],'r')
    yacc.parse(inputfile.read())
