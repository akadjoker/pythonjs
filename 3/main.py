
from Lexer import Lexer
from Token import TokenType, Token
from Parser import Parser, ASTPrinter
from Printer import ASTPrinter
from Interpreter import Interpreter


source_code = """
program  main;
{
  


for (int i=0; i<10; i=i+1)
{
    if (i==5)
    {
        i = i + 1;
        continue;
    }
    print(i);


}
 
}
"""

# Inicializando o lexer
lexer = Lexer(source_code)
tokens = lexer.tokenize()


# for token in tokens:
#     print(token)


parser = Parser(tokens)
program = parser.parse()

# printer = ASTPrinter()
# print("\n")
# print(printer.print(program))

interpreter = Interpreter()
print("Result:")
interpreter.interpret(program)



# /*
#     int i = 0;
#     int j = 0;
#     while(i<4)
#     {
#         if(i==3)
#         {
#             break;
#         }
#         i=i+1;
        
#         while (j<4)
#         {
#             if(j==3)
#             {
#                j=0;
#                break;
#             }
#             print(j);
#             j=j+1;
#         }
#     }
# */
    