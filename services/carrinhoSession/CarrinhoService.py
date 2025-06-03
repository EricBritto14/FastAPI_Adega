import logging
import models.ModelsP as modelsP
from models.ModelsP import *
import schemas.SchemasP as schemasP
from services.getSession.GetSession import *
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from controller.Login import get_current_user

async def getVendasService(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        vendas = session.query(modelsP.Venda_Carrinho).all()
        if not vendas:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Nenhuma venda de carrinho existente!")
        else: 
            return f"Pegando todos as vendas de carrinho para você, {user.username}", vendas
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def getVendasTipoService(tipo: str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        vendas = session.query(modelsP.Venda_Carrinho).get(tipo)
        if not vendas:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Nenhum valor encontrado com este tipo de venda!")
        else:
            return f"Pegando todos as vendas de carrinho do tipo {tipo} para você, {user.username}", vendas
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def addVendaService(item: schemasP.CarrinhoVenda, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        item = modelsP.Venda_Carrinho(
            tipo_venda = item.tipo_venda.capitalize(),
            valor_venda = item.valor_venda
        )

        if item.tipo_venda not in ( "Pix", "Cartão de debito", "Cartão de crédito", "Dinheiro", "Fiado" ):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de pagamento não válido!")
        
        if item.valor_venda <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valor de venda total igual inválido (0 ou menor que 0)")
        
        vendaCarrinho = modelsP.Venda_Carrinho(
            tipo_venda = item.tipo_venda,
            valor_venda = item.valor_venda
        )

        session.add(vendaCarrinho)
        session.commit()
        session.refresh(vendaCarrinho)
        logging.info("Venda no carrinho adicionada com sucesso.")
        return f"Olá, {user.username}, valor e tipo de venda adicionado com sucesso!", item
    except HTTPException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        logging.error(f"Erro interno: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")
