import logging
import models.ModelsP as modelsP, schemas.SchemasP as schemasP
from sqlalchemy.orm import Session
from services.getSession.GetSession import *
from fastapi import Depends, HTTPException, status
from models.ModelsP import *
from controller.Login import get_current_user

async def getFiadoServices(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session. E verificando se o usuário está logado, com o get_current_user
    try:
        valores = session.query(modelsP.Fiado_Val).all()
        if valores is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum valor salvo!")
        else:
            return f"Pegando todos os mêses para você, {user.username}", valores
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def addFiadoValService(item: schemasP.Fiado, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para adicionar dividores fiados!")            
        
        #Criando um objeto para manipular e apenas retornar a % de ganho em cima do produto em _valor_venda
        item = modelsP.Fiado_Val(
            dia=item.dia,
            valor=item.valor,
            name = item.name,
        )
        
        # produtoMes = session.query(modelsP.Fiado_Val).filter(modelsP.Fiado_Val.dia == item.dia).first()
        # if produtoMes is not None:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valor já adicionado para este dia!")

        #Criando o novo produto no banco
        novo_produto_mes = modelsP.Fiado_Val(
            dia=item.dia,
            valor=item.valor,
            name = item.name,
        )

        session.add(novo_produto_mes)
        session.commit()
        session.refresh(novo_produto_mes)
        logging.info("Valor adicionado para o(s) dia(s) com sucesso.")
        return f"Olá, {user.username}, o valor para o(s) dia(s) desejado(s) foi adicionado!", item
    except HTTPException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        logging.error(f"Erro interno: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

async def updateFiadoService(item:schemasP.Fiado, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para adicionar dividores fiados!")
        
        itemObject = session.query(modelsP.Fiado_Val).filter_by(dia=item.dia).first() #Pegando o valor que foi passado pelo int, de qual objeto salvo é
        
        if itemObject is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dia não encontrado")
        
        itemObject.dia = item.dia
        if item.valor is None:
            itemObject.valor = 0
        else:
            itemObject.valor = item.valor
        itemObject.name = item.name
        
        if not item.dia:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dia vazio! Selecione um valor.")
        
        # produto = session.query(modelsP.Fiado_Val).filter_by(dia = item.dia).first()
        # 
        # if produto == None:
            # return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Mês de nome {item.dia} já existente!")
            
        # if item.valor <= 0:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A venda total do mês não pode ser menor ou igual a 0!")
        
        session.commit() #comitando a mudança
        session.refresh(itemObject)
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
async def deleteItemByIdSpun(id: int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem autorização para deletar produtos!")
    
        item = session.query(modelsP.Fiado_Val).get(id)
        if item is None:
            # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Produto de id:{id}, não encontrado")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dívida de id:{}, não encontrado".format(id))
        produto = item.name
        session.delete(item)
        session.commit()
        session.close()
        return "Olá {}, a dívida de id:{} e do proprietário de nome:{}, foi deletado! Dívidas:".format(user.username, id, produto), item
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    