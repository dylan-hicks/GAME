# Known bugs: start part of loop expression must be on left

import sys
import re
import json
import subprocess

scan_functions = { }
scan_classes = { }
scan_errors = [ ]

proc = subprocess.Popen(["python", "scan2.py", sys.argv[1]], stdout=subprocess.PIPE, stderr=None)
out = proc.communicate()[0]
temp = json.loads(str(out))
scan_functions = temp["functions"]
scan_classes = temp["classes"]
scan_errors = temp["errors"]
if len(scan_errors)!=0:
    for x in scan_errors:
        print x
    exit(0)
found = 0
for x in scan_functions:
    if scan_functions[x]["name"]=="main":
        found = 1
if found!=1:
    print "Must have 'main' function."
    exit(0)

symbol_stack = [ ]

def syscall(x):
    syscalls = {
    'print': ['print(',')','text']
    }
    return syscalls.get(x,None)

def check_type(x,y):
    if x==y:
        return x
    else:
        t1 = x
        t2 = y
        while len(t1) > 5 and len(t2) > 5:
            if t1[:5]=="list(" and t1[:5]==t2[:5]:
                t1 = t1[5:]
                t2 = t2[5:]
        if t1[:1]==')' and not (len(t2) > 5 and t2[:5]=="list("):
            return y
        elif t2[:1]==')' and not (len(t1) > 5 and t1[:5]=="list("):
            return x
        else:
            return ""

def check_stack(x):
    for y in symbol_stack:
        temp = y[1].get(x,"")
        if temp!="":
            return y[0], temp
    return None

def add_stack(name,t):
    symbol_stack[len(symbol_stack)-1][1][name] = t

def within_loop():
    for y in symbol_stack:
        if y[0]=="loop":
            return True
    return False

def add_tab(x):
    return x.replace("\n","\n\t")

def func_shorthand(x,y):
    z = x
    for l in y:
        z += '*'+l[1]
    return z

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
    r'\d+(\.\d*)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    t.value = str(t.value)
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
    print("Illegal character '%s'" % t.value[0])
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

        
def p_program_lines(t):
    '''program_lines : include_lines lines'''
    toWrite = t[2]+"main()"
    print toWrite
    out_file = open("{}.py".format(sys.argv[1]), "w")
    out_file.write(toWrite)

def p_include_lines(t):
    '''include_lines : include_lines INCLUDE TXT NL'''
    print 'Preprocessor error, include statement unresolved.'
    exit(0)

def p_include_lines_other(t):
    '''include_lines : include_lines NL
                     | '''

def p_lines_class(t):
    '''lines : lines class_def NL'''
    t[0] = t[1] + t[2] + "\n"

def p_lines_function(t):
    '''lines : lines function_def NL'''
    t[0] = t[1] + t[2] + "\n"

def p_lines_nl(t):
    '''lines : lines NL'''
    t[0] = t[1]

def p_lines_empty(t):
    '''lines : '''
    t[0] = ""

def p_class_lines(t):
    '''class_lines : class_lines function_def NL
                   | class_lines variable_def NL
                   | class_lines NL
                   | '''
    #if len(t)==4:
    #elif len(t)==3:
    #else:

def p_function_lines_statement(t):
    '''function_lines : function_lines statement NL'''
    if t[2]=="":
        t[0] = t[1]
    else:
        t[0] = t[1] + "\t" + t[2]

def p_function_lines_nl(t):
    '''function_lines : function_lines NL'''
    t[0] = t[1]

def p_function_lines_empty(t):
    '''function_lines : '''
    t[0] = ""

def p_new_lines(t):
    '''new_lines : new_lines NL
                 | '''

def p_statement(t):
    '''statement : loop
                 | data_statement
                 | obj_expression DOT ID LPAREN function_run_args RPAREN'''

def p_statement_assign(t):
    '''statement : assignment'''
    t[0] = t[1][0]+'\n'

def p_statement_flow(t):
    '''statement : BREAK
                 | CONTINUE'''
    if within_loop():
        t[0] = t[1]+'\n'
    else:
        print 'Cannot call '+t[1]+' outside a loop.'
        exit(0)

def p_statement_variable(t):
    '''statement : variable_def''' 
    t[0] = t[1] + '\n'

def p_statement_if_statement(t):
    '''statement : if_statement'''
    t[0] = t[1]

def p_statement_function(t):
    '''statement : ID LPAREN function_run_args RPAREN'''
    # check for system calls
    sys_out = syscall(t[1])
    if sys_out!=None:
        if len(sys_out)-2==len(t[3]):
            args = ""
            for z in range(0,len(sys_out)-2):
               if sys_out[z+2]!=t[3][z][1]:
                   print t[1]+" expecting argument of type '"+sys_out[z+2]+"' given '"+t[3][z][1]+"'."
                   exit(0)
               if z!=0:
                    args += ", "
               args += t[3][z][0]
            t[0] = sys_out[0]+args+sys_out[1]+'\n'
        else:
            print t[1]+" accepts "+(len(sys_out)-2)+" arguments."
            exit(0)
    else:
        found = False
        for x in scan_functions:
            if scan_functions[x]["name"]==t[1]:
                found = True
                kk = scan_functions[x]["args"]
                args = ""
                for z in range(0,len(kk[1])):
                    if z!=0:
                        args += ", "
                    val = kk[0][kk[1][z]]
                    if val!=t[3][z][1]:
                        print t[1]+" expecting argument of type '"+val+"' given '"+t[3][z][1]+"'."
                        exit(0)
                    else:
                        args += t[3][z][0]
                t[0] = t[1]+'('+args+')'+'\n'     
        if found==False:
            print "Unknown function '"+t[1]+"'."
            exit(0)

def p_class_def(t):
    '''class_def : class_st LBRACK NL class_lines RBRACK'''
    symbol_stack.pop()

def p_class_start(t):
    '''class_st : CLASS ID'''
    symbol_stack.append([ "class", { } ])

def p_function_def_void(t):
    '''function_def : FUNCTION ID LPAREN function_args_st RPAREN LBRACK NL function_lines RBRACK'''
    if t[2]=='main':
        if len(t[4][1])!=0:
            print "Function 'main' cannot have arguments."
            exit(0)
    x = "def "+t[2]+"("
    for y in range(0,len(t[4][1])):
        if y!=0:
            x += ","
        x += t[4][1][y]
    if t[8]!="":
        x += "):\n"+t[8]
    else:
        x += "):\npass"
    symbol_stack.pop()
    t[0] = x

def p_function_def_return(t):
    '''function_def : var_type FUNCTION ID LPAREN function_args_st RPAREN LBRACK NL function_lines RETURN expression new_lines RBRACK'''
    if t[3]=='main':
        if len(t[4][1])!=0:
            print "Function 'main' cannot have arguments."
            exit(0)
    x = "def "+t[3]+"("
    for y in range(0,len(t[5][1])):
        if y!=0:
            x += ","
        x += t[5][1][y]
    x += "):\n"+t[9]
    temp1 = check_type(t[1],t[11][1])
    if temp1=="":
        print "Function '"+t[3]+" returns the wrong type."
        exit(0)
    x += '\treturn ('+t[11][0]+')'
    symbol_stack.pop()
    t[0] = x

def p_function_args_st(t):
    '''function_args_st : function_args'''
    symbol_stack.append([ "function", { } ])
    for x in t[1][0]:
        if check_stack(x)==None:
            add_stack(x,t[1][0][x])
        else:
            print "Variable name conflict with'"+x+"'."
            exit(0)
    t[0] = t[1]

def p_function_args(t):
    '''function_args : function_arg_values
                     | '''
    if len(t)==1:
        t[0] = [ {}, [ ] ]
    else:
        t[0] = t[1]

def p_function_arg_values(t):
    '''function_arg_values : function_arg_values COMMA function_arg_values
                           | var_type ID'''
    if len(t)==3:
        t[0] = [ {t[2]:t[1]}, [ t[2] ] ]
    else:
        for x in t[3][1]:
            t[1][0][x] = t[3][0][x]
            t[1][1].append(x)   
        t[0] = t[1]

def p_function_run_args(t):
    '''function_run_args : function_run_arg_values
                         | '''
    if len(t)==1:
        t[0] = [ ]
    else:
        t[0] = t[1]

def p_function_run_arg_values(t):
    '''function_run_arg_values : function_run_arg_values COMMA function_run_arg_values
                               | expression'''
    if len(t)==2:
        t[0] = [ t[1] ]
    else:
        t[1].extend(t[3])
        t[0] = t[1]

def p_loop(t):
    '''loop : LOOP LPAREN loop_expression RPAREN LBRACK NL function_lines RBRACK
            | FOREACH LPAREN var_type ID IN ID RPAREN LBRACK NL function_lines RBRACK
            | var_type ID EQ GETEACH LPAREN var_type ID IN ID WHERE expression RPAREN'''
    #if len(t)==9:
    #elif len(t)==12:
    #else:    

def p_loop_expression(t):
    '''loop_expression : loop_expression COMMA loop_expression
                       | loop_expression_values
                       | '''
    #if len(t)==4:
    #elif len(t)==2:
    #else:

def p_loop_expression_values(t):
    '''loop_expression_values : START variable_def
                              | WHILE expression
                              | SET assignment'''

def p_if_statement(t):
    '''if_statement : if_st LPAREN expression RPAREN LBRACK NL function_lines RBRACK
                    | if_st LPAREN expression RPAREN LBRACK NL function_lines RBRACK else_st LBRACK NL function_lines RBRACK'''
    symbol_stack.pop()
    if t[3][1]!="bool":
        print "If must have a boolean argument."
        exit(0)
    if len(t)==9:
        t[0] = 'if ('+t[3][0]+'):\n\t'+add_tab(t[7])
    else:
        t[0] = 'if ('+t[3][0]+'):\n\t'+add_tab(t[7])+'\n\telse:\n\t'+add_tab(t[12]) 

def p_if_st(t):
    '''if_st : IF'''
    symbol_stack.append([ "if", { } ])

def p_else_st(t):
    '''else_st : ELSE'''
    symbol_stack.pop()
    symbol_stack.append([ "if", { } ])

def p_data_statement(t):
    '''data_statement : data_statement_load
                      | data_statement_export'''
    #t[0] = t[1]

def p_data_statement_load(t):
    '''data_statement_load : LOAD obj_expression FROM expression'''

def p_data_statement_save(t):
    '''data_statement_export : EXPORT obj_expression TO expression'''

def p_expression(t):
    '''expression : obj_expression DOT ID LPAREN function_run_args RPAREN
                  | obj_expression LSQ expression RSQ'''

def p_expression_assign(t):
    '''expression : assignment'''
    t[0] = t[1] 

def p_expression_call(t):
    '''expression : ID LPAREN function_run_args RPAREN'''
    st = func_shorthand(t[1],t[3])
    if scan_functions.get(st,"")!="":
        out = t[1]+'('
        for x in range(0,len(t[3])):
            if x!=0:
                out += ', '
            out += t[3][x][0]
        out += ')'
        returnt = scan_functions[st].get("return","")
        if returnt=="":
            print "Function '"+t[1]+"' does not return a value."
            exit(0)
        else:
            out = [ out, returnt ]
    else:
        print "No function named '"+t[1]+"'."
        exit(0)
    t[0] = out 

def p_expression_obje(t):
    '''expression : obj_expression'''
    t[0] = t[1]

def p_expression_uminus(t):
    '''expression : MINUS expression %prec UMINUS'''
    if t[2][1]=="num":
        t[0] = [ '-1*('+t[2][0]+')', "num" ]
    else:
        print "Cannot apply '"+t[1]+"' operator to "+t[2][1]+"."
        exit(0)

def p_expression_not(t):
    '''expression : NOT expression'''
    if t[2][1]=="bool":
        t[0] = [ 'not ('+t[2][0]+')', "bool" ]
    else:
        print "Cannot apply '"+t[1]+"' operator to "+t[2][1]+"."
        exit(0) 

def p_expression_bool(t):
    '''expression : expression AND expression
                  | expression OR expression'''
    if t[1][1]=="bool" and t[3][1]=="bool":
        t[0] = [ '('+t[1][0]+') '+t[2]+' ('+t[3][0]+')', "bool" ]
    else:
        print "Cannot apply '"+t[2]+"' operator to "+t[1][1]+" and "+t[3][1]+"."
        exit(0)    

def p_expression_paren(t):
    '''expression : LPAREN expression RPAREN'''
    t[0] = t[2]

def p_expression_eq(t):
    '''expression : expression EQEQ expression'''
    if (t[1][1]==t[3][1]) and (t[1][1]=="num" or t[1][1]=="text" or t[1][1]=="bool"):
        t[0] = [ '('+t[1][0]+')==('+t[3][0]+')', "bool" ]
    else:
        print "Cannot apply '"+t[2]+"' operator to "+t[1][1]+" and "+t[3][1]+"."
        exit(0)

def p_expression_numeric_bool3(t):
    '''expression : expression GT expression
                  | expression LT expression'''
    if t[1][1]=="num" and t[3][1]=="num":
        t[0] = [ '('+t[1][0]+')'+t[2]+'('+t[3][0]+')', "bool" ]
    else:
        print "Cannot apply '"+t[2]+"' operator to "+t[1][1]+" and "+t[3][1]+"."
        exit(0)

def p_expression_numeric_bool4(t):
    '''expression : expression GT EQ expression %prec GTEQ
                  | expression LT EQ expression %prec LTEQ
                  | expression EXCL EQ expression %prec NOTEQ'''
    if t[1][1]=="num" and t[4][1]=="num":
        t[0] = [ '('+t[1][0]+')'+t[2]+t[3]+'('+t[4][0]+')', "bool" ]
    else:
        print "Cannot apply '"+t[2]+"' operator to "+t[1][1]+" and "+t[4][1]+"."
        exit(0)

def p_expression_numeric(t):
    '''expression : expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression'''
    if t[1][1]=="num" and t[3][1]=="num":
        t[0] = [ '('+t[1][0]+')'+t[2]+'('+t[3][0]+')', "num" ]
    else:
        print "Cannot apply '"+t[2]+"' operator to "+t[1][1]+" and "+t[3][1]+"."
        exit(0)

def p_expression_plus(t):
    '''expression : expression PLUS expression'''
    if t[1][1]=="num" and t[3][1]=="num":
        t[0] = [ '('+t[1][0]+')+('+t[3][0]+')', "num" ]
    elif t[1][1]=="num" and t[3][1]=="text":
        t[0] = [ '(str('+t[1][0]+'))+('+t[3][0]+')', "text" ]
    elif t[1][1]=="text" and t[3][1]=="num":
        t[0] = [ '('+t[1][0]+')+(str('+t[3][0]+'))', "text" ]
    else:
        print "Cannot apply '+' operator to "+t[1][1]+" and "+t[3][1]+"."
        exit(0)
    
def p_expression_constant(t):
    '''expression : constant'''
    t[0] = t[1]

def p_assignment(t):
    '''assignment : obj_expression EQ expression'''
    temp1 = check_type(t[1][1],t[3][1])
    if temp1!="":
        t[0] = [ t[1][0]+' = '+t[3][0], temp1 ]
    else:
        print t[1][0]+"does not have type '"+t[3][1]+"'."
        exit(0)

def p_obj_expression(t):
    '''obj_expression : obj_expression DOT ID'''

def p_obj_expression_id(t):
    '''obj_expression : ID'''
    temp1 = check_stack(t[1])
    if temp1!=None:
        t[0] = [ t[1], temp1[1] ]
    else:
        print "Unknown variable '"+t[1]+"'."
        exit(0)

def p_variable_def(t):
    '''variable_def : var_type ID EQ NEW var_type
                    | var_type ID EQ NEW var_type LBRACK NL mul_variable_assign RBRACK'''

def p_variable_def_expression(t):
    '''variable_def : var_type ID EQ expression'''
    temp = check_stack(t[2])
    if temp==None:
        add_stack(t[2],t[1])
        temp2 = check_type(t[1],t[4][1])
        if temp2!="":
            t[0] = t[2]+' = ('+t[4][0]+')'
        else:
            print "Type conflict with '"+t[2]+"'."
            exit(0)
    else:
        print "Cannot redefine variable '"+t[2]+"'."
        exit(0)

def p_variable_def_simple(t):
    '''variable_def : var_type ID'''
    temp = check_stack(t[2])
    if temp==None:
        add_stack(t[2],t[1])
        t[0] = ""
    else:
        print "Cannot redefine variable '"+t[2]+"'."
        exit(0)

def p_mul_variable_assign(t):
    '''mul_variable_assign : mul_variable_assign assignment NL
                           | data_statement_load NL
                           | mul_variable_assign NL
                           | '''
    #if len(t)==4:
    #elif len(t)==3:
    #else:

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
                | LBRACK RBRACK'''
    if len(t)==3:
        out = "[ "
        for x in range(0,len(t[2][0])):
            if x!=0:
                out += ', '
            t[2][0][x]
        out += " ]"
        t[0] = [ out, t[2][1] ]
    else:
        t[0] = [ "[ ]", "list()" ]

def p_constant_num(t):
    '''constant : NUM'''
    t[0] = [ t[1], "num" ]

def p_constant_txt(t):
    '''constant : TXT'''
    t[0] = [ t[1], "text" ]

def p_constant_bool_true(t):
    '''constant : TRUE'''
    t[0] = [ 'True', "bool" ]

def p_constant_bool_false(t):
    '''constant : FALSE'''
    t[0] = [ 'False', "bool" ]

def p_constant_list(t):
    '''constant_list : constant_list COMMA constant_list
                     | constant'''
    if len(t)==4:
        temp = check_type(t[1][1],t[3][1])
        if temp!="":
            t[1][0].extend(t[3][0])
            t[1][1] = temp
            t[0] = t[1]
        else:
            print("Cannot create list containing multiple types.")
            exit(0)
    else:
        t[0] = [ [ t[1][0] ], "list("+t[1][1]+")"  ]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc

yacc.yacc()

if len(sys.argv) > 1 :
    inputfile = open(sys.argv[1],'r')
    yacc.parse(inputfile.read())
