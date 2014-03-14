import sys
import re

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'loop' : 'LOOP',
   'start' : 'START',
   'while' : 'WHILE',
   'set' : 'SET',
   'and' : 'AND',
   'or' : 'OR',
   'not' : 'NOT',
   'number' : 'NUMBER_TYPE',
   'text' : 'TEXT_TYPE',
   'class' : 'CLASS'
}

tokens = [
    'NAME','NUMBER','EQ','EXCL',
    'PLUS','MINUS','TIMES','DIVIDE', 'MOD',
    'LPAREN','RPAREN', 'NL' , 'LBRACK', 'RBRACK', 
    'COMMA', 'GT', 'LT', 'EQEQ'
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

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    if(t.type=='NAME'):
        p = re.compile('[a-zA-Z_][a-zA-Z0-9_]{0, 99}')
        if(not p.match(t.value)):
            t.value = ""
    return t

# Ignored characters
t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
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
    ('right','ASSIGN'),
    ('left','COMMA'),
    )

# dictionary of names
names = { }

def p_lines(t):
    '''lines : lines statement NL
             | lines NL
             | '''

def p_statement(t):
    '''statement : start_expression
                 | loop
                 | if_statement'''


def p_start_expression(t):
    '''start_expression : expression
                        | def_variable'''

def p_opt_statement(t):
    '''opt_statement : statement
                     | '''
                 
def p_loop(t):
    '''loop : LOOP LPAREN loop_expression RPAREN LBRACK lines opt_statement RBRACK'''

def p_loop_expression(t):
    '''loop_expression : loop_expression COMMA loop_expression
                       | START start_expression
                       | WHILE expression
                       | SET expression
                       | '''

def p_if_statement(t):
    '''if_statement : IF LPAREN expression RPAREN LBRACK lines opt_statement RBRACK
                    | IF LPAREN expression RPAREN LBRACK lines opt_statement RBRACK ELSE LBRACK lines opt_statement RBRACK'''

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | NAME EQ expression %prec ASSIGN'''
#    if t[2] == '+'  : t[0] = t[1] + t[3]  
#    elif t[2] == '-': t[0] = t[1] - t[3]
#    elif t[2] == '*': t[0] = t[1] * t[3]
#    elif t[2] == '/': t[0] = t[1] / t[3]
#    elif t[2] == '%': t[0] = t[1] % t[3]

def p_expression_conditional(t):
    '''expression : expression GT expression
                  | expression GT EQ expression %prec GTEQ
                  | expression LT expression
                  | expression LT EQ expression %prec LTEQ
                  | expression EQEQ expression
                  | expression EXCL EQ expression %prec NOTEQ
                  | expression AND expression
                  | expression OR expression
                  | NOT expression %prec NOT'''
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
   
def p_def_variable(t):
    '''def_variable : var_type NAME
                    | var_type NAME EQ expression'''

def p_var_type(t):
    '''var_type : NUMBER_TYPE
                | TEXT_TYPE'''

def p_error(t):
#    print("Syntax error at '%s'" % t.value)
    print("syntax error")

import ply.yacc as yacc
yacc.yacc()

if len(sys.argv) > 1 :
    inputfile = open(sys.argv[1],'r')
    yacc.parse(inputfile.read())
