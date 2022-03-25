# Author        : Milan Gulati
# Description   : Lexer and Tokenizer
# README.txt for instructions on how to run. 

import sys

########### Token and Lexeme Codes ###########

ERROR = -1          # ERROR
SEMICOLON = 0       # ;
PRINT = 1           # print
GET = 2             # get
EQUAL = 3           # =
IF = 4              # if
THEN = 5            # then
ELSE = 6            # else
END = 7             # end
WHILE = 8           # while
DO = 9              # do
FOR = 10            # for
AND = 11            # and
OR = 12             # or
PLUS = 13           # +
MINUS = 14          # -
MULT = 15           # *
DIV = 16            # /
MOD = 17            # %
GREATERTHAN = 18    # >
GREATERTHANEQL = 19 # >=
LESSTHAN = 20       # <
LESSTHANEQL = 21    # <=
EQUALEQUAL = 22     # ==
NOTEQUAL = 23       # !=
PARENOPEN = 24      # (
PARENCLOSE = 25     # )
NOT = 26            # !
TRUE = 27           # True - Boolean variable
FALSE = 28          # False - Boolean variable
ENDSTREAM = 29      # Endstream of input
STRING_TOKEN = 30   # String token
ID_TOKEN = 31       # ID token
INT_TOKEN = 32      # INT token
BOOL_TOKEN = 33     # BOOL token
CHAR_TOKEN = 34     # CHAR token

NAMES = ["SEMICOLON", "PRINT", "GET", "EQUAL", "IF", "THEN", "ELSE", "END", "WHILE", "DO", "FOR", "AND", "OR", "PLUS", 
        "MINUS", "MULT", "DIV", "MOD", "GREATERTHAN", "GREATERTHANEQL", "LESSTHAN", "LESSTHANEQL", "EQUALEQUAL", 
        "NOTEQUAL", "PARNOPEN", "PARENCLOSE", "NOT", "TRUE", "FALSE", "ENDSTREAM", "STRING_TOKEN", "ID_TOKEN",
        "INT_TOKEN", "BOOL_TOKEN", "CHAR_TOKEN"]

########### TOKEN CATEGORIES ###########

# determine start of processing
# returns True or False
def startID(c):
    return c == "_" or c.isalpha()

# determine if the char is part of an id (valid for regex: [_a-zA-Z][_a-zA-Z0-0]*)
# returns True or False
def isIdChar(c):
    return c == "_" or c.isalpha() or c.isdigit()

# determine if the start of a string
# returns True or False
def startString(c):
    return c == '"'

# determine if the start of a char token
# returns True or False
def startChar(c):
    return c == "'"

# determine what keyword the lexeme is
# returns the appropriate token given the name
def tokenKeyWord(input, name):
    
    token = input[0]
    i = 1
    while i < len(input) and isIdChar(input[i]):    # while input is longer than i and is a character
        token = token + input[i]                    # append char to token
        i = i + 1                                   # increment counter
    if name == "print":                     # print keyword
        return [[PRINT, token], input[i:]]
    elif name == "get":                     # get keyword
        return [[GET, token], input[i:]]
    elif name == "if":                      # if keyword
        return [[IF, token], input[i:]]        
    elif name == "then":                    # then keyword
        return [[THEN, token], input[i:]]
    elif name == "else":                    # else keyword
        return [[ELSE, token], input[i:]]
    elif name == "end":                     # end keyword
        return [[END, token], input[i:]]
    elif name == "while":                   # while keyword
        return [[WHILE, token], input[i:]]
    elif name == "do":                      # do keyword
        return [[DO, token], input[i:]]
    elif name == "for":                     # for keyword
        return [[FOR, token], input[i:]]
    elif name == "and":                     # and keyword
        return [[AND, token], input[i:]]
    elif name == "or":                      # or keyword
        return [[OR, token], input[i:]]
    elif name == "True":                    # True boolean keyword
        return [[TRUE, token], input[i:]]
    elif name == "False":                   # False boolean keyword
        return [[FALSE, token], input[i:]]     
    elif name == ">=":                      # greater than equal comparison
        return [[GREATERTHANEQL, token], input[i:]]   
    elif name == "<=":                      # less than equal comparison
        return [[LESSTHANEQL, token], input[i:]]
    elif name == "==":                      # equal equal comparison
        return [[EQUALEQUAL, token], input[i:]]
    elif name == "!=":                      # not equal to comparison
        return [[NOTEQUAL, token], input[i:]]

# handle ID token processing
def tokenID(input):

    token = input[0]    # first char of input
    i = 1
    while i < len(input) and isIdChar(input[i]):
        token = token + input[i]
        i = i + 1
    if(token == "end"):         # special case for end must be checked, in case "end;" is not at EOF
        return [[END, token], input[i:]]
    elif(token == "True"):      # special case for True must be checked
        return [[TRUE, token], input[i:]]
    elif(token == "False"):     # special case for False must be checked
        return [[FALSE, token], input[i:]]
    else:                       # else just return the normal ID token
        return [[ID_TOKEN, token], input[i:]]

# handle int token processing
def tokenInteger(input):

    token = input[0]    # first char of input
    i = 1
    while i < len(input) and input[i].isdigit():    # while input is digit
        token = token + input[i]                    # append char to token
        i = i + 1
    return [[INT_TOKEN, int(token)], input[i:]]     # convert token to int val and return

# handle string token processing
def tokenString(input):

    endQuote = input.find('\"', 1)                                          # find end quote location
    if endQuote == -1:
        return [[ERROR, "Not a recognized symbol..."], input[0:]]           # ERROR - only a single quote

    token = input[0:endQuote+1]                                             # extract string token
    if len(token) >= 2 and token.startswith('"') and token.endswith('"'):   # verify string token and return
        return [[STRING_TOKEN, token], input[len(token):]]

# handle char token processing
def tokenChar(input):

    if input[2] != "'":
        return [[ERROR, "Not a recognized symbol..."], input[0:]]           # ERROR - only a single quote

    if len(input[0:3]) != 3:                                                # lexeme starts with single quote, but does not fit the format 'c'
        return [[ERROR, "Not a recognized symbol..."], input[0:]]           # ERROR - too many chars

    token = input[0:3]                                                      # lexeme will be 3 characters long (example: 'c')
    if len(token) == 3 and token.startswith("'") and token.endswith("'"):   # verify char token and return
        return [[CHAR_TOKEN, token], input[3:]]

########### DETERMINE NEXT TOKEN OF INPUT ###########

# input string is passed into this function
# lexeme is checked against keywords, comparisons, and token categories
# appropriate category is returned to the main funciton
def nextToken(input):

    i = 0
    while i < len(input) and input[i].isspace():    # ensure input not whitespace
        i = i + 1
    if i >= len(input):                             # if end of input
        return [[ENDSTREAM, None], []]              # return ENDSTREAM code

    # check if lexeme is a keyword or multi-char condition
    # split input by whitespace to get first word and check for each
    elif input.split()[0] == "print":
        return tokenKeyWord(input[i:], "print")
    elif input.split()[0] == "get":
        return tokenKeyWord(input[i:], "get")
    elif input.split()[0] == "if":
        return tokenKeyWord(input[i:], "if") 
    elif input.split()[0] == "then":
        return tokenKeyWord(input[i:], "then")    
    elif input.split()[0] == "else":
        return tokenKeyWord(input[i:], "else")
    elif input.split()[0] == "end":
        return tokenKeyWord(input[i:], "end")
    elif input.split()[0] == "while":
        return tokenKeyWord(input[i:], "while")
    elif input.split()[0] == "do":
        return tokenKeyWord(input[i:], "do")
    elif input.split()[0] == "for":
        return tokenKeyWord(input[i:], "for")
    elif input.split()[0] == "and":
        return tokenKeyWord(input[i:], "and")
    elif input.split()[0] == "or":
        return tokenKeyWord(input[i:], "or")
    elif input.split()[0] == "True":
        return tokenKeyWord(input[i:], "True")
    elif input.split()[0] == "False":
        return tokenKeyWord(input[i:], "False")
    elif input.split()[0] == ">=":
        return tokenKeyWord(input[i + 1:], ">=")    
    elif input.split()[0] == "<=":
        return tokenKeyWord(input[i + 1:], "<=")    
    elif input.split()[0] == "==":
        return tokenKeyWord(input[i + 1:], "==")    
    elif input.split()[0] == "!=":
        return tokenKeyWord(input[i + 1:], "!=")    

    # check if lexeme is a symbol or single-char condition
    # check a single character
    elif input[i] == ";":
        return [[SEMICOLON], input[i + 1:]]
    elif input[i] == "=":
        return [[EQUAL], input[i + 1:]]
    elif input[i] == "+":
        return [[PLUS], input[i + 1:]]
    elif input[i] == "-":
        return [[MINUS], input[i + 1:]]
    elif input[i] == "*":
        return [[MULT], input[i + 1:]]
    elif input[i] == "/":
        return [[DIV], input[i + 1:]]
    elif input[i] == "%":
        return [[MOD], input[i + 1:]]
    elif input[i] == ">":
        return [[GREATERTHAN], input[i + 1:]]
    elif input[i] == "<":
        return [[LESSTHAN], input[i + 1:]]
    elif input[i] == "(":
        return [[PARENOPEN], input[i + 1:]]
    elif input[i] == ")":
        return [[PARENCLOSE], input[i + 1:]]
    elif input[i] == "!":
        return [[NOT], input[i + 1:]]

    # check if lexeme is a token category
    # use appropriate function to test start of input and categorize accordingly
    elif startChar(input[i]):         # if the input starts with '
        return tokenChar(input[i:])     # pass input to token char function
    elif startString(input[i]):       # if the input starts with "
        return tokenString(input[i:])   # pass input to token string function
    elif startID(input[i]):           # if input starts with regex of ID
        return tokenID(input[i:])       # pass to token ID function
    elif input[i].isdigit():            # if input start with digit
        return tokenInteger(input[i:])  # pass to token integer function
    else:                               # lexeme did not fit any category
        return [[ERROR, "Not a recognized symbol..."], input[i:]]   # ERROR


########### TEST DRIVER PORTION ###########

# print token function
# if token number > 29 it is user input determined
def printLex(t):
    if t[0] >= 29:
        print(NAMES[t[0]] + "(" + str(t[1]) + ")")          # print user input token
    else:
        print(NAMES[t[0]])                                  # print keyword, condition, or symbol

########### MAIN FUNCTION ###########

def main():

    #### comment out next two lines to hardcoded input instead of file: ####
    with open(str(sys.argv[1]), 'r') as file:                   # open file passed as cmd line arg
        input = file.read().replace('\n', '')                   # read and store contents to string, replace \n with space

    #### uncomment and modify to use hardcoded input instead of file: ####
    #input = 'input here'

    temp = nextToken(input)                                     # determine first lexeme from input string

    # print token while not end of file and not an error
    while temp[0][0] != ENDSTREAM and temp[0][0] != ERROR:      # while not EOF and not ERROR
        printLex(temp[0])                                       # print determined token
        temp = nextToken(temp[1])                               # get next token

    if temp[0][0] == ERROR:                                     # if error recieved
        print("Lexer Error: " + temp[0][1])                     # print error response

if __name__ == "__main__":
    main()