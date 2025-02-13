from fastapi import APIRouter, Depends
from requests import Session

from controller.Login import get_current_user
from models.ModelsP import Cadastro_Users
from schemas import SchemasP
from services.boletos.BoletosService import *

router = APIRouter()

@router.patch("/boletos/adicionar_valores")
async def addBill(item: SchemasP.Meses_Valores_Bill, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await addBillsMonthService(item, session, user)

@router.patch("/boletos/adicionar_valores_dias")
async def addBillDay(item: SchemasP.Dias_Valores_Mes_Bill, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await addDaysBillsService(item, session, user)

@router.get("/dias_boletos/{mes}") #Router para trazer as informações de acordo com o id
async def getBill(mes: str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    return await getDaysBillsServices(mes, session, user)

#Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
@router.get("/boletos") #Router para trazer as informações de acordo com o id
async def getBillAll(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    return await getBillsServices(session, user)

# @router.put("/boletos/atualizar_valores/{mes}") #Tentar pegar pelo nome, não pelo id
# async def updateBill(mes:str, item: SchemasP.Meses_Valores_Att, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
#     return await updateMesService(mes, item, session, user)

#Deletando valores
@router.delete("/boletos/deletar_valores/{mes}")
async def deleteBill(mes:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await deleteBillsMonthService(mes, session, user)
