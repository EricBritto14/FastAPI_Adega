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

def valida_senha(senha : str):
    if len(senha) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha com menos caracteres que o mínimo(8)!"
            )
    elif not re.search("[A-Z]", senha):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve ter pelo menos 1 caractere maíusculo!"
            )
        
    elif not re.search("[a-z]", senha):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve contar pelo menos 1 caractere mínusculo!"
            )

    elif not re.search("[!@#$%¨^&*()_+]", senha):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve contar pelo menos 1 caractere especial!"
            )
    elif not re.search("[0-9]", senha):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve conter pelo menos 1 caractere númerico!"
            )
    else:
        return get_password_hash(senha)


@router.get("/usuarios")
def getItems(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para visualizar todos os usuários!"
        )
    try:
        items = session.query(models.Cadastro_Users).all()
        return f"Olá, {user.username}, aqui estão todos os usuários!:", items
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/usuarios/{id}") #Router para trazer as informações de acordo com o id
def getItem(id:int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para visualizar o usuário {id}!"
        )
    try:
        item = session.query(models.Cadastro_Users).get(id) #Para pegar apenas o valor que for representado pelo id
        #return fakeDataBase[id] #Retornando o valor do dicionário, de acordo com o ID que ele digitar
        return f"Olá, {user.username}, aqui está o usuário de id:{id} -", item
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/usuarios/adicionar")
def addItem(item:Cadastro, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    if not user.is_admin:     #, user: Cadastro_Users = Depends(get_current_user)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para adicionar usuários!"
        )
    try:
        item = Cadastro_Users(username = item.username, email = item.email, senha = valida_senha(item.senha), is_admin = item.is_admin)
        #Validação de email, pro cara n por qlqr coisa
        if not item.email.endswith(('@gmail.com', '@hotmail.com', '@outlook.com')):
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

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
                    # Aqui, todas as outras validações podem ser realizadas
                    # Se todas as validações passarem, agora podemos hash a senha
        itemObject.username, itemObject.email, itemObject.is_admin, itemObject.senha = item.username, item.email, item.is_admin, valida_senha(item.senha)
                # Validar e-mail antes de validar a senha
        if not itemObject.email.endswith(('@gmail.com', '@outlook.com', '@hotmail.com')):
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email não válido!"
                )

        session.commit() #comitando a mudança
        return f"Olá {user.username}, o usuário desejado foi atualizado para:", itemObject

    except Exception as e:
        session.rollback()
        print("goddamn", str(e))   
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou nome de usuário  já registrado!")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
           

#Deletando valores
@router.delete("/usuarios/delete/{id}")
def deleteItem(id:int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para excluir usuários!"
        )
    try:
        #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
        itemObject = session.query(models.Cadastro_Users).get(id) #Pegando o valor que foi passado pelo int, de qual objeto salvo é
        session.delete(itemObject) #comitando a mudança
        session.commit() #Comitando as mudanças
        session.close() #Fechando o banco
        return f"Olá {user.username}, o usuário de id:{id} foi excluido!", itemObject
    except Exception as e:
        session.rollback()
        if "Class 'builtins.NoneType' is not mapped" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O id do usuário digitado não existe.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro no servidor!")