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
   'inherits' : 'INHERITS',
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
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
# TODO check token length
#    if(t.type=='ID'):
#        p = re.compile('[a-zA-Z_][a-zA-Z0-9_]{0, 99}')
#        if(not p.match(t.value)):
#            t.value = ""
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

        
def p_program_lines(t):
    '''program_lines : include_lines lines'''
    print('program_lines(' + t[1] + ',' + t[2] + ')')

def p_include_lines(t):
    '''include_lines : include_lines INCLUDE TXT NL
                     | include_lines NL
                     | '''
    if len(t)==5:
        t[0] = 'include_lines(' + t[1] + ',' + t[3] + ')'
    elif len(t)==3:
        t[0] = 'include_lines(' + t[1] + ')'
    else:
        t[0] = 'include_lines()'

def p_lines(t):
    '''lines : lines class_def NL
             | lines function_def NL
             | lines NL
             | '''
    if len(t)==4:
        t[0] = 'lines(' + t[1] + ',' + t[2] + ')'
    elif len(t)==2:
        t[0] = 'lines(' + t[1] + ')'
    else:
        t[0] = 'lines()'

def p_class_lines(t):
    '''class_lines : class_lines function_def NL
                   | class_lines variable_def NL
                   | class_lines NL
                   | '''
    if len(t)==4:
        t[0] = 'class_lines(' + t[1] + ',' + t[2] + ')'
    elif len(t)==3:
        t[0] = 'class_lines(' + t[1] + ')'
    else:
        t[0] = 'class_lines()'

def p_function_lines(t):
    '''function_lines : function_lines statement NL
                      | function_lines NL
                      | '''
    if len(t)==1:
        t[0] = 'function_lines()'
    elif len(t)==3:
        t[0] = 'function_lines(' + t[1] + ')'
    else:
        t[0] = 'function_lines(' + t[1] + ',' + t[2] + ')'

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
    if len(t)==2:
        t[0] = 'statement(' + t[1] + ')'
    elif len(t)==5:
        t[0] = 'statement(' + t[1] + ',' + t[3] + ')'
    elif len(t)==7:
        t[0] = 'statement(' + t[1] + ',' + t[3] + ')'
    else:
        t[0] = 'statement(' + t[1] + ',' + t[3] + ',' + t[5] + ')'

def p_class_def(t):
    '''class_def : CLASS ID LBRACK NL class_lines RBRACK
                 | CLASS ID INHERITS ID LBRACK NL class_lines RBRACK'''
    if len(t)==7:
        t[0] = 'class_def(' + t[2] + ',' + t[5] + ')'
    else:
        t[0] = 'class_def(' + t[2] + ',' + t[4] + ',' + t[7] + ')' 

def p_function_def(t):
    '''function_def : FUNCTION ID LPAREN function_args RPAREN LBRACK NL function_lines RBRACK
                    | var_type FUNCTION ID LPAREN function_args RPAREN LBRACK NL function_lines RETURN expression NL RBRACK'''
    if len(t)==10:
        t[0] = 'function_def(' + t[2] + ',' + t[4] + ',' + t[8] + ')'
    else:
        t[0] = 'function_def(' + t[1] + ',' + t[3] + ',' + t[5] + ',' + t[9] + t[11] + ')'

def p_function_args(t):
    '''function_args : function_arg_values
                     | '''
    if len(t)==1:
        t[0] = 'function_args()'
    else:
        t[0] = 'function_args(' + t[1] + ')'

def p_function_arg_values(t):
    '''function_arg_values : function_arg_values COMMA function_arg_values
                           | var_type ID'''
    if len(t)==3:
        t[0] = 'function_arg_values(' + t[1] + ',' + t[2] + ')'
    else:
        t[0] = 'function_arg_values(' + t[1] + ',' + t[3] + ')'

def p_function_run_args(t):
    '''function_run_args : function_run_arg_values
                         | '''
    if len(t)==1:
        t[0] = 'function_run_args()'
    else:
        t[0] = 'function_run_args(' + t[1] + ')'

def p_function_run_arg_values(t):
    '''function_run_arg_values : function_run_arg_values COMMA function_run_arg_values
                               | expression'''
    if len(t)==2:
        t[0] = 'function_run_arg_values(' + t[1] + ')'
    else:
        t[0] = 'function_run_arg_values(' + t[1] + ',' + t[3] + ')'

def p_loop(t):
    '''loop : LOOP LPAREN loop_expression RPAREN LBRACK NL function_lines RBRACK
            | FOREACH LPAREN var_type ID IN ID RPAREN LBRACK NL function_lines RBRACK
            | var_type ID EQ GETEACH LPAREN var_type ID IN ID WHERE expression RPAREN'''
    if len(t)==9:
        t[0] = 'loop(' + t[3] + ',' + t[7] + ')'
    elif len(t)==12:
        t[0] = 'loop(' + t[3] + ',' + t[4] + ',' + t[6] + ',' + t[10] + ')'
    else:    
        t[0] = 'loop(' + t[1] + ',' + t[2] + ',' + t[6] + ',' + t[7] + ',' + t[9] + ',' + t[11] + ')'

def p_loop_expression(t):
    '''loop_expression : loop_expression COMMA loop_expression
                       | loop_expression_values
                       | '''
    if len(t)==4:
        t[0] = 'loop_expression(' + t[1] + ',' + t[3] + ')'
    elif len(t)==2:
        t[0] = 'loop_expression(' + t[1] + ')'
    else:
        t[0] = 'loop_expression()'

def p_loop_expression_values(t):
    '''loop_expression_values : START variable_def
                              | WHILE expression
                              | SET assignment'''
    t[0] = 'loop_expression_values(' + t[2] + ')'

def p_if_statement(t):
    '''if_statement : IF LPAREN expression RPAREN LBRACK NL function_lines RBRACK
                    | IF LPAREN expression RPAREN LBRACK NL function_lines RBRACK ELSE LBRACK NL function_lines RBRACK'''
    if len(t)==9:
        t[0] = 'if_statement(' + t[3] + ',' + t[7] + ')'
    else:
        t[0] = 'if_statement(' + t[3] + ',' + t[7] + ',' + t[12] + ')'

def p_data_statement(t):
    '''data_statement : data_statement_load
                      | data_statement_save'''
    t[0] = t[1]

def p_data_statement_load(t):
    '''data_statement_load : LOAD obj_expression FROM expression'''
    t[0] = 'data_statement(' + t[2] + ',' + t[4] + ')'

def p_data_statement_save(t):
    '''data_statement_save : EXPORT obj_expression TO expression'''
    t[0] = 'data_statement(' + t[2] + ',' + t[4] + ')'

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
                  | ID LPAREN function_run_args RPAREN
                  | obj_expression DOT ID LPAREN function_run_args RPAREN
                  | obj_expression LSQ expression RSQ
                  | obj_expression'''
    if len(t)==4:
        t[0] = 'expression(' + t[1] + ',' + t[3] + ')'
    elif len(t)==3:
        t[0] = 'expression(' + t[2] + ')'
    elif len(t)==2:
        t[0] = 'expression(' + t[1] + ')'
    elif len(t)==7:
        t[0] = 'expression(' + t[1] + ',' + t[3] + ',' + t[5] + ')'
    elif len(t)==5:
        t[0] = 'expression(' + t[1] + ',' + t[3] + ')'
    else:
        t[0] = 'expression(' + t[1] + ')'

def p_assignment(t):
    '''assignment : obj_expression EQ expression'''
    t[0] = 'assignment(' + t[1] + ',' + t[3] + ')'

def p_obj_expression(t):
    '''obj_expression : obj_expression DOT ID
                      | ID'''
    if len(t)==2:
        t[0] = 'obj_expression(' + t[1] + ')'
    else:
        t[0] = 'obj_expression(' + t[1] + ',' + t[3] + ')'

def p_variable_def(t):
    '''variable_def : var_type ID
                    | var_type ID EQ expression
                    | var_type ID EQ NEW var_type
                    | var_type ID EQ NEW var_type LBRACK NL mul_variable_assign RBRACK'''
    if len(t)==3:
        t[0] = 'variable_def(' + t[1] + ',' + t[2] + ')'
    elif len(t)==5:
        t[0] = 'variable_def(' + t[1] + ',' + t[2] + ',' + t[4] + ')'
    elif len(t)==6:
        t[0] = 'variable_def(' + t[1] + ',' + t[2] + ',' + t[5] + ')'
    else: 
        t[0] = 'variable_def(' + t[1] + ',' + t[2] + ',' + t[5] + ',' + t[8] + ')'

def p_mul_variable_assign(t):
    '''mul_variable_assign : mul_variable_assign assignment NL
                           | data_statement_load NL
                           | mul_variable_assign NL
                           | '''
    if len(t)==4:
        t[0] = 'mul_variable_def(' + t[1] + ',' + t[2] + ')'
    elif len(t)==3:
        t[0] = 'mul_variable_def(' + t[1] + ')'
    else:
        t[0] = ''

def p_var_type(t):
    '''var_type : TEXT_TYPE
                | NUM_TYPE
                | BOOL_TYPE
                | ID
                | LIST LPAREN var_type RPAREN'''
    if len(t)==2:
        t[0] = 'var_type(' + t[1] + ')'
    else:
        t[0] = 'var_type(' + t[3] + ')'
    print(t[0])

def p_constant(t):
    '''constant : LBRACK constant_list RBRACK
                | LBRACK RBRACK
                | NUM
                | TXT
                | FALSE
                | TRUE'''            
    if len(t)<3:
        t[0] = 'constant(' + str(t[1]) + ')'
    elif len(t)==3:
        t[0] = 'constant()'
    else:
        t[0] = 'constant(' + t[2] + ')'

def p_constant_list(t):
    '''constant_list : constant_list COMMA constant_list
                     | constant'''
    if len(t)==4:
        t[0] = 'constant_list(' + t[1] + ',' + t[3] + ')'
    else:
        t[0] = 'constant_list(' + t[1] + ')'

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc

yacc.yacc()

if len(sys.argv) > 1 :
    inputfile = open(sys.argv[1],'r')
    yacc.parse(inputfile.read())
