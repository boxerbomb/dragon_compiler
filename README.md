# dragon_compiler
A recursive-descent compiler as described in EECS 6083/5183 by Philip A. Wilsey and "The Dragon Book" 1st Edition.


Currently work is being done in Python as I am still figuring out what is needed for a compiler. I plan on switching to C, C++, Ada, or Pascal once I feel ready for a rewrite. The course project description reccomends generating LLVM assembly for the code generation, I might look into that but right now I plan on generating Gameboy assembly code, as it is very similar to Z80 assembly and I love retro-computers.

Being able to visualize the Abstract Syntax Tree has been extremely helpful in debugging my progress, I choose to use Graphvis for the visualzation. I believe this is a solid choice as I have separated Graphvis generation code from the parser, hopefully allowing an easy transistion to another programming language. Other than python, no dependencies are required to run the parser, although Graphviz is required to generate the visual representation, and ImageMagick is optional to combine the multiple images(seperated per procedure) into one whole-program image.

To Do:
Simplify Parse Tree to AST.
Error Handling
Intermediate Code Generation
Register Allocation (Graph Coloring)


Here is an example of a generated Parse Tree:
![AST_image](https://raw.githubusercontent.com/boxerbomb/dragon_compiler/main/parser/final_tree.png)
