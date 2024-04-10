from sqlalchemy import Column, Integer, String, Float
from database import Base

#Classe que cria a table no banco de dados, e coloca que valores que serão armazenados
class Produtos(Base):
    __tablename__ = 'produtos' 
    idProduto = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False, unique=True)
    tipo = Column(String(256), nullable=False)#Bebida alcoolica/doce/bebida normal/salgadinho etc
    valor = Column(Float(200), nullable=False) #Valor do produto
    quantidade = Column(Integer, nullable=False)
    tamanho = Column(String(200), nullable=False) #Tamanho, se é L, ml, e o quanto q é..
    data_validade = Column(String(10), nullable=False)
    data_cadastro = Column(String(10), nullable=False)

    # def __str__(self):
    #     return "Criado o", self.nome

class Cadastro_Users(Base):
    __tablename__ = 'usuarios'
    idUsuario = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    nome = Column(String(200), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    senha = Column(String(200), nullable=False)

class Cadastro_Admins(Base):
    __tablename__ = 'admins'
    idAdmin = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    nome = Column(String(200), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    senha = Column(String(200), nullable=False)


