from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base
from datetime import date
from pydantic import BaseModel

#Classe que cria a table no banco de dados, e coloca que valores que serão armazenados
class Produtos_Cad(Base):
    __tablename__ = 'produtos' 
    idProduto: int = Column(Integer, primary_key=True)
    nome: String = Column(String(200), nullable=False, unique=True)
    tipo: String = Column(String(256), nullable=False)#Bebida alcoolica/doce/bebida normal/salgadinho etc
    valor: Float = Column(Float(53), nullable=False) #Valor do produto
    quantidade: int = Column(Integer, nullable=False)
    tamanho: String = Column(String(200), nullable=False) #Tamanho, se é L, ml, e o quanto q é..
    data_validade: String = Column(String(10), nullable=False)
    data_cadastro: String = Column(String(10), nullable=False)

class Cadastro_Users(Base):
    __tablename__ = 'all_users'
    idUsuario: int = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    username: String = Column(String(200), nullable=False, unique=True)
    email: String = Column(String(200), nullable=False, unique=True)
    senha: String = Column(String(200), nullable=False)
    is_admin: bool = Column(Boolean, default=False)

