## Code Generation
################################################################################################
class CodeGeneratorObject(object):
    def __init__(self):
        self.exampleVar = 0


    # Important part of this fucntion is we don't need to worry about scoping, that will all be taken care of,
    # For now we just need to find the code, then we can worry about activation records at another time.
    def genIntCode(self, curNode):
        # Accept a root, and start some sort of tree walk, it should make sense with the order it is going.
        # Wait! What about "Triple children", basically walk the tree to find nodes that I have identified as "active"
        # Here are some examples of "active" nodes

        # assignment_statment: generate a thing like t1 = a + b

        # if_statement: if condition goto true_label
        #   true_lebel: make a true label and start generating
        #   else_label: make a else label and start generating

        # loop_statment: condition_label: if true go to body label
        #   body_label: start generating
        #   break_label: just points to rest of code

        # return_statement: basically just find what ID to return and return that t_label(t1)

        # procedure_call: goto function label, maybe also take note of what vars are needed 

        if curNode.name == "assignment_statement":
            varName = None
            index = None
            value = None

            for child_node in curNode.children:
                if child_node.name == "destination":
                    varName = child_node.children[0].name
                    index = child_node.children[1].name
                elif child_node.type == "value":
                    value = child_node.name
            
            #print(varName+"["+index+"]"+" <= "+value)


        # Currently I am thinking that I could find each branch, "print a label", and then run the found nodes through this function again
        # But I might have to do something so make sure those pieces are not traversed again
        # I could also have soem sort of state machine that knows that branch it is on.
        if curNode.name == "if_statement":
            pass

         

        print("CodeGeneratorObject:",curNode.name, curNode.type)


        if len(curNode.children)==0:
            pass
        else:
            if len(curNode.children)>=1:
                self.genIntCode(curNode.children[0])
            if len(curNode.children)>=2:
                self.genIntCode(curNode.children[1])
            if len(curNode.children)>=3:
                self.genIntCode(curNode.children[2])



    def write_file(self,root_name):
        print(" This is just an example function")
        exit()
        with open("dot_files/"+root_name+".dot",'w') as outputFile:
            outputFile.write(self.content)
        outputFile.close()
        print("Wrote Dot File to disk")

###############################################################################################################