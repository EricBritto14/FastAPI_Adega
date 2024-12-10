from sqlalchemy import null
import models as models, schemas as schemas
from controller.Login import *
from models import *
from schemas import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
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
async def addItem(item:Cadastro, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await addItemService(item, session, user)

#Atualizando valores
@router.put("/usuarios/atualizar/{nome}")
async def updateItem(nome:str, item:schemas.Cadastro, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await updateItemService(nome, item, session, user)

@router.put("/usuarios/atualizar_by_id/{id}")
async def atualizarById(id: int, item:schemas.Cadastro, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await atualizarByIdService(id, item, session, user) 
    
@router.patch("/usuarios/patch_by_id/{id}")
async def atualizarById(id: int, item:schemas.Att_Cadastro, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await atualizarByIdService(id, item, session, user)

#Deletando valores
@router.delete("/usuarios/delete/{nome}")
async def deleteItem(nome:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await deleteItemService(nome, session, user)
    
@router.delete("/users/delete_by_id/{id}")
async def deleteItemId(id: int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await deleteItemIdService(id, session, user)