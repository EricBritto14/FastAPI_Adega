from fastapi import APIRouter, Depends
from requests import Session

from controller.Login import get_current_user
from models.ModelsP import Cadastro_Users
from schemas import SchemasP
from services.gastosCartoes.GastosCartoesService import *

router = APIRouter()

@router.patch("/gastos_cartao/adicionar_valores")
async def addExpensesCard(item: SchemasP.Gastos_Aleatorios_Mes, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await addExpensesCardMonthService(item, session, user)

@router.patch("/gastos_cartao/adicionar_valores_dias")
async def addExpensesCardDay(item: SchemasP.Gastos_Aleatorios, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await addDaysExpensesCardService(item, session, user)

@router.get("/gastos_cartao/{mes}") #Router para trazer as informações de acordo com o id
async def getExpensesCard(mes: str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    return await getDaysExpensesCardServices(mes, session, user)

#Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
@router.get("/gastos_cartao") #Router para trazer as informações de acordo com o id
async def getBillAll(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    return await getExpensesCardServices(session, user)

# @router.put("/boletos/atualizar_valores/{mes}") #Tentar pegar pelo nome, não pelo id
# async def updateBill(mes:str, item: SchemasP.Meses_Valores_Att, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
#     return await updateMesService(mes, item, session, user)

#Deletando valores
@router.delete("/gastos_cartao/deletar_valores/{mes}")
async def deleteBill(mes:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await deleteExpensesCardMonthService(mes, session, user)
