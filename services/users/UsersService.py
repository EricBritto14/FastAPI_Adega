import models.ModelsP as models, schemas.SchemasP as schemas 
import re
from services.getSession.GetSession import *
from fastapi import Depends, HTTPException, UploadFile, status
from controller.Login import *
from models import *
from schemas import *

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
    
async def getItemsAllService(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para visualizar todos os usuários!")
        
        items = session.query(models.Cadastro_Users).all()
        return f"Olá, {user.username}, aqui estão todos os usuários!:", items
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
async def getItemByNameService(username:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Você não tem permissão para visualizar os usuários!")
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
    
async def getItemByIdService(id:int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não tem permissão para visualizar os usuários!")        
        
        usuarioBusca = session.query(models.Cadastro_Users).get(id)
        if not usuarioBusca:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inexistente!")
        else:
            return f"Olá, {user.username}, aqui está o usuário de id:{id} -", usuarioBusca         
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
async def addItemService(username: str,
    email: str,
    senha: str,
    is_admin_raw: str,
    profile_image: UploadFile,
    session: Session): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try:
        # if not user.is_admin:     #, user: Cadastro_Users = Depends(get_current_user)
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Você não tem permissão para adicionar usuários!")
        is_admin = is_admin_raw in ["1", "true", "on"]

        image_path = None
        if profile_image:
            from pathlib import Path
            import uuid

            filename = f"{uuid.uuid4()}_{profile_image.filename}"
            upload_folder = Path("static/profile_images")
            upload_folder.mkdir(parents=True, exist_ok=True)
            file_path = upload_folder / filename

            with open(file_path, "wb") as buffer:
                buffer.write(await profile_image.read())

            image_path = f"profile_images/{filename}"



        item = Cadastro_Users(username = username.capitalize(), email = email, senha = valida_senha(senha), is_admin = is_admin, profile_image= image_path)
        
        usernameT = session.query(models.Cadastro_Users).filter_by(username = item.username).first()
        emailT = session.query(models.Cadastro_Users).filter_by(email = item.email).first()
        
        if usernameT != None:
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
        return {
            "mensagem": f"Usuário {username} adicionado com sucesso!",
            "usuario": {
                "id": item.idUsuario,
                "username": item.username,
                "email": item.email,
                "is_admin": item.is_admin,
                "profile_image": item.profile_image
            }
        }

    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise e
    except Exception as e:
        session.rollback()
        print("Erro:", repr(e))
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
    
async def atualizarByIdService(user_id: int,
    username: Optional[str],
    email: Optional[str],
    is_admin_raw: Optional[str],
    profile_image: Optional[UploadFile],
    session: Session):
    try:
            db_user = session.query(models.Cadastro_Users).filter(models.Cadastro_Users.idUsuario == user_id).first()

            if not db_user:
                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
            
            if username is not None:
                username_real = session.query(models.Cadastro_Users).filter(models.Cadastro_Users.username == username.capitalize(), models.Cadastro_Users.idUsuario != user_id).first();

                if username_real:
                     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username já existente, tente outro!")
                
                db_user.username = username.capitalize()
            
            if email is not None:
                email_exists = session.query(models.Cadastro_Users).filter(models.Cadastro_Users.email == email, models.Cadastro_Users.idUsuario != user_id).first()

                if email_exists:
                     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já existente, tente outro!")
            
                if not email.endswith(('@gmail.com', '@hotmail.com', '@outlook.com')):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email não válido!"
                    )

                db_user.email = email
            
            if is_admin_raw is not None:
                db_user.is_admin = is_admin_raw in ["1", "true", "on"]

            if profile_image:
                from pathlib import Path
                import uuid

                filename = f"{uuid.uuid4()}_{profile_image.filename}"
                upload_folder = Path("static/profile_images")
                upload_folder.mkdir(parents=True, exist_ok=True)
                file_path = upload_folder / filename

                with open(file_path, "wb") as buffer:
                    buffer.write(await profile_image.read())

                db_user.profile_image = f"profile_images/{filename}"

            session.commit()  #comitando a mudança
            session.refresh(db_user) #Dando um refresh para atualizar o banco
            return {
                "mensagem": f"Usuário {db_user.username} atualizado com sucesso!",
                "usuario": db_user
            }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
async def deleteItemService(nome:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try:    
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para excluir usuários!")

        itemObject = session.query(models.Cadastro_Users).filter_by(username=nome.capitalize()).first() #Pegando o valor que foi passado pelo int, de qual objeto salvo é
        
        if not itemObject:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome de usuário não existe")
        
        id = itemObject.idUsuario
        session.delete(itemObject) #comitando a mudança
        session.commit() #Comitando as mudanças
        session.close() #Fechando o banco
        return f"Olá {user.username}, o usuário de nome:{nome} e id {id}, foi excluido!", itemObject
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
async def deleteItemIdService(id: int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não tem permissão para excluir usuários!")
        
        itemId = session.query(models.Cadastro_Users).get(id)
        if not itemId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Id de usuário inexistente!")      
        
        nomeUser = itemId.username
        session.delete(itemId)
        session.commit()
        session.close()
        return f"Olá {user.username}, o usuário de id:{id} e nome {nomeUser}, foi excluído!", itemId    
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))