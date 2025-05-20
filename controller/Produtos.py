import schemas.SchemasP as schemasP
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter #APIRouter para fazer as rotas
from controller.Login import *
from services.getSession.GetSession import *
from services.produtos.ProdutosService import *

router = APIRouter() #Criando o router para por no lugar do @app.get, vai virar router.get

@router.get("/produtos")
async def getItems(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session. E verificando se o usuário está logado, com o get_current_user
    return await getItemsServices(session, user)

#Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
@router.get("/produtos/produto_name/{tipo}") #Router para trazer as informações de acordo com o id
async def getItem(tipo:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    return await getItemByTipoService(tipo, session, user)

@router.get("/produtos/produto_id/{id}")
async def getItemId(id:int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await getItemIdService(id, session, user)

@router.post("/produtos/adicionar")
async def addItem(item:schemasP.Produtos_S, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await addItemService(item, session, user)

@router.post("/produtos/totalWtipo")
async def addTotalwTipo(item:schemasP.Produtos_TeT, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await addTotalEOpcaoVenda(item, session, user)

@router.patch("/produtos/atualizar_by_name/{nome}") #Tentar pegar pelo nome, não pelo id
async def updateItem(nome:str, item:schemasP.AttProdutos, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await updateItemService(nome, item, session, user)

@router.patch("/produtos/atualizar_by_id/{id}")
async def atualizarItemId(id: int, item:schemasP.AttProdutos, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await atualizarItemIdService(id, item, session, user)

@router.get("/produtos/totalWtipos")
async def getItemTipoQuantidade(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await getItemTiposQuantidades(session, user)

#Deletando valores
@router.delete("/produtos/delete_by_name/{nome}")
async def deleteItem(nome:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    return await deleteItemService(nome, session, user)

@router.delete("/produtos/delete_by_id/{id}")
async def deleteItemById(id: int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    return await deleteItemByIdService(id, session, user)
    