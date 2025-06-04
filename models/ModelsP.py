from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, validates
from database import Base
from datetime import date
from pydantic import BaseModel, validator
from sqlalchemy.ext.hybrid import hybrid_property
import re

#Classe que cria a table no banco de dados, e coloca que valores que serão armazenados
class Produtos_Cad(Base):
    __tablename__ = 'produtos' 
    idProduto: int = Column(Integer, primary_key=True)
    nome: str = Column(String(200), nullable=False)
    tipo: str = Column(String(256), nullable=False)  # Tipo do produto
    valor_compra: float = Column(Float(53), nullable=False)
    valor_venda = Column("valor_venda", Float(53), nullable=False)  # Valor original do produto
    percentual_lucro = Column(Float(53), nullable=True)
    quantidade: int = Column(Integer, nullable=False)
    tamanho: str = Column(String(200), nullable=False)  # Tamanho do produto
    data_validade: str = Column(String(10), nullable=False)
    # data_cadastro: str = Column(String(10), nullable=False)

    @validates('valor_venda')
    def set_valor_venda(self, key, valor_venda):
        if self.valor_compra > 0:
            self.percentual_lucro = ((valor_venda - self.valor_compra) / self.valor_compra) * 100
        
        else:
            self.percentual_lucro = 0

        return valor_venda
    
    @validator("tamanho")
    def validar_tamanho(cls, v):
        if not re.fullmatch(r"\d+(ml|l|g|kg)", v.strip(), flags=re.IGNORECASE):
            raise ValueError("Tamanho inválido! Use formatos como: 500ml, 1L, 2Kg, 100g")
        return v
    
class Venda_Carrinho(Base):
    __tablename__ = "vendasCarrinho"
    id_venda: int = Column(Integer, primary_key=True, autoincrement=True)
    tipo: str = Column(String(100), nullable=False)
    
class Produto_TeT_Cad(Base):
    __tablename__ = "valorTotal_e_tipoVenda"
    id_venda_com_tipo: int = Column(Integer, primary_key=True, autoincrement=True)
    tipo: str = Column(String(100), nullable=False)
    valor: float = Column(Float(53), nullable=False)
    quantidade: float = Column(Float(53), nullable=False)
    produto: str = Column(String(100), nullable=False)
    
class Meses_Valores_Cad(Base):
    __tablename__ = 'valores_meses'
    idMes: int = Column(Integer, primary_key=True)
    mes: str = Column(String(100), nullable=False)
    valor: float = Column(Float(53), nullable=False)

class Dias_Valores_Mes_Cad(Base):
    __tablename__ = "valores_dias_venda"
    dia: int = Column(Integer, nullable=False, primary_key=True)
    valor: float = Column(Float(53), nullable=False)
    mes: String = Column(String(100), nullable=False, primary_key=True)

class Meses_Valores_Bill_Cad(Base):
    __tablename__ = 'valores_contas_bills'
    idMes: int = Column(Integer, primary_key=True)
    mes: str = Column(String(100), nullable=False)
    valor: float = Column(Float(53), nullable=False)

class Dias_Valores_Mes_Bill_Cad(Base):
    __tablename__ = "valores_dias_bills"
    dia: int = Column(Integer, nullable=False, primary_key=True)
    valor: float = Column(Float(53), nullable=False)
    mes: String = Column(String(100), nullable=False, primary_key=True)

class Gastos_Aleatorios_Mes(Base):
    __tablename__ = 'gastos_aleatorios'
    idMes: int = Column(Integer, primary_key=True)
    mes: str = Column(String(100), nullable=False)
    valor: float = Column(Float(53), nullable=False)

class Gastos_Aleatorios_Cad(Base):
    __tablename__ = "gastos_aleatorios_mes"
    dia: int = Column(Integer, nullable=False, primary_key=True)
    valor: float = Column(Float(53), nullable=False)
    mes: String = Column(String(100), nullable=False, primary_key=True)

class Gastos_Cartao_Mes(Base):
    __tablename__ = 'gastos_cartoes'
    idMes: int = Column(Integer, primary_key=True)
    mes: str = Column(String(100), nullable=False)
    valor: float = Column(Float(53), nullable=False)

class Gastos_Cartao_Cad(Base):
    __tablename__ = "gastos_cartoes_mes"
    dia: int = Column(Integer, nullable=False, primary_key=True)
    valor: float = Column(Float(53), nullable=False)
    mes: String = Column(String(100), nullable=False, primary_key=True)
class Fiado_Val(Base):
    __tablename__ = "fiado"
    dia: int = Column(Integer, nullable=False, primary_key=True)
    valor: float = Column(Float(53), nullable=False)
    name: String = Column(String(200), nullable=False)

class Cadastro_Users(Base):
    __tablename__ = 'all_users'
    idUsuario: int = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    username: String = Column(String(200), nullable=False, unique=True)
    email: String = Column(String(200), nullable=False, unique=True)
    senha: String = Column(String(200), nullable=False)
    is_admin: bool = Column(Boolean, default=False)
    profile_image: String = Column(String(255), nullable=False)
