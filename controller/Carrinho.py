from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas.SchemasP as schemasP

from services.getSession.GetSession import *
from controller.Login import *
from models.ModelsP import Cadastro_Users
from services.carrinhoSession.CarrinhoService import *

router = APIRouter()

@router.get("/vendasCarrinho")
async def getVendas(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await getVendasService(session, user)

@router.get("/vendasCarrinho/{tipo}")
async def getVendasTipo(tipo: str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await getVendasTipoService(tipo, session, user)

@router.post("/vendasCarrinho")
async def addVenda(item: schemasP.CarrinhoVenda, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await addVendaService(item, session, user)