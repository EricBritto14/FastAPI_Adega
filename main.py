from fastapi import FastAPI, Depends, HTTPException #, Response
from sqlalchemy import select
import uvicorn
from endpoints import loginn, produtos, users #, admins
import schemas, models
from endpoints.loginn import *
from schemas import *
from models import *
from logger import logger
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware
from loggs import *
from loggs.middleware import *
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine) #Linha para realmente criar o banco de dados se não tivermos um. Vai criar o banco de dados com as informações que temos no engine do database.py

#Fazer o metodo pra recuperar senha pelo email, e pegar as info não apenas pelo id e pelo nome, mas sim pelos 2 talvez.

async def get_session(): #Função para pegar a sessão, e abrir e fechar o banco de dados
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI(title="API Adega Santa-Dose")#title="API Santa-Dose" #Title para dar nome à api

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(produtos.router, tags=["Produtos"])
app.include_router(users.router, tags=["Usuários"])
# app.include_router(admins.router, tags=["Admins"])
app.include_router(loginn.router, tags=["Login"])
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware) #Jeito certo de registar o middleware no app, para conseguir criar uma classe middleware e só puxar pra cá
logger.info('Starting API...')

@app.get("/")
async def getItems(session: Session = Depends(get_session)): #Pegando os valores do banco de dados, Depends do get_session
    items = session.query(Produtos).all()
    return items

@app.get("/usuarios/teste")
async def getItemss(session: Session = Depends(get_session)):
    usuarios = session.query(Cadastro_Users).all()
    return usuarios

@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    try:
        user = session.query(Cadastro_Users).filter(Cadastro_Users.username == form_data.username.capitalize()).first()
        if user is None: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Usuário incorreto ou inexistente!'
            )
        if not verify_password(form_data.password, user.senha):
             raise HTTPException(
                 status_code=status.HTTP_400_BAD_REQUEST, detail='Senha incorreta!'
             )

        access_token = create_access_token(data={'sub': user.username})
        return {'access_token': access_token, 'token_type': 'bearer'}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Erro ao validar o usuário")

if __name__ == "__main__":
    uvicorn.run('main:app', port=5000, log_level='info')


#Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
# @app.get("/produtos")
# def getItems(session: Session = Depends(get_session)): #Pegando os valores do banco de dados, Depends do get_session
#     items = session.query(models.Produtos).all()
#     return items

# #Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
# @app.get("/{id}") #Router para trazer as informações de acordo com o id
# def getItem(id:int, session: Session = Depends(get_session)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
#     item = session.query(models.Produtos).get(id) #Para pegar apenas o valor que for representado pelo id
#     #return fakeDataBase[id] #Retornando o valor do dicionário, de acordo com o ID que ele digitar
#     return item

# ###################################################################################################################################################
#  #1 tipo de fazer um post, mas apenas é recomendado se for passar 1 ou poucos valores como é o exemplo... caso contrário é melhor fazer de outra forma como o pydantic 
# #@app.post("/") #Router para haver um post de valores no host principal do /
# # def addItem(task:str):  #Criando um addItem, (post), que espera receber uma variável (task) e com os dois pontos :str eu EXIJO que a variável que venha seja string
#     # newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
#     # fakeDataBase[newId] = {"task": task} #Indicando que no fakedatabase no novo id, seja adicionado task + o valor que for passado
#     # return fakeDataBase #Retornando o fakedatabase todo

# ####################################################################################################################################################
# #2 Segundo jeito de fazer e o melhor para vários valores, seria com o pydantic, para passar mais valores e informações, como strings, ints e etc
# #Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
# @app.post("/")
# def addItem(item:schemas.Produtos, session: Session = Depends(get_session)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
#     #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
#     item = models.Produtos(nome = item.nome, tipo = item.tipo, valor = item.valor, quantidade = item.quantidade, tamanho = item.tamanho, data_validade = item.data_validade, data_cadastro = item.data_cadastro)
#     session.add(item) #Adicionando no banco
#     session.commit()  #comitando a mudança
#     session.refresh(item) #Dando um refresh para atualizar o banco
#     #fakeDataBase[newId] = {"task":item.task, "valor":item.value} #Indicando que no fakedatabase no novo id, seja adicionado task + o valor que for passado
#     #return fakeDataBase
#     return item

# ####################################################################################################################################################
# #3 Seria um jeito criando uma requisição com o próprio Body (mas tem muitos problemas desse jeito e não é mto recomendado)
# # @app.post("/")
# # def addItem(body = Body()):
# #     newId = len(fakeDataBase.keys()) + 1
# #     fakeDataBase[newId] = {"task":body['task']}
# #     return fakeDataBase

# #Atualizando valores
# @app.put("/{id}")
# def updateItem(id:int, item:schemas.Produtos, session: Session = Depends(get_session)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
#     #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
#     itemObject = session.query(models.Produtos).get(id) #Pegando o valor que foi passado pelo int, de qual objeto salvo é
#     itemObject.nome, itemObject.tipo, itemObject.valor, itemObject.quantidade, itemObject.tamanho, itemObject.data_validade, itemObject.data_cadastro = item.nome, item.tipo, item.valor, item.quantidade, item.tamanho, item.data_validade, item.data_cadastro #atualizando com esses valores novos 
#     session.commit() #comitando a mudança
#     #fakeDataBase[newId] = {"task":item.task, "valor":item.value} #Indicando que no fakedatabase no novo id, seja adicionado task + o valor que for passado
#     #return fakeDataBase
#     return itemObject

# #Deletando valores
# @app.delete("/{id}")
# def deleteItem(id:int, session: Session = Depends(get_session)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
#     #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
#     itemObject = session.query(models.Produtos).get(id) #Pegando o valor que foi passado pelo int, de qual objeto salvo é
#     session.delete(itemObject) #comitando a mudança
#     session.commit() #Comitando as mudanças
#     session.close() #Fechando o banco
#     return 'O item foi deletado'
