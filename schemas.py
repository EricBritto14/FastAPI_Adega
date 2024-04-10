from pydantic import BaseModel


#Classe que vamos criar o que queremos que o usuário passe de valores, para colocar no banco de dados
class Produtos(BaseModel):
   nome:str
   tipo:str #Criando uma variável e indicando o valor que deve ser atribuido á ela quando chamarem essa classe para usar 
   valor:float
   quantidade:int
   tamanho:str
   data_validade:str 
   data_cadastro:str

class Cadastro(BaseModel):
   nome:str
   email:str
   senha:str

class Admins(BaseModel):
   nome:str
   email:str
   senha:str