
from Lexer import Lexer
from Token import TokenType, Token
from Parser import Parser, ASTPrinter
from Printer import ASTPrinter
from Interpreter import Interpreter


source_code = """
program  main;
{
   print("start main");
   start nave(1);
   start bala(1);
   print("end main");
}
 
process nave(int m_x)
{
    print("start nave ");
    x = m_x;
    loop
    {
        if (x > 5)
        {
            break;
        }
        print("nave: "+x);
        
        x = x + 1;
        frame(50);

    }
        
    print("end nave ");
    
}

process bala(int m_x)
{
    
    print("start bala ");
    x = m_x;
    loop
    {
        if (x > 5)
        {
            break;
        }
        print("bala: "+x);
        
        x = x + 1;
        frame(80);

    }
        
    print("end bala ");

}


"""

# Inicializando o lexer
lexer = Lexer(source_code)
tokens = lexer.tokenize()


# for token in tokens:
#      print(token)


parser = Parser(tokens)
program = parser.parse()

printer = ASTPrinter()
print("\n")
printer.print(program)

interpreter = Interpreter()
print("Result:")

async def main():
    await interpreter.run(program)




try:
    interpreter.run(program)
except Exception as e:
    print(f"Run Error: {e}")


#interpreter.go()

#interpreter.debug()



