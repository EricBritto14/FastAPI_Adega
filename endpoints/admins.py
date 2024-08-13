# import models, schemas
# from database import SessionLocal
# from sqlalchemy.orm import Session
# from fastapi import Depends, APIRouter
# from models import *
# from endpoints.loginn import *

# router = APIRouter()

# def get_session(): #Função para pegar a sessão, e abrir e fechar o banco de dados
#     session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()

# @router.get("/admins")
# def getItems(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session
#     if not user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Você não tem permissão para acessar os admins!"
#         )
#     items = session.query(models.Cadastro_Admins).all()
#     return {f"Olá {user.username}, aqui estão os admins: {items}"}

# #Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
# @router.get("/admins/{id}") #Router para trazer as informações de acordo com o id
# def getItem(id:int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
#     if not user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Você não tem permissão para acessar os admins!"
#         )
#     item = session.query(models.Cadastro_Admins).get(id) #Para pegar apenas o valor que for representado pelo id
#     #return fakeDataBase[id] #Retornando o valor do dicionário, de acordo com o ID que ele digitar
#     return {f"Olá {user.username}, aqui está o admin id:{id} - {item}"}

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
# @router.post("/admins/adicionar")
# def addItem(item:schemas.Admins, session: Session = Depends(get_session)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
#     # if not user.is_admin: #, user: Cadastro_Users = Depends(get_current_user)
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED,
#     #         detail="Você não tem permissão para criar um admin!"
#     #     )
#     #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
#     item = models.Cadastro_Admins(username = item.username, email = item.email, senha = get_password_hash(item.senha), is_admin = item.is_admin)
#     session.add(item) #Adicionando no banco
#     session.commit()  #comitando a mudança
#     session.refresh(item) #Dando um refresh para atualizar o banco
#     #fakeDataBase[newId] = {"task":item.task, "valor":item.value} #Indicando que no fakedatabase no novo id, seja adicionado task + o valor que for passado
#     #return fakeDataBase
#     return {f"Olá, adicionando o admin: {item}"}

# ####################################################################################################################################################
# #3 Seria um jeito criando uma requisição com o próprio Body (mas tem muitos problemas desse jeito e não é mto recomendado)
# # @app.post("/")
# # def addItem(body = Body()):
# #     newId = len(fakeDataBase.keys()) + 1
# #     fakeDataBase[newId] = {"task":body['task']}
# #     return fakeDataBase

# #Atualizando valores
# @router.put("/admins/atualizar/{id}")
# def updateItem(id:int, item:schemas.Admins, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
#     if not user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Você não tem permissão de atualizar admins!"
#         )
#     #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
#     itemObject = session.query(models.Cadastro_Admins).get(id) #Pegando o valor que foi passado pelo int, de qual objeto salvo é
#     itemObject.nome, itemObject.email, itemObject.senha = item.nome, item.email, item.senha #atualizando com esses valores novos 
#     session.commit() #comitando a mudança
#     #fakeDataBase[newId] = {"task":item.task, "valor":item.value} #Indicando que no fakedatabase no novo id, seja adicionado task + o valor que for passado
#     #return fakeDataBase
#     return {f"Olá {user.username}, atualizando o admin:{id} para - {itemObject}"}

# #Deletando valores
# @router.delete("/admins/delete/{id}")
# def deleteItem(id:int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
#     if not user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Você não tem permissão para excluir admins!"
#         )
#     #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
#     itemObject = session.query(models.Cadastro_Admins).get(id) #Pegando o valor que foi passado pelo int, de qual objeto salvo é
#     session.delete(itemObject) #comitando a mudança
#     session.commit() #Comitando as mudanças
#     session.close() #Fechando o banco
#     return {f"Olá {user.username}, deletando o admin de id: {id} - {itemObject}"}
    