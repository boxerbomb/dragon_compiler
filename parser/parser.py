import visualizeTree as vt

src_file = open("source.txt",'r')

lookahead="Uninitialized"

###############################################################################################
###############################################################################################
##               Currently Tokens are just strings
##                Change to a token type with more information
###############################################################################################
###############################################################################################

class Node(object):
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None
        self.info = None

    def add(self, node):
       #No detection for adding one than two nodes
        if self.left==None:
          self.left = node
        elif self.right == None:
          self.right = node
        else:
          print("Attempt to add " + node.name + " to " + self.name+" when left and right nodes are full")
          print("Current Left: "+self.left.name+" Current Right: "+self.right.name)
          exit()

    def add_info(self, infoNode):
      self.info = infoNode

    def get_left(self):
      return self.left

    def get_right(self):
      return self.right


def printPreorder(root):
  root_right_name = "NONE"
  root_left_name = "NONE"
  if root:
    if root.left:
      root_left_name = root.left.name
    if root.right:
      root_right_name = root.right.name
    print(root.name+" has left node: "+root_left_name+" and right node: "+root_right_name)
    print()

    printPreorder(root.left)
    printPreorder(root.right)


# Trying to not use as many classes as I am unsure of what language I will use
matchStack = []
def match(token_text):
  global lookahead
  if lookahead==token_text:
    matchStack.append(lookahead)
    lookahead=get_token()
    return True
  else:
    if token_text=="<number>" and lookahead.isnumeric():
      print("Returning True for a number")
      matchStack.append(lookahead)
      lookahead=get_token()
      return True
    elif token_text=="<id>" and lookahead[0].isalpha():
      matchStack.append(lookahead)
      lookahead=get_token()
      return True
    print("No match for", lookahead, token_text)
    return False

def get_token():
  next_token = src_file.readline().strip() 
  print("Working on: "+next_token)
  return next_token

def program_header(parent_node):
  new_node = Node("program_header")
  if match("program") and id(new_node) and match("is"):
    parent_node.add(new_node)
    return True
  else:
    #print("No header")
    return False

def variable_declaration(parent_node):
  new_node = Node("Variable_Declaration")
  if match("variable") and id(new_node) and match(":") and type_mark(new_node):
    parent_node.add(new_node)
    return True
  return False

def type_mark(parent_node):
  new_node = Node("type_mark")
  if match("integer") or match("float") or match("string") or match("bool"):
    new_node.add(Node(matchStack.pop()))
    parent_node.add(new_node)
    return True
  return False

def parameter_list(parent_node):
  global lookahead
  new_node = Node("parameter_list")

  if lookahead=="variable":
    parameter(new_node)
    match(";")
    parameter_list(new_node)
    match(";")
    parent_node.add(new_node)
    return True
  return False

def parameter(parent_node):
  new_node = Node("parameter")
  if variable_declaration(new_node):
    return True
  return False

def procedure_header(parent_node):
  new_node = Node("procedure_header")
  temp_node = Node("")
  if match("procedure") and id(temp_node) and match(":") and type_mark(new_node) and match("("):
    matchStack.pop()
    matchStack.pop()
    matchStack.pop()
    function_name = matchStack.pop()
    parameter_list(new_node)
    if match(")"):
      parent_node.add(new_node)
      return True
    print("Fatal Error: Incomplete without the ')'")
    exit()
  return False

def procedure_body(parent_node):
  new_node = Node("procedure_body")
  declaration_list(new_node)
  match(";")

  match("begin")

  statement_list(new_node)
  match(";")

  return_statement(new_node)
  match(";")
    
  if  match("end") and match("procedure"):
    parent_node.add(new_node)
    return True
    
def procedure_declaration(parent_node):
  new_node = Node("procedure_delcaration")
  if procedure_header(new_node) and procedure_body(new_node):
    parent_node.add(new_node)
    return True
  return False

def declaration_list(parent_node):
  global lookahead
  new_node = Node("declaration_list")

  if lookahead=="variable" or lookahead=="global" or lookahead=="procedure":
    declaration(new_node)
    match(";")
    declaration_list(new_node)
    parent_node.add(new_node)
    return True
  return False

def declaration(parent_node):
  new_node = Node("declaration")
  match("global")
  if variable_declaration(new_node) or procedure_declaration(new_node):
    parent_node.add(new_node)
    return True
  return False

# A little trouble shooting out how "primes" work in relation to left-recursion elimination.
# This is something to keep an eye on
# This is a pretty decent webpage on the subject https://www.csd.uwo.ca/~mmorenom/CS447/Lectures/Syntax.html/node8.html
# arith_op = arithop + relation
# arith_op = arithop - relation
# arith_op = relation

# E = E+T | E
# T = id

# E = T and Eprime
# Eprime = + and T and Eprime | nothing
 
# arith_op = match(relation) and arith_op_prime
# arith_op_prime = ((match("+") or match("-")) and relation and arith_op_prime) or nothing
#5 + 2 - 1 + 9
def arith_op(parent_node):
  new_node = Node("arith_op")
  print("arith op right now")
  if relation(new_node) and arith_op_prime(new_node):
    parent_node.add(new_node)
    return True
  return False

def arith_op_prime(parent_node):
  new_node = Node("arith_value")
  if (match("+") or match("-")):
    operation_name = matchStack.pop()
    if relation(new_node) and arith_op_prime(new_node):
      parent_node.name = operation_name
      parent_node.add(new_node)
      return True
  return True


####  Left Recursion Elimination Notes  ####
# term = term (* or /) Factor
# term = Factor

# term = match(factor) and term_prime
# term_prime = (match("*") or match("/")) and factor() and term_prime
# term_prime = empty
def term(parent_node):
  new_node = Node("term")
  if factor(new_node) and term_prime(new_node):
    print("In here")
    parent_node.add(new_node)
    return True
  return False

def term_prime(parent_node):
  new_node = Node("term_prime")
  if (match("*") or match("/")) and factor(new_node) and term_prime(new_node):
    parent_node.name =- matchStack.pop()
    parent_node.add(new_node)
    return True
  return True




def relation(parent_node):
  new_node = Node("relation")
  if term(new_node):
    #new_node.name=matchStack.pop()
    parent_node.add(new_node)
    return True
  return False

def factor(parent_node):
  new_node = Node("factor")

  if match("(") and expression(new_node) and match(")"):
    parent_node.add(new_node)
    return True
  if procedure_call(new_node):
    parent_node.add(new_node)
    return True
  if string(new_node):
    parent_node.add(new_node)
    return True
  if match("true"):
    new_node.name = "True"
    parent_node.add(new_node)
    return True
  if match("false"):
    new_node.name = "False"
    parent_node.add(new_node)
    return True

  # Optional Minus sign
  match("-")
  if name(new_node):
    parent_node.add(new_node)
    return True
  if number(new_node):
    parent_node.add(new_node)
    return True
  
  return False


def string(parent_node):
  new_node = Node("")
  if match("<string>"):
    new_node.name = matchStack.pop()
    parent_node.add(new_node)
    return True
  return False

def number(parent_node):
  new_node = Node("")
  if match("<number>"):
    new_node.name = matchStack.pop()
    parent_node.add(new_node)
    return True
  return False

def name(parent_node):
  new_node = Node("name")
  if id(new_node):
    if match("[") and expression(new_node) and match("]"):
      matchStack.pop()
      new_node.name = new_node.name + matchStack.pop()
    parent_node.add(new_node)
    return True
  return False
  

def procedure_call(parent_node):
  print("Update Procedure Call function")
  return False


# Expression is another example of needing a "prime"
def expression(parent_node):
  new_node = Node("expression")
  if match("not"):
    print("This should be fixed")
    exit()
  if arith_op(new_node) and expression_prime(new_node):
    parent_node.add(new_node)
    return True
  return False

def expression_prime(parent_node):
  print("HERE RIGHT NOW")
  new_node = Node("")
  if match("&") and expression(new_node):
    new_node.name = "& (and)"
    parent_node.add(new_node)
    return True
  elif match("|") and expression(new_node):
    new_node.name = "| (or)"
    parent_node.add(new_node)
  else:
    return True
    

def assignment_statement(parent_node):
  new_node = Node("assignment_statement")
  #if (match("a") or match("b")) and match(":=") and match("<number>"):
  print("Trying out expression, this might cause errors")
  if id(new_node) and match(":="):
    if expression(new_node):
      parent_node.add(new_node)
      return True
  return False

def if_statement(parent_node):
  new_node = Node("if_statement")
  return False

def loop_statement(parent_node):
  new_node = Node("loop_statment")

  # more_statement=True
  # if match("for") and match("(") and assignment_statement(new_node) and match(";") and expression(new_node):
  #   while more_statement:
  #     more_statement=statement(new_node)

  statement_list(new_node)
  match(";")

  if match("end") and match("for"):
    parent_node.add(new_node)
    return True
    
  return False

def return_statement(parent_node):
  print("In Fucntion Return_statatemtn")
  new_node = Node("return_statement")
  if match("return") and expression(new_node):
    parent_node.name = "Return Statement Found"
    print("The two branch appoach is starting to be an issue.")
    print("Either way it seems like the best approach might be to either a seperate tree for each function")
    print("Or create a very long invisible link between the two. Invsiible links are a real thing in graphviz")
    return True
  return False


def statement(parent_node):
  new_node = Node("statement")
  if assignment_statement(new_node) or if_statement(new_node) or loop_statement(new_node) or return_statement(new_node):
    parent_node.add(new_node)
    return True
  return False

def statement_list(parent_node):
  global lookahead
  new_node = Node("statement_list")

  if lookahead=="a" or lookahead=="b" or lookahead=="y" or lookahead=="x" or lookahead=="for" or lookahead=="if":
    statement(new_node)
    match(";")
    statement_list(new_node)
    match(";")
    parent_node.add(new_node)
    return True
  return False
    

def program_body(parent_node):
  new_node = Node("program_body")

  declaration_list(new_node)
  match(";")

  match("begin")

  statement_list(new_node)
  match(";")
  
  if  match("end") and match("program") and match("."):
    parent_node.add(new_node)
    return True
  return False


def id(parent_node):
  new_node = Node("id")
  if match("<id>"):
    new_node.name = new_node.name + " : "+matchStack.pop()
    parent_node.add(new_node)
    return True
  return False



def program(parent_node):
  new_node = Node("program")
  if program_header(new_node) and program_body(new_node):
    parent_node.add(new_node)
    return True
  else:
    return False


def main():
  global lookahead
  lookahead = get_token()

  start_node = Node("root")

  # Kicks off the entire parseing
  if program(start_node):
    print("Success!!")

    #print("------Printing Preorder------\n")
    #printPreorder(start_node)

    viz = vt.ParseTreeVisualizer()
    viz.gendot(start_node)

  else:
    print("Error in program")

main()
