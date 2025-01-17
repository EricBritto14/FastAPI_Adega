from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from database import Base
from datetime import date
from pydantic import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property

#Classe que cria a table no banco de dados, e coloca que valores que serão armazenados
class Produtos_Cad(Base):
    __tablename__ = 'produtos' 
    
    idProduto: int = Column(Integer, primary_key=True)
    nome: str = Column(String(200), nullable=False, unique=True)
    tipo: str = Column(String(256), nullable=False)  # Tipo do produto
    valor_compra: float = Column(Float(53), nullable=False)
    _valor_venda = Column("valor_venda", Float(53), nullable=False)  # Valor original do produto
    quantidade: int = Column(Integer, nullable=False)
    tamanho: str = Column(String(200), nullable=False)  # Tamanho do produto
    data_validade: str = Column(String(10), nullable=False)
    # data_cadastro: str = Column(String(10), nullable=False)

    # Propriedade híbrida para calcular a porcentagem de ganho
    @hybrid_property
    def valor_venda(self):
        if self.valor_compra > 0:
            return ((self._valor_venda - self.valor_compra) / self.valor_compra) * 100
        return 0

    # Setter para armazenar o valor original
    @valor_venda.setter
    def valor_venda(self, valor): 
        self._valor_venda = valor
    
class Meses_Valores_Cad(Base):
    __tablename__ = 'valores_meses'
    idMes: int = Column(Integer, primary_key=True)
    mes: str = Column(String(100), nullable=False, unique=True)
    valor: float = Column(Float(100), nullable=False)

class Dias_Valores_Mes_Cad(Base):
    __tablename__ = "valores_dias_venda"
    id: int = Column(Integer, primary_key=True)
    dia: int = Column(Integer, nullable=False)
    valor: float = Column(Float(53), nullable=False)
    mes: String = Column(String(100), nullable=False, unique=True)

class Fiado_Val(Base):
    __tablename__ = "fiado"
    idFiado: int = Column(Integer, primary_key=True)
    dia: int = Column(Integer, nullable=False)
    valor: float = Column(Float(53), nullable=False)
    name: String = Column(String(200), nullable=False, unique=True)


class Cadastro_Users(Base):
    __tablename__ = 'all_users'
    idUsuario: int = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    username: String = Column(String(200), nullable=False, unique=True)
    email: String = Column(String(200), nullable=False, unique=True)
    senha: String = Column(String(200), nullable=False)
    is_admin: bool = Column(Boolean, default=False)

