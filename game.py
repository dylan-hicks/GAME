#This file takes in a resolved (no #include statements) GAME file and produces the output.

import sys
import re
import json
import subprocess

#First the scanner is called, which return structure information on functions and classes.
scan_functions = { }
scan_classes = { }
scan_errors = [ ]

proc = subprocess.Popen(["python", "scan.py", sys.argv[1]], stdout=subprocess.PIPE, stderr=None)
out = proc.communicate()[0]
temp = json.loads(str(out))
scan_functions = temp["functions"]
scan_classes = temp["classes"]
scan_errors = temp["errors"]
if len(scan_errors)!=0:
    for x in scan_errors:
        print x
    exit(0)


#Make sure that there is a "main" function.
found = 0
for x in scan_functions:
    if scan_functions[x]["name"]=="main":
        found = 1
if found!=1:
    print "Needs a main function to run."
    exit(0)

#Whenever a variable or function or class is added to the scope, it needs to
#go into the symbol stack so the compiler can track it.
symbol_stack = [ ]

#Given a system call and an argument, these functions determine if it exists and what the output code should be.
def syscall(x,t): #syscalls with no return value, print is an exception and is below in statement
    syscalls = {
    'graph*list(num)*list(num)*text*text*text': ['graph(',')','list(num)', 'list(num)', 'text', 'text', 'text'],
    'display': ['display(',')'],
    'label*text*text': ['label(', ')', 'text', 'text'],
    'axis*list(num)*list(num)': ['axis(', ')', 'list(num)', 'list(num)'],
    'bestfit*list(num)*list(num)*text*text*text': ['bestfit(',')','list(num)', 'list(num)', 'text', 'text', 'text'],
    'subgraph*num*num*num': ['subgraph(', ')', 'num', 'num', 'num'],
    'legend': ['legend(',')']
    }
    return syscalls.get(func_shorthand(x,t),None)

def syscallret(x,t): #syscalls with a return value (last type in array)
    syscalls = {
    'sqrt*num': ['math.sqrt(',')','num','num'],
    'num_form*text*num': ['num_form(',')','text','num','text']
    }
    return syscalls.get(func_shorthand(x,t),None)

#Given two different data types, this function determines if they are equivalent.
def check_type(x,y):
    if x==y:
        return x
    elif x=="list()" or y=="list()":
        if x=="list()":
            if len(y) > 5 and y[:5]=="list(":
                return y
        else:
            if len(x) > 5 and x[:5]=="list(":
                return x
    else:
        t1 = x
        t2 = y
        while len(t1) > 5 and len(t2) > 5:
            if t1[:5]=="list(" and t1[:5]==t2[:5]:
                t1 = t1[5:]
                t2 = t2[5:]
            else:
                break
        if t1[:1]==')' and not (len(t2) > 5 and t2[:5]=="list("):
            return y
        elif t2[:1]==')' and not (len(t1) > 5 and t1[:5]=="list("):
            return x
        else:
            return ""

#Given a data type, such as list(list(bla)), determine the root type, which in this case would be bla.
def get_root_type(x):
    while len(x) > 5 and x[:5]=="list(":
        x = x[5:-1]
    return x

#Check if a data type is a list.
def list_check(x):
    if len(x) > 5 and x[:5]=="list(":
        return x[5:-1]
    else:
        return None

#Check the stack to see if it contains a symbol x, if so return what type it is as well.
def check_stack(x):
    for y in symbol_stack:
        temp = y[1].get(x,"")
        if temp!="":
            return y[0], temp
    return None

#Add something to the stack, also say what type it is.
def add_stack(name,t):
    symbol_stack[len(symbol_stack)-1][1][name] = t

#Check if the stack has a loop on it.
def within_loop():
    for y in symbol_stack:
        if y[0]=="loop":
            return True
    return False

#Check if the highest item in the stack is a class.
def above_is_class():
    if len(symbol_stack)>0 and symbol_stack[len(symbol_stack)-1][0]=="class":
        return True
    else:
        return False

#Check if there is a class on the stack, if so return it's name.
def in_class():
    if len(symbol_stack)>0 and symbol_stack[0][0]=="class":
        return symbol_stack[0][2]
    return False

#Add a tab to each line of the input string.
def add_tab(x):
    return x.replace("\n","\n\t")

#Given a function x and it's argument types y, create a descriptive string.
def func_shorthand(x,y):
    z = x
    for l in y:
        z += '*'+l[1]
    return z

#Words reserved by the GAME language that may not be used as variables/functions/classes.
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

#All the tokens used by lex and yacc (compiler generator).
tokens = [
    'ID','NUM','EQ','EXCL', 'TXT',
    'PLUS','MINUS','TIMES','DIVIDE', 'MOD',
    'LPAREN','RPAREN', 'NL' , 'LBRACK', 'RBRACK',
    'COMMA', 'GT', 'LT', 'EQEQ' , 'DOT' , 'LSQ' , 'RSQ'
    ] + list(reserved.values())

#Regular expressions for each token.

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

#Now for the grammar rules and attached actions. These rules take the tokens from lex
#and use them to follow these rules and execute the actions that generate the compiled file.

#Basic layout of one of these funtions:
#def p_name_of_rule(t):
#    '''name_of_rule : rule content'''
#    various actions that are used to ultimately produce output code

#This rule is special because it is the starting rule, all other rules must descend from it.
def p_program_lines(t):
    '''program_lines : include_lines lines'''
    sys_calls = open("syscalls.py",'r')
    toWrite = sys_calls.read()+"\nscan_classes = "+json.dumps(scan_classes)+"\n"+t[2]+"main()" #write in our syscalls and code from descending rules (t[2])
    toWrite = re.sub(r"\n[\t\n ]*\n","\n",toWrite) #removes excess lines
    out_file = open("{}.py".format(sys.argv[1]).replace(".temp", ""), "w")
    out_file.write(toWrite)

#There shouldn't be an include statements at this point, so throw an error if there are.
def p_include_lines(t):
    '''include_lines : include_lines INCLUDE TXT NL'''
    print 'Preprocessor error, include statement unresolved.'
    exit(0)

def p_include_lines_other(t):
    '''include_lines : include_lines NL
                     | '''

#Rules such as the next one are strictly for the structure of the language. The usually just concatonate all child rules.
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
    '''class_lines : class_lines function_def NL'''
    t[0] = t[1]+t[2]

def p_class_variable(t):
    '''class_lines : class_lines variable_def NL'''
    if t[2]!="":
        t[0] = t[1]+t[2]+'\n'
    else: # if variable_def is empty for some reason, just pass up class_lines
        t[0] = t[1]

def p_class_ignore(t):
    '''class_lines : class_lines NL'''
    t[0] = t[1]

def p_class_empty(t):
    '''class_lines : '''
    t[0] = ""

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
                 | data_statement'''
    t[0] = t[1]

#The obj_expression rule is used when class method is called.
#It determines what type of class the object is, if the function is available
#what the functions returns, and outputs the appropriate compiled code.
def p_statement_obj_function(t):
    '''statement : obj_expression DOT ID LPAREN function_run_args RPAREN'''
    temp1 = scan_classes.get(t[1][1],"")
    if temp1!="":
        st = func_shorthand(t[3],t[5])
        temp2 = scan_classes[t[1][1]]["methods"].get(st,"")
        if temp2!="":
            out = t[1][0]+"."+t[3]+"("
            for x in range(0,len(t[5])):
                if x!=0:
                    out += ', '
                out += t[5][x][0]
            out += ')\n'
            t[0] = out
        else:
            print "'"+t[1][0]+"' has no function '"+t[3]+"'."
            exit(0)
    else:
        temp7 = list_check(t[1][1])
        if temp1!=None:
            if t[3]=="add" and len(t[5])==1:
                temp8 = check_type(temp7,t[5][0][1])
                if temp8!="":
                    t[0] = t[1][0]+".append("+t[5][0][0]+")\n"
                else:
                    if t[5][0][1]==t[1][1]:
                        t[0] = t[1][0]+".extend("+t[5][0][0]+")\n"
                    else:
                        print "Can only add type '"+temp7+"' to '"+t[1][0]+"'."
                        exit(0)
            elif t[3]=="rem" and len(t[5])==1:
                temp8 = check_type(temp7,t[5][0][1])
                if temp8!="":
                    t[0] = t[1][0]+".remove("+t[5][0][0]+")\n"
                else:
                    print "Can only remove type '"+temp7+"' from '"+t[1][0]+"'."
                    exit(0)
            elif t[3]=="remAt" and len(t[5])==1:
                if t[5][0][1]=="num":
                    t[0] = "del "+t[1][0]+"[int("+t[5][0][0]+")]\n"
                else:
                    print "Can only remove indice type num from '"+t[1][0]+"'."
                    exit(0)
            elif t[3]=="addAt" and len(t[5])==2:
                temp8 = check_type(temp7,t[5][1][1])
                if temp8!="" and t[5][0][1]=="num":
                    t[0] = t[1][0]+"[int("+t[5][0][0]+")] = "+t[5][1][0]+"\n"
                else:
                    print "Wrong arguments for addAt."
                    exit(0)
            elif t[3]=="get":
                 t[0] = ""
            elif t[3]=="length":
                 t[0] = ""
            else:
                print "Cannot apply operator '"+t[3]+"' to a list."
                exit(0)
        else:
            if t[1][1]=="text" and t[3]=="length" and len(t[5])==0:
                t[0] = ""
            else:
                print "'"+t[1][0]+"' has no function '"+t[3]+"'."
                exit(0)

def p_statement_assign(t):
    '''statement : assignment'''
    t[0] = t[1][0]+'\n'

#Break/continue statements are simple. If you are within a loop, allow them. Otherwise don't.
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

#This rule allows functions with no return arguments to be used.
#First it checks if the function exists, then verifies that the arguments are correct.
#Then it outputs the compiled code.
def p_statement_function(t):
    '''statement : ID LPAREN function_run_args RPAREN'''
    # check if it is a system call
    if t[1]=="print" and len(t[3])==1:
        temp1 = get_root_type(t[3][0][1])
        if temp1=="" or temp1=="num" or temp1=="text" or temp1=="bool":
            t[0] = "print("+t[3][0][0]+")\n"
        else:
            print "Print needs an argument of native type"
            exit(0)
    else:
        sys_out = syscall(t[1],t[3])
        if sys_out==None:
            sys_out = syscallret(t[1],t[3])
            if sys_out!=None:
                sys_out.pop()
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
            st = func_shorthand(t[1],t[3])
            if scan_functions.get(st,"")!="":
                out = t[1]+'('
                for x in range(0,len(t[3])):
                    if x!=0:
                        out += ', '
                    out += t[3][x][0]
                out += ')\n'
            else:
                temp9 = in_class()
                if temp9!=False:
                    temp10 = scan_classes[temp9]
                    st = func_shorthand(t[1],t[3])
                    if temp10["methods"].get(st,"")!="":
                        out = 'self.'+t[1]+'('
                        for x in range(0,len(t[3])):
                            if x!=0:
                                out += ', '
                            out += t[3][x][0]
                        out += ')\n'
                    else:
                        print "No function named '"+t[1]+"'."
                        exit(0)
                else:
                    print "No function named '"+t[1]+"'."
                    exit(0)
            t[0] = out

#The following two rules allow classes to be created.
#First the class is added to the symbol stack, then all child rules are 
#executed, and then the class is popped from the symbol stack and the compiled code is generated.
def p_class_def(t):
    '''class_def : class_st LBRACK class_lines RBRACK'''
    if t[3]=="":
        t[0] = t[1]+'\n\tpass\n'
    else:
        t[0] = t[1]+'\n\t'+add_tab(t[3])
    symbol_stack.pop()

def p_class_start(t):
    '''class_st : CLASS ID'''
    symbol_stack.append([ "class", { }, t[2] ])
    for x in scan_classes[t[2]]["members"]:
        add_stack(x,scan_classes[t[2]]["members"][x])
    t[0] = 'class '+t[2]+':'

#This functions generates the compiled code for functions with no return type.
def p_function_def_void(t):
    '''function_def : FUNCTION ID LPAREN function_args_st RPAREN LBRACK NL function_lines RBRACK'''
    if t[2]=='main':
        if len(t[4][1])!=0:
            print "Function 'main' cannot have arguments."
            exit(0)
    inc = in_class()
    if inc==False:
        x = "def "+t[2]+"("
    else:
        x = "def "+t[2]+"(self"
    for y in range(0,len(t[4][1])):
        if inc==False:
            if y!=0:
                x += ","
        else:
            x += ","
        x += t[4][1][y]
    if t[8]!="":
        x += "):\n"+t[8]
    else:
        x += "):\n\tpass\n"
    symbol_stack.pop()
    t[0] = x

#Same as previous function, but WITH return types.
def p_function_def_return(t):
    '''function_def : var_type FUNCTION ID LPAREN function_args_st RPAREN LBRACK NL function_lines RETURN expression new_lines RBRACK'''
    if t[3]=='main':
        if len(t[4][1])!=0:
            print "Function 'main' cannot have arguments."
            exit(0)
    inc = in_class()
    if inc==False:
        x = "def "+t[3]+"("
    else:
        x = "def "+t[3]+"(self"
    for y in range(0,len(t[5][1])):
        if inc==False:
            if y!=0:
                x += ","
        else:
            x += ","
        x += t[5][1][y]
    x += "):\n"+t[9]
    temp1 = check_type(t[1],t[11][1])
    if temp1=="":
        print "Function '"+t[3]+" returns the wrong type."
        exit(0)
    x += '\treturn ('+t[11][0]+')\n'
    symbol_stack.pop()
    t[0] = x

#The following 5 functions process function/method arguments.
#They pass up the resulting data which is used by the function rules.
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

#The following two functions handle the geteach loop type.
#First the loop is added to the symbol stack, then the child rules are executed,
#then the loop is removed from the symbol stack and the compiled code is generated.
def p_loop(t):
    '''loop : geteach_st WHERE expression RPAREN'''
    if t[3][1]=="bool":
        t[0] = t[1][0] + " = [ ]\n\tfor "+ t[1][1] + " in "+ t[1][2] + ":\n\t\tif (" + t[3][0] + "):\n\t\t\t" + t[1][0] + ".append("+t[1][1]+")\n"
    else:
        print "An expression inside a get each statement must return a boolean value."
        exit(0)
    symbol_stack.pop()

def p_geteach_st(t):
    '''geteach_st : var_type ID EQ GETEACH LPAREN var_type ID IN ID'''
    if check_stack(t[2])==None:
        add_stack(t[2],t[1])
        symbol_stack.append([ "loop", { } ])
        temp2 = check_stack(t[9])
        if temp2!=None and check_type(temp2[1],t[1])!="":
            temp7 = list_check(t[1])
            if temp7!=None:
                if check_type(temp7,t[6])!="":
                    temp3 = check_stack(t[7])
                    if temp3==None:
                        add_stack(t[7],t[6])
                        t[0] = [ t[2], t[7], ("self." if temp2[0]=="class" else "")+t[9] ]
                    else:
                        print "Cannot redefine '"+t[7]+"'."
                        exit(0)
                else:
                    print "The temporary variable in the list you are iterating must be the same type the list contains."
                    exit(0)
            else:
                print "The geteach statement can only operator on lists."
                exit(0)
        else:
            print "Variable '"+t[9]+"' must be defined and be of type "+t[1]+"."
            exit(0)
    else:
        print "Cannot redefine '"+t[2]+"'."
        exit(0)


#The next 4 functions operate similarly on the standard loop and the geteach loop.
def p_loop_foreach(t):
    '''loop : foreach_st IN ID RPAREN LBRACK NL function_lines RBRACK'''
    ftype = t[1][0]
    fid = t[1][1]
    out = ""
    temp2 = check_stack(t[3])
    if temp2!=None:
        temp3 = list_check(temp2[1])
        if temp3!=None:
            temp4 = check_type(temp3,ftype)
            if temp4!="":
                if temp2[0]!="class":
                    out += "for "+fid+" in "+t[3]+":\n\t"
                else:
                    out += "for "+fid+" in self."+t[3]+":\n\t"
                if t[7]!="":
                    out += add_tab(t[7])
                else:
                    out += "\tpass\n"
            else:
                print "Foreach loop variable type mis-match."
                exit(0)
        else:
            print "Variable '"+t[3]+"' is not a list."
            exit(0)
    else:
        print "Unkown variable '"+t[3]+"'."
        exit(0)
    t[0] = out+"\n"
    symbol_stack.pop()

def p_foreach_st(t):
    '''foreach_st : FOREACH LPAREN var_type ID'''
    symbol_stack.append([ "loop", { } ])
    if check_stack(t[4])!=False:
        add_stack(t[4],t[3])
    else:
        print "Cannot redefine '"+t[4]+"'."
        exit(0)
    t[0] = t[3], t[4]

def p_loop_all(t):
    '''loop : loop_st LPAREN loop_expression RPAREN LBRACK NL function_lines RBRACK'''
    out = ""
    first = True
    for x in t[3]["start"]:
        if not first:
            out+="\t"
        first = False
        out += x+"\n"
    if len(t[3]["start"])!=0:
        out += "\twhile ("
    else:
        out += "while ("
    first = True
    for x in t[3]["while"]:
        if not first:
            out += " and "
        first = False
        out += "("+x+")"
    if len(t[3]["while"])==0:
        out += "True"
    out += "):\n"
    if t[7]=="" and len(t[3]["set"])==0:
        out += "\t\tpass"
    else:
        if t[7]!="":
            out += "\t"
        out += add_tab(t[7])
        if t[7]=="":
            out += "\t"
        first = True
        for x in t[3]["set"]:
            if not first:
                 out+="\t\t"
            else:
                 out+="\t"
            first = False
            out += x+"\n"
    t[0] = out+"\n"
    symbol_stack.pop()

def p_loop_st(t):
    '''loop_st : LOOP'''
    symbol_stack.append([ "loop", { } ])

#The next 5 functions process the arguments for loops, and pass them up to the apporpriate loop type.
def p_loop_expression(t):
    '''loop_expression : loop_expression COMMA loop_expression'''
    t[1]["start"].extend(t[3]["start"])
    t[1]["while"].extend(t[3]["while"])
    t[1]["set"].extend(t[3]["set"])
    t[0] = t[1]

def p_loop_expression_single(t):
    '''loop_expression : loop_expression_values'''
    t[0] = {"start":[ ],"while":[ ],"set":[ ]}
    t[0][t[1][0]].append(t[1][1])

def p_loop_expression_empty(t):
    '''loop_expression : '''
    t[0] = {"start":[ ],"while":[ ],"set":[ ]}

def p_loop_expression_values(t):
    '''loop_expression_values : START variable_def
                              | WHILE expression
                              | SET assignment'''
    if t[1]=="start":
        t[0] = t[1], t[2]
    elif t[1]=="while":
        if t[2][1]=="bool":
            t[0] = t[1], t[2][0]
        else:
            print "Loop while expressions must have arguments of type bool."
            exit(0)
    elif t[1]=="set":
        t[0] = t[1], t[2][0]

def p_loop_expression_start_assign(t):
    '''loop_expression_values : START assignment'''
    t[0] = "start", t[2][0]

#The next 3 functions produce the output code for if statements. 
#The if frame is added to the stack, the child rules are run, the code is generated,
# and then the if frame is popped from the stack.
def p_if_statement(t):
    '''if_statement : if_st LPAREN expression RPAREN LBRACK NL function_lines RBRACK
                    | if_st LPAREN expression RPAREN LBRACK NL function_lines RBRACK else_st LBRACK NL function_lines RBRACK'''
    symbol_stack.pop()
    if t[3][1]!="bool":
        print "If must have a boolean argument."
        exit(0)
    if len(t)==9:
        if t[7]!="":
            t[0] = 'if ('+t[3][0]+'):\n\t'+add_tab(t[7])
        else:
            t[0] = 'if ('+t[3][0]+'):\n\t\tpass\n'
    else:
        out = 'if ('+t[3][0]+'):\n\t'
        if t[7]!="":
            out += add_tab(t[7])
        else:
            out += '\tpass\n'
        out += '\n\telse:\n\t'
        if t[12]!="":
            out += add_tab(t[12])
        else:
            out += '\tpass\n'
        t[0] = out
    t[0] = t[0]+"\n"

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
    t[0] = t[1]

#The load and save statements simply are replaced by function calls we have written.
def p_data_statement_load(t):
    '''data_statement_load : LOAD obj_expression FROM expression'''
    if t[4][1]=="text":
        t[0] = t[2][0]+" = load_function("+t[2][0]+',"'+t[2][1]+'",'+t[4][0]+")\n"
    else:
        print 'Data statements load from text type.'
        exit(0)

def p_data_statement_save(t):
    '''data_statement_export : EXPORT obj_expression TO expression'''
    if t[4][1]=="text":
        t[0] = t[2][0]+" = export_function("+t[2][0]+","+t[4][0]+")\n"
    else:
        print 'Data statements export to text type.'
        exit(0)

#The upcoming rules are called expressions.
#Expressions return code that produces a value and also return the type of that value.
#For example, for j = 6, it would return 'j' and 'num'.

#This rule allows the creation of new objects.
def p_expression_new(t):
    '''expression : NEW ID'''
    if scan_classes.get(t[2],"")!="":
        t[0] = t[2]+"()" , t[2]
    else:
        print "No object of type '"+t[2]+"'."
        exit(0)

#If an object is a list, this rule allows you to use brackets to index into it.
def p_expression(t):
    '''expression : obj_expression LSQ expression RSQ'''
    temp1 = list_check(t[1][1])
    if temp1!=None:
        if t[3][1]=="num":
            t[0] = [ "("+t[1][0]+"[int("+t[3][0]+")])", temp1 ]
        else:
            print "'"+t[3][0]+"' is not a number and cannot be used as an array index."
            exit(0)
    else:
        if t[1][1]=="text" and t[3][1]=="num":
            t[0] = [ t[1][0]+"[int("+t[3][0]+")]", "text" ]
        else:
            print "'"+t[1][0]+"' is not a list or text and cannot use the [ ] operator."
            exit(0)

#If an object is a class, this rule allows you to execute one of it's methods (the method must return a value).
def p_expression_obj(t):
    '''expression : obj_expression DOT ID LPAREN function_run_args RPAREN'''
    temp1 = scan_classes.get(t[1][1],"")
    if temp1!="":
        st = func_shorthand(t[3],t[5])
        temp2 = scan_classes[t[1][1]]["methods"].get(st,"")
        if temp2!="":
            temp3 = temp2.get("return","")
            if temp3!="":
                out = "("+t[1][0]+"."+t[3]+"("
                for x in range(0,len(t[5])):
                    if x!=0:
                        out += ', '
                    out += t[5][x][0]
                out += '))'
                t[0] = out, temp3
            else:
                print "'"+t[1][0]+"."+t[3]+" has no return type."
        else:
            print "'"+t[1][0]+"' has no function '"+t[3]+"'."
            exit(0)
    else:
        temp7 = list_check(t[1][1])
        if temp7!=None:
            if t[3]=="get" and len(t[5])==1:
                temp8 = check_type(temp7,t[5][0][1])
                if t[5][0][1]=="num":
                    t[0] = [ t[1][0]+"[int("+t[5][0][0]+")]", temp7 ]
                else:
                    print "Can only index into arrays with type num."
                    exit(0)
            elif t[3]=="length" and len(t[5])==0:
                t[0] = [ "len("+t[1][0]+")" , "num" ]
            else:
                print "Cannot apply operator '"+t[3]+"' to a list."
                exit(0)
        elif t[1][1]=="text" and t[3]=="length" and len(t[5])==0:
             t[0] = [ "len("+t[1][0]+")" , "num" ]
        else:
            print "'"+t[1][0]+"' has no function '"+t[3]+"'."
            exit(0)

def p_expression_assign(t):
    '''expression : assignment'''
    t[0] = t[1]

#This rule allows you to call functions that return a value.
def p_expression_call(t):
    '''expression : ID LPAREN function_run_args RPAREN'''
    sys_out = syscallret(t[1],t[3])
    if sys_out!=None:
        if len(sys_out)-3==len(t[3]):
            args = ""
            for z in range(0,len(sys_out)-3):
               if sys_out[z+2]!=t[3][z][1]:
                   print t[1]+" expecting argument of type '"+sys_out[z+2]+"' given '"+t[3][z][1]+"'."
                   exit(0)
               if z!=0:
                    args += ", "
               args += t[3][z][0]
            t[0] = [ sys_out[0]+args+sys_out[1], sys_out[len(sys_out)-1] ]
        else:
            print t[1]+" accepts "+(len(sys_out)-2)+" arguments."
            exit(0)
    else:
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
            temp9 = in_class()
            if temp9!=False:
                temp10 = scan_classes[temp9]
                st = func_shorthand(t[1],t[3])
                if temp10["methods"].get(st,"")!="":
                    temp11 = temp10["methods"][st].get("return","")
                    if temp11!="":
                        print temp10["methods"]
                        out = 'self.'+t[1]+'('
                        for x in range(0,len(t[3])):
                            if x!=0:
                                out += ', '
                            out += t[3][x][0]
                        out += ')'
                        out = [ out, temp11 ]
                    else:
                        print "No function named '"+t[1]+"'."
                        exit(0)
                else:
                    print "No function named '"+t[1]+"'."
                    exit(0)
            else:
                print "No function named '"+t[1]+"'."
                exit(0)
        t[0] = out

def p_expression_obje(t):
    '''expression : obj_expression'''
    t[0] = t[1]

#This rule allows you to use the unary minus operator.
def p_expression_uminus(t):
    '''expression : MINUS expression %prec UMINUS'''
    if t[2][1]=="num":
        t[0] = [ '-1*('+t[2][0]+')', "num" ]
    else:
        print "Cannot apply '"+t[1]+"' operator to "+t[2][1]+"."
        exit(0)

#If something is boolean, you can use the not operator.
def p_expression_not(t):
    '''expression : NOT expression'''
    if t[2][1]=="bool":
        t[0] = [ 'not ('+t[2][0]+')', "bool" ]
    else:
        print "Cannot apply '"+t[1]+"' operator to "+t[2][1]+"."
        exit(0)

#If both arguments are boolean, you can use binary operators.
def p_expression_bool(t):
    '''expression : expression AND expression
                  | expression OR expression'''
    if t[1][1]=="bool" and t[3][1]=="bool":
        t[0] = [ '('+t[1][0]+') '+t[2]+' ('+t[3][0]+')', "bool" ]
    else:
        print "Cannot apply '"+t[2]+"' operator to "+t[1][1]+" and "+t[3][1]+"."
        exit(0)

#Allow balanced parantheses anywhere in expressions.
def p_expression_paren(t):
    '''expression : LPAREN expression RPAREN'''
    t[0] = t[2]

#Equivalence operator on equivalent types.
def p_expression_eq(t):
    '''expression : expression EQEQ expression'''
    if (t[1][1]==t[3][1]) and (t[1][1]=="num" or t[1][1]=="text" or t[1][1]=="bool"):
        t[0] = [ '('+t[1][0]+')==('+t[3][0]+')', "bool" ]
    else:
        print "Cannot apply '"+t[2]+"' operator to "+t[1][1]+" and "+t[3][1]+"."
        exit(0)

#Boolean operators for numbers.
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

#Common mathematic operators.
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

#Addition or concatonation operator.
def p_expression_plus(t):
    '''expression : expression PLUS expression'''
    if t[1][1]=="num" and t[3][1]=="num":
        t[0] = [ '('+t[1][0]+')+('+t[3][0]+')', "num" ]
    elif t[1][1]=="num" and t[3][1]=="text":
        t[0] = [ '(str('+t[1][0]+'))+('+t[3][0]+')', "text" ]
    elif t[1][1]=="text" and t[3][1]=="num":
        t[0] = [ '('+t[1][0]+')+(str('+t[3][0]+'))', "text" ]
    elif t[1][1]=="bool" and t[3][1]=="text":
        t[0] = [ '(str('+t[1][0]+'))+('+t[3][0]+')', "text" ]
    elif t[1][1]=="text" and t[3][1]=="bool":
        t[0] = [ '('+t[1][0]+')+(str('+t[3][0]+'))', "text" ]
    elif t[1][1]=="text" and t[3][1]=="text":
        t[0] = [ '('+t[1][0]+')+('+t[3][0]+')', "text" ]
    else:
        print "Cannot apply '+' operator to "+t[1][1]+" and "+t[3][1]+"."
        exit(0)

#Allow constants as expressions.
def p_expression_constant(t):
    '''expression : constant'''
    t[0] = t[1]

#Assign class members when possible.
def p_assignment(t):
    '''assignment : obj_expression EQ expression'''
    temp1 = check_type(t[1][1],t[3][1])
    if temp1!="":
        t[0] = [ t[1][0]+' = '+t[3][0], temp1 ]
    else:
        print "'"+t[1][0]+"' does not have type '"+t[3][1]+"'."
        exit(0)

#Access class members.
def p_obj_expression(t):
    '''obj_expression : obj_expression DOT ID'''
    temp10 = scan_classes.get(t[1][1],"")
    if temp10!="":
        temp = scan_classes[t[1][1]]["members"].get(t[3],"")
        if temp=="":
            print "'"+t[1][0]+" has no member '"+t[3]+"'."
            exit(0)
    else:
        print "'"+t[1][0]+"' is not a class."
        exit(0)
    t[0] = [ "("+t[1][0]+"."+t[3]+")", temp ]

#Find the object with a particular name.
def p_obj_expression_id(t):
    '''obj_expression : ID'''
    temp1 = check_stack(t[1])
    if temp1!=None:
        if temp1[0]=="class":
            t[0] = [ '(self.'+t[1]+')', temp1[1] ]
        else:
            t[0] = [ t[1], temp1[1] ]
    else:
        print "Unknown variable '"+t[1]+"'."
        exit(0)

#Allow variables to be initialized.
def p_variable_def_expression(t):
    '''variable_def : var_type ID EQ expression'''
    if not above_is_class():
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
    else:
        temp2 = check_type(t[1],t[4][1])
        if temp2!="":
            if symbol_stack[0][2]==get_root_type(temp2):
                print "Cannot instantiate a class while defining it."
                exit(0)
            t[0] = t[2]+' = ('+t[4][0]+')'
        else:
            print "Type conflict with '"+t[2]+"'."
            exit(0)

#Allow variables to be defined.
def p_variable_def_simple(t):
    '''variable_def : var_type ID'''
    inc = above_is_class()
    if inc==False:
        temp = check_stack(t[2])
        if temp==None:
            add_stack(t[2],t[1])
        else:
            print "Cannot redefine variable '"+t[2]+"'."
            exit(0)
    else:
        if get_root_type(t[1])==symbol_stack[0][2]:
            print "Cannot have a class inside a class of the same type."
            exit(0)
    t[0] = t[2]+" = "
    temp20 = list_check(t[1])
    if temp20==None:
        if t[1]=="num":
            t[0] += "0"
        elif t[1]=="text":
            t[0] += '""'
        elif t[1]=="bool":
            t[0] += "False"
        else:
            t[0] += t[1]+"()"
    else:
        t[0] += "[ ]"

#Determine variable type.
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

#Allow different types of constants and lists of constants.
def p_constant(t):
    '''constant : LBRACK constant_list RBRACK
                | LBRACK RBRACK'''
    if len(t)==4:
        out = "[ "
        for x in range(0,len(t[2][0])):
            if x!=0:
                out += ', '
            out += t[2][0][x]
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
                     | expression'''
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

#Run the compiler.
if len(sys.argv) > 1 :
    inputfile = open(sys.argv[1],'r')
    yacc.parse(inputfile.read())
