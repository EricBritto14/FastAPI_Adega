import logging
import models.ModelsP as modelsP, schemas.SchemasP as schemasP
from sqlalchemy.orm import Session
from services.getSession.GetSession import *
from fastapi import Depends, HTTPException, status
from models.ModelsP import *
from controller.Login import get_current_user

async def addBillsMonthService(item: schemasP.Meses_Valores_Bill, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para adicionar valores de boletos aos mêses!")
        
        #Criando um objeto para manipular e apenas retornar a % de ganho em cima do produto em _valor_venda
        item = modelsP.Meses_Valores_Bill_Cad(
            mes=item.mes.capitalize(),
            valor=item.valor,
        )
        
        if not isinstance(item.mes, str):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome de mês inválido.")

        produtoMes = session.query(modelsP.Meses_Valores_Bill_Cad).filter(modelsP.Meses_Valores_Bill_Cad.mes == item.mes).first()
        
        if item.valor <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O valor total de boletos no mês não pode ser menor ou igual a 0!")
        
        if produtoMes:
            produtoMes.valor = item.valor 
            session.commit()
            session.refresh(produtoMes)
            logging.info("Valor total de Boletos atualizado para o mês com sucesso.")
            return f"Olá, {user.username}, o valor total de boletos para o mês desejado foi adicionado!", item
        else:
            #Criando o novo produto no banco
            novo_produto_mes = modelsP.Meses_Valores_Bill_Cad(
                mes=item.mes.capitalize(),
                valor=item.valor,
            )

            session.add(novo_produto_mes)
            session.commit()
            session.refresh(novo_produto_mes)
            logging.info("Boleto adicionado para o mês com sucesso.")
            return f"Olá, {user.username}, o boleto para o mês desejado foi adicionado!", item
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
    
async def addDaysBillsService(item: schemasP.Dias_Valores_Mes_Bill, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para adicionar novos valores de boletos!")            

        produtoMes = (
            session.query(modelsP.Dias_Valores_Mes_Bill_Cad)
            .filter(
                modelsP.Dias_Valores_Mes_Bill_Cad.dia == item.dia,
                modelsP.Dias_Valores_Mes_Bill_Cad.mes == item.mes  
            )
            .first()
        )
        
        if produtoMes:
            produtoMes.valor = item.valor
            session.commit()
            session.refresh(produtoMes)
            logging.info("Boleto atualizado para o(s) dia(s) com sucesso.")
            return f"Olá, {user.username}, o valor dos boletos atualizado!", item
        else:
            #Criando o novo produto no banco
            novo_produto_dia_venda = modelsP.Dias_Valores_Mes_Bill_Cad(
                dia=item.dia,
                valor=item.valor,
                mes=item.mes
            )

            session.add(novo_produto_dia_venda)
            session.commit()
            session.refresh(novo_produto_dia_venda)
            logging.info("Boleto criado para o(s) dia(s) e mês selecionado com sucesso!")
            return f"Olá, {user.username}. Novo boleto foi adicionado para o dia {item.dia} e mês {item.mes}"
        
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
    
async def getDaysBillsServices(mes: str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session. E verificando se o usuário está logado, com o get_current_user
    try:
        mes = session.query(modelsP.Dias_Valores_Mes_Bill_Cad).filter_by(mes=mes.capitalize()).all()
        if not mes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum boleto existente neste mês!")
        else:
            return f"Pegando todos os valores de boletos para você, {user.username}", mes
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def getBillsServices(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session. E verificando se o usuário está logado, com o get_current_user
    try:
        mes = session.query(modelsP.Meses_Valores_Bill_Cad).all()
        if not mes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum mês existente!")
        else:
            return f"Pegando todos os mêses para você, {user.username}", mes
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))
    

# async def updateMesService(mes:str, item:schemasP.Meses_Valores, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
#     try:
#         itemObject = session.query(modelsP.Meses_Valores_Cad).filter_by(mes=mes.capitalize()).first() #Pegando o valor que foi passado pelo int, de qual objeto salvo é
        
#         if itemObject is None:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mês não encontrado")
        
#         itemObject.mes,itemObject.valor = item.mes, item.valor
        
#         if not item.mes:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mês vazio! Selecione um valor.")
        
#         produto = session.query(modelsP.Meses_Valores_Cad).filter_by(mes = item.mes).first()
        
#         if produto == None:
#             return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Mês de nome {item.mes} já existente!")
            
#         if item.valor <= 0:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A venda total do mês não pode ser menor ou igual a 0!")
        
#         session.commit() #comitando a mudança
#     except Exception as e:
#         session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
async def deleteBillsMonthService(mes:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try: 
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para deletar boletos!"
            )
    
        #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
        itemObject = session.query(modelsP.Meses_Valores_Bill_Cad).filter_by(mes=mes.capitalize()).first() #Pegando o valor que foi passado pelo nome, e procurando no bnaco pra ver se existe algo com esse nome
        if not itemObject:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Boleto no mês: {mes}, não encontrado")
        id = itemObject.idMes
        session.delete(itemObject) #comitando a mudança
        session.commit() #Comitando as mudanças
        session.close() #Fechando o banco
        return f"Olá {user.username}, o boleto {mes} e id {id}, foi deletado! Produto:", itemObject
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))
