#           Needed for inport of common.py
##############################################################
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 
from common import common
##############################################################

one_dig_seperators=[',',';','(',')','[',']','+','-','/','*',':','.']
two_dig_seperators=[":=","<=","<=","==","!=","//"]

tokens = []


filename = "../test0.src"

source_file = open(filename, 'r')




# Enum used for types to prevent passing around strings.
# reserved_word = ["PROGRAM","IS","VARIABLE","BEGIN","END",".","//"]
# reserved_types =["INTEGER","BOOL","FLOAT","STRING","CHAR","ID"]
# control_words = ["IF","THEN","ELSE","FOR","WHILE","SWITCH","CASE"]
# mult_op = ["*","/","DIV","MOD","AND"]
# add_op = ["+","-","OR"]
# assign_op = [":="]
# re_op=["=","!=","<","<=",">=",">"]
# id = starts with letter than letters and or digitis
# digit = 0-9
# letter = az and A-Z

# num is digits,optional_fraction,optional_exponent
# digits = digit and any number of other digits
# opetional_fraction = .plus digits

def identify_token(token_text_lower):
    token_text = token_text_lower.upper()

    # Start with a token of Invalid type and hopefully identify before sending
    # Only certain tokens such as number, and id will need a value
    return_token = common.token(common.token_types.t_INVALID,None);

    if token_text=="PROGRAM":
        return_token.type = common.token_types.t_PROGRAM
    elif token_text=="IS":
        return_token.type = common.token_types.t_IS
    elif token_text=="VARIABLE":
        return_token.type = common.token_types.t_VARIABLE
    elif token_text=="BEGIN":
        return_token.type = common.token_types.t_BEGIN
    elif token_text=="END":
        return_token.type = common.token_types.t_END
    elif token_text==".":
        return_token.type = common.token_types.t_DOT       
    elif token_text=="//":
        return_token.type = common.token_types.t_LINE_COMMENT
    elif token_text=="INTEGER":
        return_token.type = common.token_types.t_INTEGER
    elif token_text=="BOOL":
        return_token.type = common.token_types.t_BOOL
    elif token_text=="FLOAT":
        return_token.type = common.token_types.t_FLOAT
    elif token_text=="STRING":
        return_token.type = common.token_types.t_STRING
    elif token_text=="CHAR":
        return_token.type = common.token_types.t_CHAR
    elif token_text=="IF":
        return_token.type = common.token_types.t_IF
    elif token_text=="THEN":
        return_token.type = common.token_types.t_THEN
    elif token_text=="ELSE":
        return_token.type = common.token_types.t_ELSE
    elif token_text=="FOR":
        return_token.type = common.token_types.t_FOR
    elif token_text=="WHILE":
        return_token.type = common.token_types.t_WHILE
    elif token_text=="SWITCH":
        return_token.type = common.token_types.t_SWITCH
    elif token_text=="CASE":
        return_token.type = common.token_types.t_CASE
    elif token_text=="GLOBAL":
        return_token.type = common.token_types.t_GLOBAL
    elif token_text=="*":
        return_token.type = common.token_types.t_MULT_OP
    elif token_text=="/":
        return_token.type = common.token_types.t_DIVIDE_OP
    elif token_text=="AND":
        return_token.type = common.token_types.t_AND
    elif token_text=="+":
        return_token.type = common.token_types.t_ADD_OP
    elif token_text=="-":
        return_token.type = common.token_types.t_SUBTRACT_OP
    elif token_text=="OR":
        return_token.type = common.token_types.t_OR
    elif token_text==":=":
        return_token.type = common.token_types.t_ASSIGN
    elif token_text=="=":
        return_token.type = common.token_types.t_EQUALS
    elif token_text=="<":
        return_token.type = common.token_types.t_LESS_THAN
    elif token_text=="<=":
        return_token.type = common.token_types.t_LESS_THAN_OR_EQUAL
    elif token_text==">":
        return_token.type = common.token_types.t_GREATER_THAN
    elif token_text==">=":
        return_token.type = common.token_types.t_GREATER_THAN_OR_EQUAL
    elif token_text==":":
        return_token.type = common.token_types.t_COLON
    elif token_text==";":
        return_token.type = common.token_types.t_SEMI_COLON
    elif token_text=="(":
        return_token.type = common.token_types.t_LEFT_PAREN
    elif token_text==")":
        return_token.type = common.token_types.t_RIGHT_PAREN
    elif token_text=="[":
        return_token.type = common.token_types.t_LEFT_BRACKET
    elif token_text=="]":
        return_token.type = common.token_types.t_RIGHT_BRACKET
    elif token_text=="TRUE":
        return_token.type = common.token_types.t_TRUE
    elif token_text=="FALSE":
        return_token.type = common.token_types.t_FALSE

    elif token_text.isnumeric():
        return_token.type = common.token_types.t_NUMBER
        return_token.value = token_text
    elif token_text[0].isalpha():
        return_token.type = common.token_types.t_ID
        return_token.value = token_text
    return return_token

def getNextToken():
    word = ""
    textMode=False
    commentMode=False
    while 1:
        # Read two characters. Peek does not advance the iterator
        cur_char = getNextChar()
        next_char = peekNextChar()

        # If not valid char, most likely end of file
        if not cur_char:
            return None

        # Add the the current "word", only if special case modes are not active and it is not a comment
        if textMode==False and commentMode==False and cur_char+next_char!="//":

            # First check if cur_char is a one or two digit pre-defined token
            if cur_char+next_char in two_dig_seperators:
                # Make a pointless read to advance the iterator that was peeked
                temp = getNextChar()
                return identify_token(cur_char+next_char)
            elif cur_char in one_dig_seperators:
                return identify_token(cur_char)

            # Do not add spaces, tabs newlines etc to word
            if not isWhitespace(cur_char):
                word = word + cur_char

            # If the next chatacter is whitespace or a seperator, our current word is over
            if next_char in one_dig_seperators or isWhitespace(next_char):
                if word!="":
                    return identify_token(word)
            # textMode allows for quotations that will not get chopped by the lexer
            if cur_char=='"':
                textMode=True
        else:
            # Start ignoring all characters for comments
            if cur_char+next_char=="//":
                commentMode=True
            # Comments end at the end of the line, add multi-line comment support later
            if commentMode==True:
                if cur_char=='\n':
                    commentMode=False

            if textMode==True:
                word=word+cur_char
                if cur_char=='"':
                    textMode=False



def getNextChar():
    char = source_file.read(1)
    return char

# Chapter 3.2 Dragon book
# Used two-digit tokens
def peekNextChar():
    pos = source_file.tell()
    char = source_file.read(1)
    source_file.seek(pos)
    return char

def printTokens():
    tempIndex=0
    for token in tokens:
        print(str(tempIndex)+" "+token)
        tempIndex=tempIndex+1

def isWhitespace(inChar):
    if inChar==' ' or inChar=='\t' or inChar=='\n' or inChar=='\v' or inChar=='\f' or inChar=='\r':
        return True
    return False


# i=0
# while True:
#     result = getNextToken()
#     if result==None:
#         break
#     print(str(i)+": "+str(result.type)+" "+str(result.value))
#     if result.type==common.token_types.t_INVALID:
#       print("Error")
#       exit()
#     i=i+1
# source_file.close()

