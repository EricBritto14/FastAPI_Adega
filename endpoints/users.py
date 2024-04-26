from sqlalchemy import null
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

async def get_session(): #Função para pegar a sessão, e abrir e fechar o banco de dados
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
async def getItems(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para visualizar todos os usuários!")
        
        items = session.query(models.Cadastro_Users).all()
        return f"Olá, {user.username}, aqui estão todos os usuários!:", items
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.get("/usuarios/{nome}") #Router para trazer as informações de acordo com o id
async def getItem(username:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Você não tem permissão para visualizar o usuário:{username}!")
        #Descobrir o pq este item está retornando null, e depois ajeitar todos os routers abaixo deste. Os de produtos já estão certos!
        item = session.query(models.Cadastro_Users).filter_by(username=username.capitalize()).first() #Para pegar apenas o valor que for representado pelo id
        #return fakeDataBase[id] #Retornando o valor do dicionário, de acordo com o ID que ele digitar
        if item == None: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário não encontrado!")
        else:
            return f"Olá, {user.username}, aqui está o usuário de nome:{username} -", item
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.post("/usuarios/adicionar")
async def addItem(item:Cadastro, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try:
        if not user.is_admin:     #, user: Cadastro_Users = Depends(get_current_user)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Você não tem permissão para adicionar usuários!")
    
        item = Cadastro_Users(username = item.username.capitalize(), email = item.email, senha = valida_senha(item.senha), is_admin = item.is_admin)
        
        username = session.query(models.Cadastro_Users).filter_by(username = item.username).first()
        emailT = session.query(models.Cadastro_Users).filter_by(email = item.email).first()
        
        if username != None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username já existente, tente outro!")
        
        if emailT != None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já existente, tente outro!")
        
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
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))

#Atualizando valores
@router.put("/usuarios/atualizar/{nome}")
async def updateItem(nome:str, item:schemas.Cadastro, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Você não tem permissão para atualizar")   
    
        itemObject = session.query(models.Cadastro_Users).filter_by(username=nome.capitalize()).first() #Pegando o valor que foi passado pelo int, de qual objeto salvo é
                    # Aqui, todas as outras validações podem ser realizadas
                    # Se todas as validações passarem, agora podemos hash a senha
        if itemObject is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inexistente!")
        #Pegando o username digitado para atualizar
        usernameN = item.username.capitalize()
        newUsername = session.query(models.Cadastro_Users).filter_by(username = usernameN).first() #Está procurando no banco o novo nome de usuário que o cara quer atualizar, se tiver, vai dar o erro de baixo, se não vai da bom
        
        if newUsername != None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome de usuário já existente!")
        
        #Pegando o email digitado para atualizar
        emailN = item.email
        newEmail = session.query(models.Cadastro_Users).filter_by(email = emailN).first()#Está procurando no banco o novo email que o cara quer atualizar, se tiver, vai dar o erro de baixo, se não vai da bom
        
        if newEmail != None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este email já está sendo usado!")
        
        itemObject.username, itemObject.email, itemObject.is_admin, itemObject.senha = item.username.capitalize(), item.email, item.is_admin, valida_senha(item.senha)
        
        #Continuar a partir daqui os testes de caso, o do produto já está tudo feito. Após isso, colocar pra funcionar com o ID também as coisas, não apenas com o nome. E por fim, tentar fazer como os "componentes" de front-end e reaproveitar melhor o código, principalmente esses session.query de procurar no banco, da pra fazer uma def e só passar os valores, invez de repetir o código.
        if not itemObject.email.endswith(('@gmail.com', '@outlook.com', '@hotmail.com')):
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email não válido!"
                )

        session.commit() #comitando a mudança
        return f"Olá {user.username}, o usuário desejado foi atualizado para:", itemObject

    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.put("/usuarios/atualizar_by_id/{id}")
async def atualizarById(id: int, item:schemas.Produtos, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado!")
        #Continuar daqui do atualizar usuarios id, deixar tudo com o id também funcionando. E por fim, tentar fazer como os componentes de front-end e reaproveitar melhor o código, principalmente esses session.query de procurar no banco, da pra fazer uma def e só passar os valores, invez de repetir o código.
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=str(e)) 
      

#Deletando valores
@router.delete("/usuarios/delete/{nome}")
async def deleteItem(nome:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try:    
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para excluir usuários!")

        itemObject = session.query(models.Cadastro_Users).filter_by(username=nome.capitalize()).first() #Pegando o valor que foi passado pelo int, de qual objeto salvo é
        
        if itemObject is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome de usuário não existe")
        
        id = itemObject.idUsuario
        session.delete(itemObject) #comitando a mudança
        session.commit() #Comitando as mudanças
        session.close() #Fechando o banco
        return f"Olá {user.username}, o usuário de nome:{nome} e id {id}, foi excluido!", itemObject
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
@router.delete("/users/delete_by_id/{id}")
async def deleteItemId(id: int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não tem permissão para excluir usuários!")
        
        itemId = session.query(models.Cadastro_Users).get(id)
        if itemId is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Id de usuário inexistente!")      
        
        nomeUser = itemId.username
        session.delete(itemId)
        session.commit()
        session.close()
        return f"Olá {user.username}, o usuário de id:{id} e nome {nomeUser}, foi excluído!", itemId    
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))