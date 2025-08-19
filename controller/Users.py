from sqlalchemy import null
import models as models, schemas as schemas
from controller.Login import *
from models import *
from schemas import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, File, Form, UploadFile
from services.users.UsersService import *

router = APIRouter()

@router.get("/usuarios")
async def getItems(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session
    return await getItemsAllService(session, user)

@router.get("/usuarios/{nome}") #Router para trazer as informações de acordo com o id
async def getItem(username:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    return await getItemByNameService(username, session, user)    

@router.get("/usuarios/get_by_id/{id}")
async def getItemId(id:int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await getItemByIdService(id, session, user)

@router.post("/usuarios/adicionar")
async def addItem(username: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    is_admin_raw: str = Form(...),
    profile_image: UploadFile = File(None),
    session: Session = Depends(get_session),
    user: Cadastro_Users = Depends(get_current_user)
):
    print(f"username: {username}, email: {email}, senha: {senha}, is_admin_raw: {is_admin_raw}")
    print(f"profile_image: {profile_image.filename if profile_image else 'Nenhuma imagem'}")
    return await addItemService(
        username=username,
        email=email,
        senha=senha,
        is_admin_raw=is_admin_raw,
        profile_image=profile_image,
        session=session
    )

@router.patch("/usuarios/patch_by_id/{id}")
async def atualizarById(id: int,
    username: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    is_admin_raw: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session),
    user: Cadastro_Users = Depends(get_current_user)):

    print("--- DADOS RECEBIDOS NA ROTA ---")
    print(f"ID: {id}")
    print(f"Username: {username} (Tipo: {type(username)})")
    print(f"Email: {email} (Tipo: {type(email)})")
    print(f"Is Admin Raw: {is_admin_raw} (Tipo: {type(is_admin_raw)})")
    print(f"Profile Image: {profile_image.filename if profile_image else 'Nenhuma'}")
    print("---------------------------------")


    return await atualizarByIdService(user_id=id,
        username=username,
        email=email,
        is_admin_raw=is_admin_raw,
        profile_image=profile_image,
        session=session)

#Deletando valores
@router.delete("/usuarios/delete/{nome}")
async def deleteItem(nome:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await deleteItemService(nome, session, user)
    
@router.delete("/users/delete_by_id/{id}")
async def deleteItemId(id: int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await deleteItemIdService(id, session, user)