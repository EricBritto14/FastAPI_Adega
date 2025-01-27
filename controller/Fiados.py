from fastapi import APIRouter, Depends
from requests import Session

from controller.Login import get_current_user
from models.ModelsP import Cadastro_Users
from schemas import SchemasP
from services.fiado.FiadoServices import *
from services.meses.MesesService import *

router = APIRouter()

@router.post("/fiados/adicionar_valores")
async def addValFiado(item: SchemasP.Fiado, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await addFiadoValService(item, session, user)

#Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
@router.get("/fiados") #Router para trazer as informações de acordo com o id
async def getValFiado(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    return await getFiadoServices(session, user)

@router.put("/fiados/atualizar_valores") #Tentar pegar pelo nome, não pelo id
async def updateValFiado(item: SchemasP.Fiado_Att, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await updateFiadoService(item, session, user)