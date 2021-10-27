import visualizeTree as vt

src_file = open("source.txt",'r')

lookahead="hhhh"

###############################################################################################
###############################################################################################
##                      ADD STATEMENT_LIST and DECLARATION_LIST as symbols
##                            maybe "symbols" is not the right word
###############################################################################################
###############################################################################################

class Node(object):
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

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

def match(token_text):
  global lookahead
  if lookahead==token_text:
    lookahead=get_token()
    return True
  else:
    if token_text=="<number>" and lookahead.isnumeric():
      print("Returning True for a number")
      lookahead=get_token()
      return True
    print("No match for", lookahead, token_text)
    return False

def get_token():
  global lookahead
  print("Current Token: "+lookahead)
  return src_file.readline().strip()

def program_header(parent_node):
  new_node = Node("program_header")
  if match("program") and match("test_program") and match("is"):
    parent_node.add(new_node)
    return True
  else:
    #print("No header")
    return False

def variable_declaration(parent_node):
  new_node = Node("Variable_Declaration")
  if match("variable") and (match("a") or match("b")) and match(":") and (match("integer") or match("bool")):
    parent_node.add(new_node)
    return True
  return False
  
def procedure_declaration(parent_node):
  return False

def declaration_list(parent_node):
  global lookahead
  new_node = Node("declaration_list")

  if lookahead=="variable":
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

def assignment_statement(parent_node):
  new_node = Node("assignment_statement")
  if (match("a") or match("b")) and match(":=") and match("<number>"):
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
  new_node = Node("return_statement")
  if match("return") and expression(new_node):
    parent_node.add(new_node)
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

  if lookahead=="a" or lookahead=="b" or lookahead=="for" or lookahead=="return" or lookahead=="if":
    statement(new_node)
    match(";")
    statement_list(new_node)
    parent_node.add(new_node)
    return True
  return False
    

def program_body(parent_node):
  new_node = Node("program_body")
  global lookahead

  declaration_list(new_node)
  match(";")

  match("begin")

  statement_list(new_node)
  match(";")
  
  if  match("end") and match("program") and match("."):
    parent_node.add(new_node)
    return True
  return False



def program(parent_node):
  new_node = Node("program")
  global lookahead
  if program_header(new_node) and program_body(new_node):
    parent_node.add(new_node)
    return True
  else:
    return False


def main():
  global lookahead
  lookahead = get_token()

  start_node = Node("root")
  if program(start_node):
    print("Success!!")

    #print("------Printing Preorder------\n")
    #printPreorder(start_node)

    viz = vt.ParseTreeVisualizer()
    viz.gendot(start_node)

  else:
    print("Error in program")

main()
