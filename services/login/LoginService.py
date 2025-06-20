import os
from services.getSession.GetSession import *
from models.ModelsP import *
from schemas.SchemasP import *
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status, Depends, Request, Response, status, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jwt import encode, decode, DecodeError
from dotenv import load_dotenv

#Se der error no jwt encode como resolver: https://stackoverflow.com/questions/33198428/jwt-module-object-has-no-attribute-encode
#https://www.youtube.com/watch?v=5GxQ1rLTwaU - Autenticação com token
#https://fastapidozero.dunossauro.com/06/# - Certinho aqui também

load_dotenv()

#Classe para gerenciar as operações do banco de dados já criado, realmente necessária para fazer login e pegar infos
class DBManager:
    @staticmethod
    def get_user(db: Session, username: str): #Get_User, passando o bacno de dados e o nome de usuário
        return db.query(Cadastro_Users).filter(Cadastro_Users.username == username).first() #passando o banco, e o filtro, igualando o username que for passado pelo que está no banco, assim fazendo a procura
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = DBManager.get_user(db, username) #Pegando do banco de dados, o usuário digitado e os que tem no banco de dados
        if user is None: #Se o usuário "procurado" não existir
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Usuário inexistente!") 
            
        if not CryptContext(schemes=["bcrypt"]).verify(password, user.senha): #Verificando a senha digitada, com a senha que ta no banco
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Senha errada!")
        return user
    
#Chave secreta para assinar e verificar tokens
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256" #Algoritmo para desencryptografar 
#ACCESS_TOKEN_EXPIRE_MINUTES = 30 Se quiser colocar expiração no token, precisa dessa linha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Função para criar um hash de senha(incriptografar a senha)
def get_password_hash(password):
        return CryptContext(schemes=["bcrypt"]).hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password) #Verificando a senha que foi passada, e a que foi incriptografada
    
def create_access_token_service(data: dict): 
    try:
        to_encode = data.copy() #Pegar a data
        #expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #Se quiser colocar expiração no token, não sei se acho necessário
        #to_encode.update({'exp': expire})
        if to_encode != None: #Acho que não precisa deste if to_enncode != None, pode remover e deixar ele fazendo o encoded direto, se no /Token estiver certo igual está agora. Mas se quiser garantir deixar esse if é bom
            encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        #pp = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt
    except Exception as e:
        print("Erro ", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário errado")
    
async def loginService(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)): #Response é padrão, Auth2PassWordRequestForm seria para o login no canto da pagina, e o db session seria para pegar o banco de dados
    try:
        user = DBManager.authenticate_user(db, form_data.username.capitalize(), form_data.password)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário ou senha incorretos!",
            )
        #Criando um token com o nome do usuário
        access_token = create_access_token_service({"sub": user.username})
        user_username = user.username
        user_id = user.idUsuario
        email_user = user.email
        user_is_admin = user.is_admin
        profile_image = user.profile_image
        #Settando o token session em um cookie
        response.set_cookie(key="access_token", value=access_token, httponly=True) #Definindo o token como httponly
        return {"Status": "Login feito com sucesso!", "token": access_token,
                 "username": user_username,"userID": user_id, "User_Email": email_user,
                  "is_admin": user_is_admin, "profile_image": profile_image}
    except Exception as e:
        print("Erro específico: ", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função para obter o usuário atual a partir do cookie de token da sessão
#é responsável por verificar e decodificar o token JWT recebido no cookie da solicitação.
async def get_current_user_service(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme),):
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

async def protected_post_route_service(user: Cadastro_Users = Depends(get_current_user_service)): #Exigindo login para tal execução de uma reuqisição
    if not user.is_admin: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para fazer esta ação!!"
        )
    #Somente administradores podem acessar esta rota, e receber este retorno
    return {"message": f"Bem vindo administrador, {user.username}!!"}


