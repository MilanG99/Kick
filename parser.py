# Author        : Milan Gulati
# Description   : Recursive-descent parser and interpreter. Includes driver code.
# See README.txt for instructions on how to run. 

import sys                  # for command line args
from lexer import *         # import lexer

userVars = []               # SYMBOL TABLE - list to store key-par variables from the user

# EXPRESSION PARSING #
# <expr>
def parseExpr(val, tok, userVars):
    # given start of expression (tok)
    # find expr_n and expr_b
    # using these find result of expr and return

    if (tok[0][0] == 24 or tok[0][0] == 26 or tok[0][0] == 14 or tok[0][0] == 31 or 
        tok[0][0] == 32 or tok[0][0] == 33 or tok[0][0] == 34 or tok[0][0] == 15 or 
        tok[0][0] == 16 or tok[0][0] == 17 or tok[0][0] == 13 or tok[0][0] == 14):
        ret = parseExpr_N(val,tok, userVars)

    # if empty or "and" or "or" it is expr_b
    elif tok[0][0] == 11:
        ret = parseExpr_B(val, tok, userVars)
    elif tok[0][0] == 12:
        ret = parseExpr_B(val, tok, userVars)
    else:
        return val

    return parseExpr(ret[0], ret[1], userVars)     # recursive call with updated token list

# <n_expr>
def parseExpr_N(val, tok, userVars):
    # start must be a value
    # check what first token is
        # act accordingly
    # return parseExpr_N with updated input after evaluating - will end at semicolon

    # N_EXPR -> TERM
    if tok[0][0] == 24:                 # "(" <expr> ")"
        ret = parseTerm(val, tok[1:], userVars)

    elif (tok[0][0] == 26 or tok[0][0] == 31 or 
        tok[0][0] == 32 or tok[0][0] == 33 or tok[0][0] == 34 or tok[0][0] == 15 or 
        tok[0][0] == 16 or tok[0][0] == 17 or tok[0][0] == 18 or tok[0][0] == 19 or
        tok[0][0] == 20 or tok[0][0] == 21 or tok[0][0] == 22 or tok[0][0] == 23):
        ret = parseTerm(val, tok, userVars)

    # N_EXPR -> T_EXPR
    elif tok[0][0] == 13:               # +
        ret = parseExpr_T(val, tok, userVars)
    elif tok[0][0] == 14:               # -
        ret = parseExpr_T(val, tok, userVars)
    else:
        return val, tok

    return parseExpr_N(ret[0], ret[1], userVars)

# <b_expr>
def parseExpr_B(val, tok, userVars):
    if tok[0][0] == 11:                 # "and"
        if (val and parseExpr_N(val, tok[1:], userVars)):
            return 1, tok[1:]
        else:
            return 0, tok[1:]
    elif tok[0][0] == 12:               # "or"
        if (val or parseExpr_N(val, tok[1:], userVars)):
            return 1, tok[1:]
        else:
            return 0, tok[1:]
    else:                               # empty
        return

# <t_expr>
def parseExpr_T(val, tok, userVars):
    if tok[0][0] == 13:                  # "+"'
        return val + (parseExpr_N(val, tok[1:], userVars))[0], tok[2:]
    elif tok[0][0] == 14:                # "-"
        return val - (parseExpr_N(val, tok[1:], userVars))[0], tok[2:]
    else:                           # empty
        return


# <term>
def parseTerm(val, tok, userVars):
    if tok[0][0] == 24:
        ret = parseExpr(val, tok, userVars)

    # TERM -> FACTOR
    elif (tok[0][0] == 26 or tok[0][0] == 31 or tok[0][0] == 32 or
        tok[0][0] == 33 or tok[0][0] == 34 or tok[0][0] == 18 or tok[0][0] == 19 or
        tok[0][0] == 20 or tok[0][0] == 21 or tok[0][0] == 22 or tok[0][0] == 23):
        ret = parseFactor(val, tok, userVars)

    # TERM -> F_EXPR
    elif(tok[0][0] == 15 or tok[0][0] == 16 or tok[0][0] == 17):
        ret = parseExpr_F(val, tok, userVars)
    else:
        return val, tok

    return parseTerm(ret[0], ret[1], userVars)

# <f_expr>
def parseExpr_F(val, tok, userVars):
    if tok[0][0] == 15:         # *
        return val * (parseTerm(val, tok[1:], userVars))[0], tok[2:]               
    elif tok[0][0] == 16:       # /
        return val / (parseTerm(val, tok[1:], userVars))[0], tok[2:]
    elif tok[0][0] == 17:       # %
        return val % (parseTerm(val, tok[1:], userVars))[0], tok[2:]
    else:
        return

# <factor>
def parseFactor(val, tok, userVars):
    # FACTOR -> VALUE
    if(tok[0][0] == 26 or tok[0][0] == 31 or tok[0][0] == 32 or
        tok[0][0] == 33 or tok[0][0] == 34):
        ret = parseValue(tok, userVars)

    # FACTOR -> V_EXPR
    elif(tok[0][0] == 18 or tok[0][0] == 19 or tok[0][0] == 20 or tok[0][0] == 21 or
        tok[0][0] == 22 or tok[0][0] == 23):
        ret = parseExpr_V(val, tok, userVars)
    else:
        return val, tok
    return parseFactor(ret[0], ret[1], userVars)
    
# <value>
def parseValue(tok, userVars):
    if tok[0][0] ==  24:                        # "(" <expr> ")"
        return parseExpr(val, tok[1:], userVars)

    elif tok[0][0] == 26:                       # "!" <value>
        val = parseValue(tok[1:], userVars)
        if val == 1:
            return 0, tok[1:]
        elif val == 0:
            return 1, tok[1:]

    elif tok[0][0] == 31:                       # ID
        # search for ID in local storage
        #var = (userVars[0])[1]
        for i in userVars:
            if i[0] == tok[0][1]:       # if user var equals statement var
                var = i[1]
        return var, tok[1:]

        # # search for ID in local storage
        # for i in userVars:
        #     if i[0] == tok[0][1]:     # if user var equals statement var
        #         return i[1], tok[1:]

    elif tok[0][0] == 32:               # INT
        return int(tok[0][1]), tok[1:]

    elif tok[0][0] == 34:               # CHAR
        return tok[0][1], tok[1:]

# <v_expr>
def parseExpr_V(val, tok, userVars):
    ret = parseValue(tok[1:], userVars) # call <value> to get value
    compVal = ret[0]                    # get comp value     

    if tok[0][0] == 18:                 # >
        if val > compVal:               # True
            return 1, tok[2:]
        else:                           # False
            return 0, tok[2:]
    elif tok[0][0] == 19:               # >=
        if val >= compVal:              # True
            return 1, tok[2:]
        else:                           # False
            return 0, tok[2:]
    elif tok[0][0] == 20:               # <
        if val < compVal:               # True
            return 1, tok[2:]
        else:                           # False
            return 0, tok[2:]
    elif tok[0][0] == 21:               # <=
        if val <= compVal:              # True
            return 1, tok[2:]
        else:                           # False
            return 0, tok[2:]
    elif tok[0][0] == 22:               # ==
        if val == compVal:              # True
            return 1, tok[2:]
        else:                           # False
            return 0, tok[2:]
    elif tok[0][0] == 23:               # !=
        if val != compVal:              # True
            return 1, tok[2:]
        else:                           # False
            return 0, tok[2:]

# STMT Parsing #

# <print>
def parsePrint(tok, userVars):
    # print a string
    if tok[0][0] == 1 and tok[1][0] == 30 and tok[2][0] == 0:
        string = tok[1][1]
        string = string[1:-1]                                   # remove quotes
        i = 0
        while i < len(string):                                  # print string char by char
            if string[i] == "\\" and string[i + 1] == "n":      # handle newline escape char
                print()
                i += 1
            elif string[i] == "\\" and string[i + 1] == "t":    # handle tab escape char
                print('\t', end="")
                i += 1
            else:
                print(string[i], end="")                        # print noraml
            i += 1

    # print a variable from symbol table
    if tok[0][0] == 1 and tok[1][0] == 31 and tok[2][0] == 0:
        prt = ""
        for i in userVars:
            if i[0] == tok[1][1]:                               # find variable
                prt = i[1]                                      # get variable value
        print(prt)                                              # print variable
    else:
        return tok[3:]
    return tok[3:]

# <input>
def parseInput(tok, userVars):
    if tok[0][0] == 2 and tok[1][0] == 31 and tok[2][0] == 0:
        val = input(' ')                            # enter value
        if val[0] == "-":                           # if negative integer input
            userVars.append([tok[1][1], int(val)])  # store value with id token
        if val.isdigit():                           # if positive integer input
            userVars.append([tok[1][1], int(val)])  # store value with id token
        if val.isalpha():                           # if character or str input
            userVars.append([tok[1][1], val])       # store value with id token

    return tok[3:]

# <assign>
def parseAssign(tok, userVars):
    # ID "=" <expr>;
    # assign ID with the result of experssion
    # can be variable, INT, BOOL, CHAR

    var = tok[0][1]                         # store ID into variable
    val = parseExpr(0, tok[2:], userVars)   # retrieve value of the variable
    userVars.append([var, val])             # add user varaible to symbol table

    count = 0
    for i in tok:
        if i[0] == 0:
            indexSemi = count               # locate semicolon
            break
        count = count + 1

    return tok[indexSemi + 1:]              # tokens after semicolon

# <if>
def parseIf(tok, userVars):
    expr = parseExpr(0,tok[1:], userVars)   # evaluate expression
    tok = tok[2:]                           # evaluate from "then" onward

    # find index of else
    count = 0
    for i in tok:
        if i[0] == 6:
            indexElse = count
            break
        count = count + 1

    # find index of end
    count = 0
    for i in tok:
        if i[0] == 7:
            indexEnd = count
            break
        count = count + 1

    # if expression evaluates to 1 only execute code after "then" token - not else
    if expr == 1:
        del tok[indexElse: indexEnd + 1]        # remove tokens from else -> end

        count = 0
        for i in tok:
            if i[0] == 5:
                indexThen = count               # index of "then" token
                break
            count = count + 1
        
        tok = tok[indexThen+1:]                 # remove "then"
        return tok                              # return remaining statements
    
    # if expression evaluates to 0 only execute code after "else" token - not then
    elif expr == 0:
        del tok[indexEnd]                       # remove end token
        del tok[0:indexElse+1]                  # remove tokens before else
        return tok                              # return remaining statements

# <stmt>
def parseStmt(tok, userVars):
    if tok[0][0] == 1:                          # <print>
        ret = parsePrint(tok, userVars)
    elif tok[0][0] == 2:                        # <input>
        ret = parseInput(tok, userVars)
    elif tok[0][0] == 31 and tok[1][0] == 3:    # <assign>
        ret = parseAssign(tok, userVars)
    elif tok[0][0] == 4:                        # <if>
        ret = parseIf(tok, userVars)
    elif tok[0][0] == 29:                       # EOF
        return 0, tok
    else:                                       # ERROR
        return 1, tok
    return parseStmt(ret, userVars)             # recursive call with updated input (next <stmt>)

# <stmt_list>
def parseStmtList(tok):
    ret = (parseStmt(tok, userVars))[0]         # call <stmt>
    if ret == 1:
        return 1
    else:
        return 0

# TEST DRIVER #
def main():
    with open(str(sys.argv[1]), 'r') as file:   # open file passed as cmd line arg
        tok = file.read().replace('\n', '')     # read and store contents to string, replace \n with space

    tokens = []                                 # store tokens from lexing process
    temp = nextToken(tok)                       # determine first lexeme from string

    while temp[0][0] != ENDSTREAM and temp[0][0] != ERROR:
        tokens.append(temp[0])                  # append token ID to the list
        temp = nextToken(temp[1])               # get next token

        if temp[0][0] == ERROR:                 # if error recieved
            tokens.append(temp[0])              # appen ENDSTREAM ID to the list
            print("Lexer Error: " + temp[0][1]) # print error response

    if temp[0][0] != ERROR:
        tokens.append(temp[0])
        ret = parseStmtList(tokens)             # PARSING BEGINS HERE - call to <stmt_list>

if __name__ == "__main__":
    main()