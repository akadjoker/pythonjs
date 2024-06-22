
from Lexer import Lexer
from Token import TokenType, Token
from Parser import Parser, ASTPrinter
from Printer import ASTPrinter
from Interpreter import Interpreter


source_code = """
program  main;
{
  

    print("Expressions");
    int val = (-(2+2) * (2+2)) / 2 * 2 - 10 +0.2;
    print(val);
    eval((-(2+2) * (2+2)) / 2 * 2 - 10 +0.2);

    var a = 10;
    var b = 20;
    var c = a % b;
    print(c);
}
"""

# Inicializando o lexer
lexer = Lexer(source_code)
tokens = lexer.tokenize()

# Imprimindo os tokens gerados
# for token in tokens:
#     print(token)


parser = Parser(tokens)
program = parser.parse()

printer = ASTPrinter()
print("\n")
print(printer.print(program))

interpreter = Interpreter()
print("Result:")
interpreter.interpret(program)