from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Creates database engine
URL_DATABASE = "postgresql://admin:SmtCM92QkRUo3ms9JjbsQbUu34x6MvBu@dpg-ctbjetrqf0us73cn2i30-a.oregon-postgres.render.com/adega_santadose"
# "postgresql://postgres:e40024041@localhost:5432/database_adega"


engine = create_engine(URL_DATABASE) #Criando a engine, o banco de dados em si, e colocando o tipo dele, no caso a conexão com o postgress

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()
