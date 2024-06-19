
from Lexer import Lexer
from Token import TokenType
from Parser import Ast,Interpreter

source_code = """
process main() 
{
    
int a;
float b;
string c="luis";
bool d=false;

print("teste");

}


function teste()
{
}
"""

# Inicializando o lexer
lexer = Lexer(source_code)
tokens = lexer.tokenize()

# Imprimindo os tokens gerados
for token in tokens:
    print(token)