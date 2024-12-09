from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#Creates database engine
URL_DATABASE = os.getenv("URL_DATABASE")
# "postgresql://postgres:e40024041@localhost:5432/database_adega"
if not URL_DATABASE:
    raise ValueError("A URL do banco de dados não está sendo possível acessar.")

engine = create_engine(URL_DATABASE) #Criando a engine, o banco de dados em si, e colocando o tipo dele, no caso a conexão com o postgress

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()
