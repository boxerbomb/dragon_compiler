import visualizeTree as vt


#           Needed for inport of common.py
##############################################################
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 
from common import common
##############################################################

from lexer import lexer
from code_gen import code_generator


###############################################################################################
###############################################################################################
##               
##                        Global Vars               
## 
###############################################################################################
###############################################################################################
root_nodes = []
###############################################################################################
###############################################################################################


class Node(object):
    def __init__(self, name, in_type=None):
        self.type = in_type
        self.name = name
        self.children = []

    def add(self, node):
      self.children.append(node)
      if len(self.children)>2:
        print("WARNING: More than 2 nodes added on: "+self.name)


# Trying to not use as many classes as I am unsure of what language I will use
matchStack = []
def match(token_type):
  global lookahead
  if lookahead.type==token_type:

    # Do not add parenthese to the matchstack. This causes issues with finding the correct Divide/Multiply Operator in the Stack
    if lookahead.type==common.token_types.t_LEFT_PAREN or lookahead.type==common.token_types.t_RIGHT_PAREN:
      pass
    else:
      matchStack.append(lookahead)


    print("Matched :"+str(lookahead.type)+" to: "+str(token_type))
    lookahead=get_token()
    return True
  else:
    #print("Current Token: ", lookahead.type,"attempting", token_type)
    return False

def get_token():
  return lexer.getNextToken()

def program_header(parent_node):
  new_node = Node("program_header")
  if match(common.token_types.t_PROGRAM) and id(new_node) and match(common.token_types.t_IS):
    parent_node.add(new_node)
    return True
  else:
    #print("No header")
    return False

def bound(parent_node, in_type=None):
  new_node = Node("bound",in_type)
  if number(new_node):
    parent_node.add(new_node)
    return True
  return False

def variable_declaration(parent_node):
  new_node = Node("Variable_Declaration")
  if match(common.token_types.t_VARIABLE) and id(new_node,"variable_name") and match(common.token_types.t_COLON) and type_mark(new_node,"type"):
    # Optional bound
    if match(common.token_types.t_LEFT_BRACKET) and bound(new_node,"bound") and match(common.token_types.t_RIGHT_BRACKET):
      parent_node.add(new_node)
      return True

    # No bound
    parent_node.add(new_node)
    return True
  return False

def type_mark(parent_node,in_type=None):
  new_node = Node("type_mark",in_type)
  if match(common.token_types.t_INTEGER) or match(common.token_types.t_FLOAT) or match(common.token_types.t_FLOAT) or match(common.token_types.t_BOOL) or match(common.token_types.t_STRING):
    new_node.add(Node(matchStack.pop().type))
    parent_node.add(new_node)
    return True
  return False

def parameter_list(parent_node):
  new_node = Node("parameter_list")

  if parameter(new_node):
    match(common.token_types.t_SEMI_COLON)
    parameter_list(new_node)
    match(common.token_types.t_SEMI_COLON)
    parent_node.add(new_node)
    return True
  return False

def parameter(parent_node):
  new_node = Node("parameter")
  if variable_declaration(new_node):
    parent_node.add(new_node)
    return True
  return False

def procedure_header(parent_node):
  new_node = Node("procedure_header")
  if match(common.token_types.t_PROCEDURE) and id_no_pop_no_child(parent_node):
    procedure_name = matchStack.pop().value
    if match(common.token_types.t_COLON) and type_mark(new_node,"return_type") and match(common.token_types.t_LEFT_PAREN):
      parameter_list(new_node)
      if match(common.token_types.t_RIGHT_PAREN):
        parent_node.name = procedure_name
        parent_node.add(new_node)
        return procedure_name
      print("Fatal Error: Incomplete without the ')'")
      exit()
  return None

def procedure_body(parent_node):
  new_node = Node("procedure_body")
  declaration_list(new_node)
  match(common.token_types.t_SEMI_COLON)

  match(common.token_types.t_BEGIN)

  statement_list(new_node)
  match(common.token_types.t_SEMI_COLON)

  return_statement(parent_node)
  match(common.token_types.t_SEMI_COLON)
    
  if  match(common.token_types.t_END) and match(common.token_types.t_PROCEDURE):
    parent_node.add(new_node)
    return True


# Adds a node to "root_nodes", a lsit that will contain seperate trees.
# One tree for each function, while the code is seperate, knowing from where they stem, in important for scoping 
def procedure_declaration(parent_node):
  global root_nodes
  new_node = Node("Error, this should be filled in later","procedure_declaration")

  new_root_node = Node("New_Procedure_Root")

  procedure_name = procedure_header(new_root_node)

  if procedure_name!=None and procedure_body(new_root_node):
    new_node.name = procedure_name
    parent_node.add(new_node)
    root_nodes.append(new_root_node)
    return True
  return False

def declaration_list(parent_node):
  new_node = Node("declaration_list")

  if declaration(new_node):
    match(common.token_types.t_SEMI_COLON)
    declaration_list(new_node)
    parent_node.add(new_node)
    return True
  return False

def declaration(parent_node):
  new_node = Node("declaration")
  match(common.token_types.t_GLOBAL)
  #print("In declarion general")
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
  #print("arith op right now")
  if relation(new_node) and arith_op_prime(new_node):
    parent_node.add(new_node)
    #print("Returing true arith_op")
    return True
  #print("returing false from arith_op")
  return False

def arith_op_prime(parent_node):
  new_node = Node("arith_value")
  if (match(common.token_types.t_ADD_OP) or match(common.token_types.t_SUBTRACT_OP)):
    operation_name = matchStack.pop().type
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
    #print("In here")
    parent_node.add(new_node)
    #print("Returning true for term")
    return True
  #print("returning false for term")
  return False

def term_prime(parent_node):
  new_node = Node("term_prime")
  if (match(common.token_types.t_MULT_OP) or match(common.token_types.t_DIVIDE_OP)) and factor(new_node) and term_prime(new_node):

    operation_name = matchStack.pop().type

    # Used to have the issues with the parentheses being on the stack but that was fixed in where the stack is appended to

    parent_node.name = operation_name
    parent_node.add(new_node)
    return True
  return True




def relation(parent_node):
  new_node = Node("relation")
  #print("In relation")
  if term(new_node) and relation_prime(new_node):
    parent_node.add(new_node)
    return True
  return False

#  t_DIVIDE_OP t_AND t_ADD_OP t_SUBTRACT_OP t_GLOBAL t_OR t_ASSIGN t_EQUALS t_NOT_EQUAL t_LESS_THAN t_LESS_THAN_OR_EQUAL t_GREATER_THAN\
#   t_GREATER_THAN_OR_EQUAL t_ID t_NUMBER t_COLON t_SEMI_COLON t_LEFT_PAREN t_RIGHT_PAREN t_LEFT_BRACKET t_RIGHT_BRACKET t_TRUE t_FALSE')

def relation_prime(parent_node):
  new_node = Node("relation_prime")
  #print("In relation Prime")
  if (match(common.token_types.t_LESS_THAN) or match(common.token_types.t_LESS_THAN_OR_EQUAL) or match(common.token_types.t_DOUBLE_EQUALS) or match(common.token_types.t_GREATER_THAN) or match(common.token_types.t_GREATER_THAN_OR_EQUAL)):
    operator = str(matchStack.pop())
    parent_node.name = operator
    if factor(new_node) and term_prime(new_node):
      parent_node.add(new_node)
      #print("Returning true for relation_prime")
      return True
  return True

def factor(parent_node):
  #print("In factor from: "+parent_node.name)
  new_node = Node("factor")

  if match(common.token_types.t_LEFT_PAREN) and expression(new_node) and match(common.token_types.t_RIGHT_PAREN):
    parent_node.add(new_node)
    return True
  if match(common.token_types.t_STRING_VALUE):
    parent_node.add(new_node)
    return True
  if match(common.token_types.t_TRUE):
    new_node.name = "True"
    parent_node.add(new_node)
    return True
  if match(common.token_types.t_FALSE):
    new_node.name = "False"
    parent_node.add(new_node)
    return True
  #print("BIG MILESTONE HERE XXXXXXXXXXXXXXXXXXx")
  # Optional Minus sign
  match(common.token_types.t_SUBTRACT_OP)

  if number(new_node):
    parent_node.add(new_node)
    return True

  # This is a little hacky, The issue is if we first attempt a procedure call it consumes the id and then fails on the parentheses
  # This was, if it finds an ID, it knows it must be one of two things, a procedure call, or an ID
  # These identifying functions are "stripped" of looking for the ID because we have already found those
  if match(common.token_types.t_ID):
    matched_id = matchStack.pop().value
    if procedure_call_stripped(new_node,matched_id):
      parent_node.add(new_node)
      return True
    if name_stripped(new_node,matched_id):
      parent_node.add(new_node)
      return True

  print("Returing flase for factor ")
  return False


def string(parent_node):
  new_node = Node("")
  if match(common.token_types.t_STRING):
    new_node.name = matchStack.pop()
    parent_node.add(new_node)
    return True
  return False

def number(parent_node):
  new_node = Node("")
  if match(common.token_types.t_NUMBER):
    new_node.name = matchStack.pop().value
    if match(common.token_types.t_DOT) and match(common.token_types.t_NUMBER):
      new_node.name = new_node.name+"."+matchStack.pop().value
      parent_node.add(new_node)
      return True
    parent_node.add(new_node)
    return True
  return False

# # Take a look at another comment about why this is "stripped"
# # fixing this issue will be my next learning objective
# def name_stripped(parent_node,id_name="no name given"):
#   new_node = Node(id_name)
#   #print("IN NAME")
#   if match(common.token_types.t_LEFT_BRACKET):
#     index_node = Node("Value") 
#     if expression(index_node) and match(common.token_types.t_RIGHT_BRACKET):
#       index_node.add(new_node)
#       parent_node.add(index_node)
#       return True
#   # No Index just the value
#   parent_node.add(new_node)
#   return True


# Take a look at another comment about why this is "stripped"
# fixing this issue will be my next learning objective
def name_stripped(parent_node,id_name="no name given"):
  new_node = Node(id_name,"variable_name")
  #print("IN NAME")

  index_node = Node("Value") 
  if match(common.token_types.t_LEFT_BRACKET):
    if expression(index_node,"index") and match(common.token_types.t_RIGHT_BRACKET):
      index_node.add(new_node)
      parent_node.add(index_node)
      return True

  index_node.add(Node("0","index"))
  index_node.add(new_node)
  # No Index just the value
  parent_node.add(index_node)
  return True

  

# take a look at the comment from when this is called, it is what I call "stripped", I would love to learn a new way to do this, either from one of my books, or class
def procedure_call_stripped(parent_node,id_name="no name given"):
  new_node = Node(id_name+"()","procedure_call")
  #print("Attmepting an ID match from "+parent_node.name)
  if match(common.token_types.t_LEFT_PAREN):
    # Argument_list is not in the AND chain because it is optional
    argument_list(new_node)
    if match(common.token_types.t_RIGHT_PAREN):
      parent_node.add(new_node)
      return True
  return False


def argument_list(parent_node):
  new_node = Node("argument_list")
  if expression(new_node) and match(common.token_types.t_SEMI_COLON):
    argument_list(new_node)
    match(common.token_types.t_SEMI_COLON)
    parent_node.add(new_node)
    return True
  return False


# Expression is another example of needing a "prime"
def expression(parent_node, in_type=None):
  #print("Testing expression")
  new_node = Node("expression",in_type)
  if match(common.token_types.t_NOT):
    print("This should be fixed")
    exit()

  if arith_op(new_node) and expression_prime(new_node):
    parent_node.add(new_node)
    #print("returning true for for expression")
    return True
  #print("Returing false for expression")
  return False

def expression_prime(parent_node):
  #print("HERE RIGHT NOW")
  new_node = Node("")
  if match(common.token_types.t_AND) and expression(new_node):
    new_node.name = "& (and)"
    parent_node.add(new_node)
    return True
  elif match(common.token_types.t_OR) and expression(new_node):
    new_node.name = "| (or)"
    parent_node.add(new_node)
  else:
    return True

  # Old version of Destination that either treats the value as an index number or just an ID
  # This is being removed. It makes more sense to treat a non-index value as <var_name>[0]
# def destination(parent_node):
#   new_node = Node("destination")
#   if id(new_node,"variable_name"):
#     # Optional Bracket Indexing
#     if match(common.token_types.t_LEFT_BRACKET):
#       if expression(new_node) and match(common.token_types.t_RIGHT_BRACKET):
#         parent_node.add(new_node)
#         return True
#       print("ERROR IN DESTINATION")
#       exit()

#     # No Bracket
#     parent_node.add(new_node)
#     return True
#   return False

def destination(parent_node):
  new_node = Node("destination")
  if id(new_node,"variable_name"):
    # Optional Bracket Indexing
    if match(common.token_types.t_LEFT_BRACKET):
      if expression(new_node,"index") and match(common.token_types.t_RIGHT_BRACKET):
        parent_node.add(new_node)
        return True
      print("ERROR IN DESTINATION")
      exit()

    # No Bracket
    new_node.add(Node("0","index"))
    parent_node.add(new_node)
    return True
  return False

def assignment_statement(parent_node):
  new_node = Node("assignment_statement","assignment_statement")
  #if (match("a") or match("b")) and match(":=") and match("<number>"):
  #print("Trying out expression, this might cause errors")
  if destination(new_node) and match(common.token_types.t_ASSIGN):
    if expression(new_node,"value"):
      parent_node.add(new_node)
      return True
  return False

def if_statement(parent_node):
  new_node = Node("if_statement","if_statement")
  if match(common.token_types.t_IF) and match(common.token_types.t_LEFT_PAREN) and expression(new_node,"If Condition"):
    if match(common.token_types.t_RIGHT_PAREN) and match(common.token_types.t_THEN):
      #print("Got this far this far in an IF statment ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZz")
      if statement_list(new_node,"true_statement"):   
        #Optional Else
        if match(common.token_types.t_ELSE):
          # With an else comes more statements
          statement_list(new_node,"else_statement")

        if match(common.token_types.t_END) and match(common.token_types.t_IF):
          parent_node.add(new_node)
          return True

  #print("Returning false from IF statment")
  return False


def loop_statement(parent_node):
  new_node = Node("loop_statment")

  if match(common.token_types.t_FOR) and match(common.token_types.t_LEFT_PAREN) and assignment_statement(new_node) and match(common.token_types.t_SEMI_COLON) and expression(new_node) and match(common.token_types.t_RIGHT_PAREN) and statement_list(new_node) and match(common.token_types.t_END) and match(common.token_types.t_FOR):
    parent_node.add(new_node)
    return True
  return False

def return_statement(parent_node):
  #print("In Fucntion Return_statatemtn")
  new_node = Node("return_statement","return_statement")
  if match(common.token_types.t_RETURN) and expression(new_node):
    parent_node.add(new_node)
    print("The two branch appoach is starting to be an issue.")
    print("Either way it seems like the best approach might be to either a seperate tree for each function")
    print("Or create a very long invisible link between the two. Invsiible links are a real thing in graphviz")
    return True
  return False


def statement(parent_node):
  new_node = Node("statement")
  print("In beginning of statment")
  if assignment_statement(new_node) or if_statement(new_node) or loop_statement(new_node) or return_statement(new_node):
    parent_node.add(new_node)
    return True
  return False

def statement_list(parent_node,node_type=None):
  new_node = Node("statement_list",node_type)
  if statement(new_node):
    match(common.token_types.t_SEMI_COLON)
    statement_list(new_node)
    match(common.token_types.t_SEMI_COLON)
    parent_node.add(new_node)
    return True
  return False
    

def program_body(parent_node):
  new_node = Node("program_body")

  declaration_list(new_node)
  match(common.token_types.t_SEMI_COLON)

  match(common.token_types.t_BEGIN)

  statement_list(new_node)
  match(common.token_types.t_SEMI_COLON)
  
  if  match(common.token_types.t_END) and match(common.token_types.t_PROGRAM) and match(common.token_types.t_DOT):
    parent_node.add(new_node)
    return True
  return False



# This is something to consider during a re-write. I have to have two copies of this basic function to get the procedure name
def id(parent_node,in_type=None):
  new_node = Node("id",in_type)
  if match(common.token_types.t_ID):
    new_node.name = matchStack.pop().value
    parent_node.add(new_node)
    return True
  return False
# Nasty code.
def id_no_pop_no_child(parent_node):
  if match(common.token_types.t_ID):
    return True
  return False



def program(parent_node):
  new_node = Node("program")
  if program_header(new_node) and program_body(new_node):
    parent_node.add(new_node)
    return True
  else:
    return False


def runUnitTest(filename):
  print("FILENAME: ",filename)
  lexer.openFile(filename)
  global lookahead
  global root_nodes
  lookahead = get_token()

  root_nodes.append(Node("program_root"))

  # Kicks off the entire parseing
  if program(root_nodes[0]):
    print("Success!!")
    return True
  else:
    print("Error in program")
    return False

def solve(root):
      if not root:
         return root

      if len(root.children)==0:
         # Return an end Node
         return root

      if len(root.children)==1:
        return_node = solve(root.children[0])
        if root.type != None:
          return_node.type = root.type
        return return_node

      if len(root.children)>=2:
        root.children[0] = solve(root.children[0])
        root.children[1] = solve(root.children[1])
      if len(root.children)>=3:
        root.children[2] = solve(root.children[2])

      return root

def main():
  lexer.openFile("../src_files/test1b.src")
  global lookahead
  global root_nodes
  lookahead = get_token()

  root_nodes.append(Node("program_root"))

  # Kicks off the entire parseing
  if program(root_nodes[0]):
    print("Success!!")
    #print("------Printing Preorder------\n")
    #printPreorder(start_node)
    for function_root in root_nodes:
      viz = vt.ParseTreeVisualizer()
      code_gen = code_generator.CodeGeneratorObject()

      solve(function_root)
      viz.gendot(function_root)

      code_gen.genIntCode(function_root)


  else:
    print("Error in program")

if __name__ == '__main__':
    main()
