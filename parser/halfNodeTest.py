def solve(root):
      if not root:
         return root

      if len(root.children)==0:
         # Return an end Node
         return root

      if len(root.children)==1:
        return solve(root.children[0])

      if len(root.children)>=2:
        root.children[0] = solve(root.children[0])
        root.children[1] = solve(root.children[1])

      return root