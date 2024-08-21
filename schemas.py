from pydantic import BaseModel
from datetime import date

#Classe que vamos criar o que queremos que o usuário passe de valores, para colocar no banco de dados
class Produtos(BaseModel):
   nome:str
   tipo:str #Criando uma variável e indicando o valor que deve ser atribuido á ela quando chamarem essa classe para usar 
   valor:float
   quantidade:int
   tamanho:str
   data_validade:str 
   # data_cadastro:str 

class AttProdutos(BaseModel):
   nome:str
   tamanho: str
   tipo:str  
   valor:float
   quantidade:int
   data_validade:str 
   
class Cadastro(BaseModel):
   username:str
   email:str
   senha:str
   is_admin:bool

class Att_Cadastro(BaseModel):
   username: str
   email: str
   is_admin: bool

class Token(BaseModel): #Realomente necessário para o Login, usado no main.py com o /token
    access_token: str
    token_type: str

class TokenData(BaseModel): #Realmente necessário para o login, usado no login.py com o /login mesmo
   username: str | None = None