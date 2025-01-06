from typing import List, Union
from pydantic import BaseModel
from datetime import date

# Classe para criar/atualizar produtos
class Produtos_S(BaseModel):
    nome: str
    tipo: str
    valor_compra: float
    valor_venda: float  
    quantidade: int
    tamanho: str
    data_validade: str

    class Config:
        orm_mode = True

class Meses_Valores(BaseModel):
   mes: str
   valor: float

class Meses_Valores_Att(BaseModel):
   mes: str
   valor: float

class AttProdutos(BaseModel):
   nome:str
   tamanho: str
   tipo:str  
   valor_compra:float
   valor_venda: float  
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