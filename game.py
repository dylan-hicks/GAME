import sys
import re

reserved = { 
   'import' : 'IMPORT',
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
    if(t.type=='ID'):
        p = re.compile('[a-zA-Z_][a-zA-Z0-9_]{0, 99}')
        if(not p.match(t.value)):
            t.value = ""
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
    ('left','DOT'),
    ('left','UMINUS','NOT'),
    ('left','TIMES','DIVIDE', 'MOD'),
    ('left','PLUS','MINUS'),
    ('left','GT','LT','LTEQ','GTEQ'),
    ('left','EQEQ','NOTEQ'),
    ('left','AND'),
    ('left','OR'),
    ('right','EQ'),
    ('left','COMMA'),    
    ('left','NL'),
    )

# dictionary of names
names = { }

def p_program_lines(t):
    '''program_lines : import_lines lines'''

def p_import_lines(t):
    '''import_lines : import_lines IMPORT TXT NL
                    | import_lines NL
                    | '''

def p_lines(t):
    '''lines : lines class_def NL
             | lines function_def NL
             | lines NL
             | '''
    print('lines')

def p_class_lines(t):
    '''class_lines : class_lines function_def NL
                   | class_lines variable_def NL
                   | class_lines NL
                   | '''
    print('class lines')

def p_function_lines(t):
    '''function_lines : function_lines statement NL
                      | function_lines NL
                      | '''
    print('function lines')

def p_statement(t):
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

def p_class_def(t):
    '''class_def : CLASS ID LBRACK NL class_lines RBRACK
                 | CLASS ID EXTENDS ID LBRACK NL class_lines RBRACK'''
    print('class def')

def p_function_def(t):
    '''function_def : FUNCTION ID LPAREN function_args RPAREN LBRACK NL function_lines RBRACK
                    | var_type FUNCTION ID LPAREN function_args RPAREN LBRACK NL function_lines RETURN expression NL RBRACK'''
    print('function def')

def p_function_args(t):
    '''function_args : function_arg_values
                     | '''
    print('function args')

def p_function_arg_values(t):
    '''function_arg_values : function_arg_values COMMA function_arg_values
                           | var_type ID'''
    print('function arg values')

def p_function_run_args(t):
    '''function_run_args : function_run_arg_values
                         | '''
    print('function run args')

def p_function_run_arg_values(t):
    '''function_run_arg_values : function_run_arg_values COMMA function_run_arg_values
                               | expression'''
    print('function run arg values')

def p_loop(t):
    '''loop : LOOP LPAREN loop_expression RPAREN LBRACK NL function_lines RBRACK
            | FOREACH LPAREN var_type ID IN ID RPAREN LBRACK NL function_lines RBRACK
            | var_type ID EQ GETEACH LPAREN var_type ID IN ID WHERE expression RPAREN'''
    print('loop')

def p_loop_expression(t):
    '''loop_expression : loop_expression COMMA loop_expression
                       | loop_expression_values
                       | '''
    print('loop expression')

def p_loop_expression_values(t):
    '''loop_expression_values : START variable_def
                              | WHILE expression
                              | SET assignment'''
    print('loop expression values')

def p_if_statement(t):
    '''if_statement : IF LPAREN expression RPAREN LBRACK NL function_lines RBRACK
                    | IF LPAREN expression RPAREN LBRACK NL function_lines RBRACK ELSE LBRACK NL function_lines RBRACK'''
    print('if statement')

def p_data_statement(t):
    '''data_statement : LOAD expression FROM expression
                      | EXPORT expression TO expression'''
    print('data statement')

def p_expression(t):
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

def p_assignment(t):
    '''assignment : ID EQ expression'''
    print('assignment')

def p_obj_expression(t):
    '''obj_expression : obj_expression DOT ID
                      | ID'''
    print('obj expression')

def p_variable_def(t):
    '''variable_def : var_type ID
                    | var_type assignment
                    | var_type ID EQ NEW var_type
                    | var_type ID EQ NEW var_type LBRACK NL mul_variable_def RBRACK'''
    print('variable def')

def p_mul_variable_def(t):
    '''mul_variable_def : mul_variable_def variable_def NL
                        | variable_def NL'''
    print('mul variable def')

def p_var_type(t):
    '''var_type : TEXT_TYPE
                | NUM_TYPE
                | BOOL_TYPE
                | ID
                | LIST LPAREN var_type RPAREN'''
    print('var type')

def p_constant(t):
    '''constant : LBRACK constant_list RBRACK
                | NUM
                | TXT
                | FALSE
                | TRUE'''            
    print('constant')

def p_constant_list(t):
    '''constant_list : constant_list COMMA constant_list
                     | constant'''
    print('constant list')

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc

yacc.yacc()

if len(sys.argv) > 1 :
    inputfile = open(sys.argv[1],'r')
    yacc.parse(inputfile.read())
