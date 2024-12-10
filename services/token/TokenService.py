from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from services.getSession.GetSession import *
from sqlalchemy.orm import Session
from models.models import *
from controller.Login import *

def login_for_access_token_service(
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