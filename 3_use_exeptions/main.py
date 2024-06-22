
from Lexer import Lexer
from Token import TokenType, Token
from Parser import Parser, ASTPrinter
from Printer import ASTPrinter
from Interpreter import Interpreter


source_code = """
program  main;
{
  
int i=0;
loop;
{
    if (i==3)
    {
        break;
    }
    print(i);
    i = i + 1;
}
 print(i);
   
}
"""

# Inicializando o lexer
lexer = Lexer(source_code)
tokens = lexer.tokenize()


for token in tokens:
    print(token)


parser = Parser(tokens)
program = parser.parse()

printer = ASTPrinter()
print("\n")
print(printer.print(program))

interpreter = Interpreter()
print("Result:")
interpreter.interpret(program)



#    float start=now;
#     print("Expressions");
#     int val = 2 + 3 * 4 ^ 2;
#     print(val);
#     eval(2 + 3 * 4 ^ 2);

#     float end=now;
#     float duration =(end - start);

#     print("Duration: ");
#     print(duration);

#     int i=20;

#     if (i == 0)
#     {
#         print("0");

#     } elif(i==1)
#     {
#         print( "1");
#     } else 
#     {
#         print( "2");
#     }

    
#     i=5;
#     do
#     {
#          print(i);
#          i = i - 1;
#     } while(i>0);

#     print("for!");
#    for (int i = 0; i <= 5; i = i + 1)
#    {
#         if (i == 3)
#         {
#             i = i + 1;
#             continue;
#         }
#        print(i);
#    }

#    int state = 10;
#    switch(state)
#    {
#        case 0:
#        {
#            print("State 0");
#        }
#        case 1:
#        {
#            print("State 1");
#        }
#        default:
#        {
#            print("State default");
#        }
#    }

#    print("while break");
#     i=5;
#     while(i>0)
#     {
#         if(i==3)
#         {
#             i=i-1; 
#             continue;
#         }
#         print(i);
#         i=i-1;
#     }
#     print(i);
