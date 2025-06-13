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

    model_config = {
        "from_attributes": True  # ✅ novo nome
    }

class CarrinhoVenda(BaseModel):
   tipo: str

class Produtos_TeT(BaseModel):
   tipo: str
   valor: float
   quantidade: float
   produto: str

class AttProdutos(BaseModel):
   nome:str
   tamanho: str
   tipo:str  
   valor_compra:float
   valor_venda: float  
   quantidade:int
   data_validade:str 

class Meses_Valores(BaseModel):
   mes: str
   valor: float

class Meses_Valores_Att(BaseModel):
   mes: str
   valor: float

class Dias_Valores_Mes(BaseModel):
   mes: str
   valor: float
   dia: int

class Dias_Valores_Mes_Att(BaseModel):
   mes: str
   valor: float
   dia: int

class Meses_Valores_Bill(BaseModel):
   mes: str
   valor: float

class Dias_Valores_Mes_Bill(BaseModel):
   mes: str
   valor: float
   dia: int
   motivo: str 

class Gastos_Aleatorios_Mes(BaseModel):
   mes: str
   valor: float

class Gastos_Aleatorios(BaseModel):
   mes: str
   valor: float
   dia: int

class Gastos_Cartao_Mes(BaseModel):
   mes: str
   valor: float

class Gastos_Cartao(BaseModel):
   mes: str
   valor: float
   dia: int

class Fiado(BaseModel):
   dia: int
   valor: float
   name: str
   
class Fiado_Att(BaseModel):
   dia: int
   valor: float
   name: str

class Cadastro(BaseModel):
   username:str
   email:str
   senha:str
   is_admin:bool

class CadastroUserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    profile_image: str | None

    class Config:
        orm_mode = True

class Att_Cadastro(BaseModel):
   username: str
   email: str
   is_admin: bool

class Token(BaseModel): #Realomente necessário para o Login, usado no main.py com o /token
    access_token: str
    token_type: str

class TokenData(BaseModel): #Realmente necessário para o login, usado no login.py com o /login mesmo
   username: str | None = None