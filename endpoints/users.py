import models, schemas
from endpoints.loginn import *
from models import *
from schemas import *
# from login import *
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
import re #re e pydantic validator, fundamentais para a validação do email que o cara for passar


router = APIRouter()

def get_session(): #Função para pegar a sessão, e abrir e fechar o banco de dados
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@router.get("/usuarios")
def getItems(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para visualizar todos os usuários!"
        )
    items = session.query(models.Cadastro_Users).all()
    return f"Olá, {user.username}, aqui estão todos os usuários!:", items

#Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
@router.get("/usuarios/{id}") #Router para trazer as informações de acordo com o id
def getItem(id:int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para visualizar o usuário {id}!"
        )
    item = session.query(models.Cadastro_Users).get(id) #Para pegar apenas o valor que for representado pelo id
    #return fakeDataBase[id] #Retornando o valor do dicionário, de acordo com o ID que ele digitar
    return f"Olá, {user.username}, aqui está o usuário de id:{id} -", item

###################################################################################################################################################
 #1 tipo de fazer um post, mas apenas é recomendado se for passar 1 ou poucos valores como é o exemplo... caso contrário é melhor fazer de outra forma como o pydantic 
#@app.post("/") #Router para haver um post de valores no host principal do /
# def addItem(task:str):  #Criando um addItem, (post), que espera receber uma variável (task) e com os dois pontos :str eu EXIJO que a variável que venha seja string
    # newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
    # fakeDataBase[newId] = {"task": task} #Indicando que no fakedatabase no novo id, seja adicionado task + o valor que for passado
    # return fakeDataBase #Retornando o fakedatabase todo

####################################################################################################################################################
#2 Segundo jeito de fazer e o melhor para vários valores, seria com o pydantic, para passar mais valores e informações, como strings, ints e etc
#Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados

def valida_senha(password : str):
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha com menos caracteres que o mínimo(8)!"
        )
    if not re.search("[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve ter pelo menos 1 caractere maíusculo!"
        )
    
    if not re.search("[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve contar pelo menos 1 caractere mínusculo!"
        )

    if not re.search("[!@#$%¨^&*()_+]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve contar pelo menos 1 caractere especial!"
        )
    if not re.search("[0-9]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve conter pelo menos 1 caractere númerico!"
        )

@router.post("/usuarios/adicionar")
def addItem(item:Cadastro, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    if not user.is_admin:     #, user: Cadastro_Users = Depends(get_current_user)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para adicionar usuários!"
        )
    try:
        valida_senha(item.senha)
        item = Cadastro_Users(username = item.username, email = item.email, senha = get_password_hash(item.senha), is_admin = item.is_admin)
        #Validação de email, pro cara n por qlqr coisa
        if not item.email.endswith('@gmail.com'):
            if not item.email.endswith('@hotmail.com'):
                if not item.email.endswith('@outlook.com'):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email não válido!"
                    )
        session.add(item) #Adicionando no banco
        session.commit()  #comitando a mudança
        session.refresh(item) #Dando um refresh para atualizar o banco
        return f"Olá adicionando o usuário:", item

    except Exception as e:
        session.rollback()
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou nome de usuário  já registrado!")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro no servidor")

#Atualizando valores
@router.put("/usuarios/atualizar/{id}")
def updateItem(id:int, item:schemas.Cadastro, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar"
        )
    #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
    try:
        itemObject = session.query(models.Cadastro_Users).get(id) #Pegando o valor que foi passado pelo int, de qual objeto salvo é
        #valida_senha(itemObject.senha)
        itemObject.username, itemObject.email, itemObject.senha, itemObject.is_admin = item.username, item.email, item.senha, item.is_admin #atualizando com esses valores novos 
        if not itemObject.email.endswith('@gmail.com'):
            if not itemObject.email.endswith('@hotmail.com'):   #Descobrir o pq não ta funcionando a validação de email aqui, e o da senha também!!
                if not itemObject.email.endswith('@outlook.com'):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email não válido!"
                    )
        session.commit() #comitando a mudança
        #fakeDataBase[newId] = {"task":item.task, "valor":item.value} #Indicando que no fakedatabase no novo id, seja adicionado task + o valor que for passado
        #return fakeDataBase
        return f"Olá {user.username}, o usuário desejado foi atualizado para:", itemObject

    except Exception as e:
        session.rollback()
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou nome de usuário  já registrado!")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro no servidor")

#Deletando valores
@router.delete("/usuarios/delete/{id}")
def deleteItem(id:int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para excluir usuários!"
        )
    #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
    itemObject = session.query(models.Cadastro_Users).get(id) #Pegando o valor que foi passado pelo int, de qual objeto salvo é
    session.delete(itemObject) #comitando a mudança
    session.commit() #Comitando as mudanças
    session.close() #Fechando o banco
    return f"Olá {user.username}, o usuário de id:{id} foi excluido!", itemObject
    