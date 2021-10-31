from dataclasses import dataclass

one_dig_seperators=[',',';','(',')','[',']','+','-','/','*']
two_dig_seperators=[":=","<=","<=","==","!=","//"]

tokens = []


filename = "../test0.src"

source_file = open(filename, 'r')

@dataclass
class token:
    type: str
    value: str


reserved_word = ["PROGRAM","IS","VARIABLE","BEGIN","END",".","//"]
reserved_types =["INTEGER","BOOL"]
mult_op = ["*","/","DIV","MOD","AND"]
add_op = ["+","-"."OR"]
assign_op = [":="]
re_op=["=","!=","<","<=",">=",">"]
# id = starts with letter than letters and or digitis
# digit = 0-9
# letter = az and A-Z

# num is digits,optional_fraction,optional_exponent
# digits = digit and any number of other digits
# opetional_fraction = .plus digits

def identify_token(token_text):
    
    return token(token_text,"12")

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

for i in range(200):
    result = getNextToken()
    if result==None:
        break
    print(str(i)+": "+result.type+" "+result.value)
source_file.close()

