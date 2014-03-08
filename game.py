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
    'PLUS','MINUS','TIMES','DIVIDE', 'MOD', 'EQUALS',
    'LPAREN','RPAREN', 'ID' , 'NL' , 'LBRACK', 'RBRACK', 
    'COMMA', 'GT', 'LT', 'EXCL'
    ] + list(reserved.values())

#reserved = {
#   'if' : 'IF',
#   'then' : 'THEN',
#   'else' : 'ELSE',
#   'while' : 'WHILE',
#  ...
#}
#tokens = ['LPAREN','RPAREN',...,'ID'] + list(reserved.values())
# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MOD     = r'%'
t_EQUALS  = r'=='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]{0, 99}'
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

# Ignored characters
t_ignore = " \t"

#def t_newline(t):
#    r'\n+'
#    t.lexer.lineno += t.value.count("\n")

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

if __name__ == '__main__':
    lex.runmain()

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE', 'MOD'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_lines(t):
    '''lines : lines statement NL
             | lines NL
             | lines EOF
             | '''

def p_statement(t):
    '''statement : expression
                 | loop
                 | matched_if_statement
                 | open_if_statement'''
                 
def p_loop(t):
    '''loop : LOOP LPAREN loop_expression RPAREN newlines LBRACK lines RBRACK'''

def p_newlines(t):
    '''newlines : newlines NL
                | '''

def p_loopexpression(t):
    '''loopexpression : loop_expression COMMA loop_expression
                      | start LPAREN expression RPAREN
                      | while LPAREN expression RPAREN
                      | set LPAREN expression RPAREN
                      | '''

def p_matched_statement(t):
    '''matched_statement : IF LPAREN expression RPAREN LBRACK matched_statement RBRACK ELSE LBRACK matched_statement RBRACK 
                         | lines
    '''

def p_open_statement(t):
    '''open_statement    : IF LPAREN expression RPAREN LBRACK     statement RBRACK
                         | IF LPAREN expression RPAREN LBRACK matched_statement RBRACK ELSE LBRACK open_statement RBRACK
    '''
 
def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]
    elif t[2] == '%': t[0] = t[1] % t[3]

def p_expression_conditional(t):
    '''expression : conditional
                  | num
                  | LPAREN expression RPAREN'''
    
def p_conditional(t):
   '''conditional : expression GT expression
                  | expression GT EQ expression
                  | expression LT expression
                  | expression LT EQ expression
                  | expression EQ EQ expression
                  | expression EXCL EQ expression
                  | expression AND expression
                  | expression OR expression
                  | NOT expression'''

    if t[2] == '>'  : t[0] = t[1] > t[3]
    elif t[2] == '<': t[0] = t[1] < t[3]
    elif t[2] == '>=': t[0] = t[1] >= t[4]
    elif t[2] == '<=': t[0] = t[1] <= t[4]
    elif t[2] == '==': t[0] = t[1] == t[4]
    elif t[2] == 'and': t[0] = t[1] and t[3]
    elif t[2] == 'or' : t[0] = t[1] or t[3]
    elif t[2] == 'not' : t[0] = not t[1]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0
        
def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = """2+2
        loop() { }
        """
#       s = raw_input('calc > ')
    except EOFError:
        break
    yacc.parse(s)
