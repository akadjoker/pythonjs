
from Lexer import Lexer
from Token import TokenType, Token
from Parser import Parser, ASTPrinter
from Printer import ASTPrinter
from Interpreter import Interpreter


source_code = """
program  main;
{
  
    float start=now;
    print("Expressions");
    int val = 2 + 3 * 4 ^ 2;
    print(val);
    eval(2 + 3 * 4 ^ 2);

    float end=now;
    float duration =(end - start);

    print("Duration: ");
    print(duration);

    int i=20;

    if (i == 0)
    {
        print("0");

    } elif(i==1)
    {
        print( "1");
    } else 
    {
        print( "2");
    }
    i=5;
    while(i>0)
    {
        print(i);
        i=i-1;
    }
    
    i=5;
    do
    {
         print(i);
         i = i - 1;
    } while(i>0);

    print("Hello World!");
   for (int i = 0; i <= 100; i = i + 1)
   {
       print(i);
   }
   
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