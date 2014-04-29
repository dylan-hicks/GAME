import sys
import re
import json

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
def t_LBRACK(t):
    r'(\n|\#.*\n|[ ]|\t)*{'
    t.type = 'LBRACK'
    return t

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
    r'\d+\.?\d*'
    try:
        t.value = float(t.value)
    except ValueError:
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    if(t.type=='ID'):
        p = re.compile('[a-zA-Z_][a-zA-Z0-9_]{0,99}')
        if(not p.match(t.value)):
            t.value = ""
    return t

# Ignored characters
t_ignore = " \t"

def t_COMMENT(t):
    r'\#.*\n'
    t.type = 'NL'
    return t

def t_error(t):
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules (lowest to highest)

precedence = (
    ('right','NL'),
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

functions = { }
classes = { }
errors = [ ]
        
def p_program_lines(t):
    '''program_lines : include_lines lines'''

def p_include_lines(t):
    '''include_lines : include_lines INCLUDE TXT NL
                     | include_lines NL
                     | '''

def p_lines_class(t):
    '''lines : lines class_def NL'''
    if t[2][0] in classes:
        errors.append("Multiple definitions of class "+t[2][0]+".")
    else:
        classes[t[2][0]] = t[2][1]

def p_lines_function(t):
    '''lines : lines function_def NL'''
    if t[2][0] in functions:
        errors.append("Multiple definitions of function "+t[2][1]["name"]+".")
    else:
        functions[t[2][0]] = t[2][1]

def p_lines_other(t):
    '''lines : lines NL
             | '''

def p_class_lines_function(t):
    '''class_lines : class_lines function_def NL'''
    if t[2][0] in t[1]["methods"]:
        errors.append("Multiple definitions of method "+t[2][1]["name"]+".")    
    else:
        t[1]["methods"][t[2][0]] = t[2][1]
    t[0] = t[1]

def p_class_lines_variable(t):
    '''class_lines : class_lines variable_def NL'''
    if t[2][0] in t[1]["members"]:
        errors.append("Multiple definitions of member "+t[2][0]+".")  
    else:
        t[1]["members"][t[2][0]] = t[2][1]
    t[0] = t[1]

def p_class_lines_newline(t):
    '''class_lines : class_lines NL'''
    t[0] = t[1]

def p_class_lines_blank(t):
    '''class_lines : '''
    t[0] = {"members":{},"methods":{}}

def p_function_lines(t):
    '''function_lines : function_lines statement NL
                      | function_lines NL
                      | '''

def p_new_lines(t):
    '''new_lines : new_lines NL
                 | '''

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

def p_class_def(t):
    '''class_def : CLASS ID LBRACK NL class_lines RBRACK'''
    t[0] = t[2],t[5]

def p_function_def(t):
    '''function_def : FUNCTION ID LPAREN function_args RPAREN LBRACK NL function_lines RBRACK
                    | var_type FUNCTION ID LPAREN function_args RPAREN LBRACK NL function_lines RETURN expression new_lines RBRACK'''
    id_param = 2 if len(t)==10 else 3
    id_args = 4 if len(t)==10 else 5
    func_hash = t[id_param]
    for x in t[id_args][0]:
        func_hash += "*"+t[id_args][0][x] 
    to_add = { }
    to_add["name"] = t[id_param]
    to_add["args"] = t[id_args]
    if len(t)!=10:
        to_add["return"] = t[1]
    t[0] = func_hash,to_add

def p_function_args(t):
    '''function_args : function_arg_values
                     | '''
    if len(t)==1:
        t[0] = [ { } , [ ] ]
    else:
        t[0] = t[1]

def p_function_arg_values(t):
    '''function_arg_values : function_arg_values COMMA function_arg_values
                           | var_type ID'''
    if len(t)==3:
        t[0] = {t[2]:t[1]},[ t[2] ]
    else:
        for x in t[3][0]:
            if x in t[1]:
                errors.append("Multiple definitions of input name "+x+".")
            else:
                t[1][0][x] = t[3][0][x]
                t[1][1].extend(t[3][1]) 
        t[0] = t[1]

def p_function_run_args(t):
    '''function_run_args : function_run_arg_values
                         | '''

def p_function_run_arg_values(t):
    '''function_run_arg_values : function_run_arg_values COMMA function_run_arg_values
                               | expression'''

def p_loop(t):
    '''loop : LOOP LPAREN loop_expression RPAREN LBRACK NL function_lines RBRACK
            | FOREACH LPAREN var_type ID IN ID RPAREN LBRACK NL function_lines RBRACK
            | var_type ID EQ GETEACH LPAREN var_type ID IN ID WHERE expression RPAREN'''

def p_loop_expression(t):
    '''loop_expression : loop_expression COMMA loop_expression
                       | loop_expression_values
                       | '''

def p_loop_expression_values(t):
    '''loop_expression_values : START variable_def
                              | WHILE expression
                              | SET assignment'''

def p_if_statement(t):
    '''if_statement : IF LPAREN expression RPAREN LBRACK NL function_lines RBRACK
                    | IF LPAREN expression RPAREN LBRACK NL function_lines RBRACK ELSE LBRACK NL function_lines RBRACK'''

def p_data_statement(t):
    '''data_statement : data_statement_load
                      | data_statement_export'''

def p_data_statement_load(t):
    '''data_statement_load : LOAD obj_expression FROM expression'''

def p_data_statement_save(t):
    '''data_statement_export : EXPORT obj_expression TO expression'''

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
                  | LPAREN expression RPAREN
                  | NOT expression 
                  | MINUS expression %prec UMINUS
                  | constant
                  | assignment
                  | ID LPAREN function_run_args RPAREN
                  | obj_expression DOT ID LPAREN function_run_args RPAREN
                  | obj_expression LSQ expression RSQ
                  | obj_expression'''

def p_assignment(t):
    '''assignment : obj_expression EQ expression'''

def p_obj_expression(t):
    '''obj_expression : obj_expression DOT ID
                      | ID'''

def p_variable_def(t):
    '''variable_def : var_type ID
                    | var_type ID EQ expression
                    | var_type ID EQ NEW var_type
                    | var_type ID EQ NEW var_type LBRACK NL mul_variable_assign RBRACK'''
    t[0] = t[2],t[1] 

def p_mul_variable_assign(t):
    '''mul_variable_assign : mul_variable_assign assignment NL
                           | data_statement_load NL
                           | mul_variable_assign NL
                           | '''

def p_var_type(t):
    '''var_type : TEXT_TYPE
                | NUM_TYPE
                | BOOL_TYPE
                | ID
                | LIST LPAREN var_type RPAREN'''
    if len(t)==2:
        t[0] = t[1]
    else:
        t[0] = "list(" + t[3] + ")"

def p_constant(t):
    '''constant : LBRACK constant_list RBRACK
                | LBRACK RBRACK
                | NUM
                | TXT
                | FALSE
                | TRUE'''            

def p_constant_list(t):
    '''constant_list : constant_list COMMA constant_list
                     | constant'''

def p_error(t):
    '''Do nothing'''

import ply.yacc as yacc

yacc.yacc()

if len(sys.argv) > 1 :
    inputfile = open(sys.argv[1],'r')
    yacc.parse(inputfile.read())
    print json.dumps({"functions":functions,"classes":classes,"errors":errors})
