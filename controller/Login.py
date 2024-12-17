# from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from models import *
from schemas import *
from services.login.LoginService import *

router = APIRouter() #Router da classe

#Função para criar um token JWT
def create_access_token(data: dict): 
    return create_access_token_service(data)
        
@router.post("/login") 
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)): #Response é padrão, Auth2PassWordRequestForm seria para o login no canto da pagina, e o db session seria para pegar o banco de dados
    return await loginService(response, form_data, db)

async def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme),):
    return await get_current_user_service(session, token)

#Exemplo de rota protegida, necessário apenas o login para poder usa-lá
@router.post("/protected")
async def protected_route(user: Cadastro_Users = Depends(get_current_user)):
    return {"Mensagem": f"Hello, {user.email}!"}

#Rota protegida também pelo login, mas para usá-la precisaria ser admin, caso contrário da erro
@router.post("/protected_post")
async def protected_post_route(user: Cadastro_Users = Depends(get_current_user)): #Exigindo login para tal execução de uma reuqisição
    return await protected_post_route_service(user)

# Rota para criar o primeiro usuário
# @router.post("/init_user")
# def create_initial_user(db: Session = Depends(get_session)):
# #     # Verifica se já existe algum usuário no banco de dados
#     existing_user = db.query(Cadastro_Users).first()
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User already exists in the database",
#         )

# #     # Cria o primeiro usuário
#     initial_user = Cadastro_Users(
#         username="Admin",
#         email="Eric.Britto22@gmail.com",
#         senha=get_password_hash("E40024041e&"),
#         is_admin=True
#     )
#     db.add(initial_user)
#     db.commit()
#     return {"message": "Initial user created successfully"}