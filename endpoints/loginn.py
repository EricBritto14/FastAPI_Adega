from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, Request, Response, status, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from models import *
from database import engine, Base, SessionLocal
import jwt
from jwt import encode, decode, DecodeError
from schemas import *

#Se der error no jwt encode como resolver: https://stackoverflow.com/questions/33198428/jwt-module-object-has-no-attribute-encode
#https://www.youtube.com/watch?v=5GxQ1rLTwaU - Autenticação com token
#https://fastapidozero.dunossauro.com/06/# - Certinho aqui também

router = APIRouter() #Router da classe

def get_session(): #Função para pegar a sessão, e abrir e fechar o banco de dados
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

#Classe para gerenciar as operações do banco de dados já criado, realmente necessária para fazer login e pegar infos
class DBManager:
    @staticmethod
    def get_user(db: Session, username: str): #Get_User, passando o bacno de dados e o nome de usuário
        print(db.query(Cadastro_Users).filter(Cadastro_Users.username == username).first())
        return db.query(Cadastro_Users).filter(Cadastro_Users.username == username).first() #passando o banco, e o filtro, igualando o username que for passado pelo que está no banco, assim fazendo a procura
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = DBManager.get_user(db, username) #Pegando do banco de dados, o usuário digitado e os que tem no banco de dados
        if not user: #Se o usuário "procurado" não existir
            return None
        if not CryptContext(schemas=["bcrypt"]).verify(password, user.senha): #Verificando a senha digitada, com a senha que ta no banco
            return None
        return user   

#Chave secreta para assinar e verificar tokens
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256" #Algoritmo para desencryptografar 
#ACCESS_TOKEN_EXPIRE_MINUTES = 30 Se quiser colocar expiração no token, precisa dessa linha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Função para criar um hash de senha(incriptografar a senha)
def get_password_hash(password):
    return CryptContext(schemes=["bcrypt"]).hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password) #Verificando a senha que foi passada, e a que foi incriptografada

#Função para criar um token JWT
def create_access_token(data: dict):
    to_encode = data.copy() #Pegar a data
    #expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #Se quiser colocar expiração no token, não sei se acho necessário
    #to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    #pp = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Rota para realizar login
@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)): #Response é padrão, Auth2PassWordRequestForm seria para o login no canto da pagina, e o db session seria para pegar o banco de dados
    user = DBManager.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos!",
        )
    #Criando um token com o nome do usuário
    access_token = create_access_token({"sub": user.username})
    #Settando o token session em um cookie
    response.set_cookie(key="access_token", value=access_token, httponly=True) #Definindo o token como httponly
    return {"Status": "Login feito com sucesso!", "token": access_token}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Função para obter o usuário atual a partir do cookie de token da sessão
#é responsável por verificar e decodificar o token JWT recebido no cookie da solicitação.
async def get_current_user(
        session: Session = Depends(get_session),
        token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception
    
    user = session.scalar(
        select(Cadastro_Users).where(Cadastro_Users.username == token_data.username)
    )

    if user is None:
        raise credentials_exception
    
    return user

#Exemplo de rota protegida, necessário apenas o login para poder usa-lá
@router.post("/protected")
def protected_route(user: Cadastro_Users = Depends(get_current_user)):
    return {"Mensagem": f"Hello, {user.email}!"}

#Rota protegida também pelo login, mas para usá-la precisaria ser admin, caso contrário da erro
@router.post("/protected_post")
def protected_post_route(user: Cadastro_Users = Depends(get_current_user)): #Exigindo login para tal execução de uma reuqisição
    if not user.is_admin: #Puxando do banco de dados o atributo de cadastro "is_admin" para verificar se é adm ou não, se não for não pode fazer tal ação, mesmo estando logado
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para fazer esta ação!!"
        )
    #Somente administradores podem acessar esta rota, e receber este retorno
    return {"message": f"Bem vindo administrador, {user.username}!!"}

#Rota para criar o primeiro usuário
# @router.post("/init_user")
# def create_initial_user(db: Session = Depends(get_session)):
#     # Verifica se já existe algum usuário no banco de dados
#     existing_user = db.query(Cadastro_Admins).first()
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User already exists in the database",
#         )

#     # Cria o primeiro usuário
#     initial_user = Cadastro_Admins(
#         username="eric2222",
#         email="Eric.Britto222@gmail.com",
#         senha=get_password_hash("E40024041"),
#         is_admin=TRUE
#     )
#     db.add(initial_user)
#     db.commit()
#     return {"message": "Initial user created successfully"}