import textwrap
## Visualizing Code
################################################################################################
class ParseTreeVisualizer(object):
    def __init__(self):
        self.ncount = 1
        self.dot_header = [textwrap.dedent("""\
        digraph astgraph {
          node [shape=box, fontsize=12, fontname="Courier", height=.1];
          ranksep=.6;
          edge [arrowsize=.5]
        """)]
        self.dot_body = []
        self.dot_footer = ['}']
        self.content = ""

    def bfs(self, node):
        ncount = 1
        queue = []
        queue.append(node)
        s = '  node{} [label="{}"]\n'.format(ncount, node.name)
        self.dot_body.append(s)
        node._num = ncount
        ncount += 1

        while queue:
            node = queue.pop(0)
            for child_node in node.children:
                if child_node != None:
                  s = '  node{} [label="{}"]\n'.format(ncount, child_node.name)
                  self.dot_body.append(s)
                  child_node._num = ncount
                  ncount += 1
                  if child_node.type == None:
                    label_text=""
                  else:
                    label_text = child_node.type
                  s = '  node{} -> node{} [ label="{}" ];\n'.format(node._num, child_node._num,label_text)
                  self.dot_body.append(s)
                  queue.append(child_node)

    def gendot(self, root):
        tree = root
        self.bfs(tree)
        self.content = ''.join(self.dot_header + self.dot_body + self.dot_footer) 
        self.write_file()

    def write_file(self):
        with open("tree.dot",'w') as outputFile:
            outputFile.write(self.content)
        outputFile.close()
        print("Wrote Dot File to disk")

###############################################################################################################