from fastapi import APIRouter, Depends
from requests import Session

from controller.Login import get_current_user
from models.ModelsP import Cadastro_Users
from schemas import SchemasP
from services.meses.MesesService import *

router = APIRouter()

@router.post("/meses_venda/adicionar_valores")
async def addItem(item: SchemasP.Meses_Valores, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await addMesesService(item, session, user)

@router.post("/meses_valor/adicionar_valores_dias")
async def addItemDia(item: SchemasP.Dias_Valores_Mes, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await addDiasVendasService(item, session, user)

@router.get("/dias_venda/{mes}") #Router para trazer as informações de acordo com o id
async def getItem(mes: str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    return await getDaysMesesServices(mes, session, user)

#Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
@router.get("/meses_venda") #Router para trazer as informações de acordo com o id
async def getItem(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    return await getMesesServices(session, user)

@router.put("/meses_venda/atualizar_valores/{mes}") #Tentar pegar pelo nome, não pelo id
async def updateItem(mes:str, item: SchemasP.Meses_Valores_Att, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await updateMesService(mes, item, session, user)

#Deletando valores
@router.delete("/meses_venda/deletar_valores/{mes}")
async def deleteItem(mes:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await deleteMesService(mes, session, user)
