def p_class_lines(t):
    '''class_lines : class_lines function_def NL
                   | class_lines variable_def NL
                   | class_lines
                   | '''

def p_function_lines(t):
    '''function_lines : function_lines statement NL
                      | function_lines NL
                      | '''

def p_statement(t):
    '''statement : variable_def
                 | assignment
                 | loop
                 | if_statement
                 | data_statement
                 | obj_expression DOT ID LPAREN function_args RPAREN
                 | BREAK
                 | CONTINUE'''

def p_class_def(t):
    '''class_def : CLASS ID LBRACK NL class_lines RBRACK
                 | CLASS ID EXTENDS ID LBRACK NL class_lines RBRACK'''

def p_function_def(t):
    '''function_def : FUNCTION ID LPAREN function_args RPAREN LBRACK NL function_lines RBRACK
                    | var_type FUNCTION ID LPAREN function_args RPAREN LBRACK NL function_lines RETURN expression NL RBRACK'''

def p_function_args(t):
    '''function_args : function_args COMMA function_args
                     | var_type ID'''

def p_loop(t):
    '''loop : LOOP LPAREN loop_expression RPAREN LBRACK NL function_lines RBRACK
            | FOREACH LPAREN var_type ID IN ID RPAREN LBRACK NL function_lines RBRACK
            | var_type ID EQ GETEACH LPAREN var_type ID IN ID WHERE expression RPAREN'''

def p_loop_expression(t):
    '''loop_expression : loop_expression_values COMMA loop_expression_values
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
    '''data_statement : LOAD expression FROM expression
                      | EXPORT expression TO expression'''

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
                  | assignment
                  | obj_expression DOT ID LPAREN function_args RPAREN
                  | obj_expression LSQ expression RSQ
                  | obj_expression
                  | constant'''

def p_assignment(t):
    '''assignment : ID EQ expression'''

def p_obj_expression(t):
    '''obj_expression : obj_expression DOT ID
                      | ID'''

def p_variable_def(t):
    '''variable_def : var_type ID
                    | var_type assignment
                    | var_type ID EQ NEW var_type
                    | var_type ID EQ NEW var_type LBRACK NL mul_variable_def RBRACK'''

def p_mul_variable_def(t):
    '''mul_variable_def : mul_variable_def variable_def NL
                        | variable_def NL'''

def p_var_type(t):
    '''var_type : TEXT_TYPE
                | NUM_TYPE
                | BOOL_TYPE
                | ID
                | LIST LPAREN var_type RPAREN'''

def p_constant(t):
    '''constant : LBRACK constant RBRACK
                | constant COMMA constant
                | NUM
                | TXT
                | FALSE
                | TRUE'''            

def p_error(t):
#    print("Syntax error at '%s'" % t.value)
    print("syntax error")

import ply.yacc as yacc
yacc.yacc()

if len(sys.argv) > 1 :
    inputfile = open(sys.argv[1],'r')
    yacc.parse(inputfile.read())
