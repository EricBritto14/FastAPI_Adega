import os
from fastapi import FastAPI, Depends #, Response
from controller import Login, Meses, Produtos, Users, Fiados #, admins
from controller.Login import *
from schemas import *
from models import *
from logger import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from loggs import *
from loggs.middleware import *
from database import Base, engine
from sqlalchemy.orm import Session
from services.getSession.GetSession import *
from services.token.TokenService import *
from dotenv import load_dotenv

Base.metadata.create_all(engine) #Linha para realmente criar o banco de dados se não tivermos um. Vai criar o banco de dados com as informações que temos no engine do database.py
#Fazer o metodo pra recuperar senha pelo email, e pegar as info não apenas pelo id e pelo nome, mas sim pelos 2 talvez.

app = FastAPI(title="API Adega Santa-Dose")#title="API Santa-Dose" #Title para dar nome à api

load_dotenv()

ORIGINS = os.getenv("ORIGINS")

# origins = [
    # "http://localhost:5173",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Produtos.router, tags=["Produtos"])
app.include_router(Users.router, tags=["Usuários"])
app.include_router(Fiados.router, tags=["Fiados"])
app.include_router(Meses.router, tags=["Meses"])
app.include_router(Login.router, tags=["Login"])
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware) #Jeito certo de registar o middleware no app, para conseguir criar uma classe middleware e só puxar pra cá
logger.info('Starting API...')

@app.get("/")
async def getItems(session: Session = Depends(get_session)): #Pegando os valores do banco de dados, Depends do get_session
    items = session.query(Produtos_Cad).all()
    return items

@app.get("/usuarios/teste")
async def getItemss(session: Session = Depends(get_session)):
    usuarios = session.query(Cadastro_Users).all()
    return usuarios

@app.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return login_for_access_token_service(form_data, session)
