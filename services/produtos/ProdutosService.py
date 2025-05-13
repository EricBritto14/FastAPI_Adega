import logging
import models.ModelsP as modelsP, schemas.SchemasP as schemasP
import datetime
import re
from sqlalchemy.orm import Session
from datetime import datetime, date
from services.getSession.GetSession import *
from fastapi import Depends, HTTPException, status
from models.ModelsP import *
from controller.Login import get_current_user

data_hoje = date.today()

#Validando se está vindo em formato de data, e se a data de vencimendo do produto é menor que a data de hoje ou não
def validar_data(data_val: str) -> str:
    try:
        data_formatada = datetime.strptime(data_val, '%d/%m/%Y').date()
        data_hoje = date.today()

        # Verifica se a data é futura
        if data_formatada > data_hoje:
            print(f"Data de validade formatada: {data_formatada}")
            print(f"Data de hoje: {data_hoje}")
            # Retorna a data em formato padrão para salvar no banco
            return data_formatada.strftime('%Y-%m-%d')
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data de validade menor ou igual à data de hoje!"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de data inválido! Use DD/MM/AAAA."
        )

async def getItemsServices(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session. E verificando se o usuário está logado, com o get_current_user
    try:
        items = session.query(modelsP.Produtos_Cad).all()
        if not items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum produto existente!")
        else:
            return f"Pegando todos os itens para você, {user.username}", items
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
async def getItemByTipoService(tipo:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    try:
        item = session.query(modelsP.Produtos_Cad).filter_by(tipo=tipo.capitalize()).all()
        print("item que está buscando:", item)
        if not item:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto de nome:{}, não encontrado".format(tipo))
        #return fakeDataBase[id] #Retornando o valor do dicionário, de acordo com o ID que ele digitar
        return f"Pegando o produto de nome:{tipo} para você, {user.username}", item
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))

async def getItemIdService(id:int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        itemId = session.query(modelsP.Produtos_Cad).get(id)
        if not itemId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto inexistente!")
        else:
            return f"Pegando o produto de id:{id} para você, {user.username}", itemId   
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))

async def addItemService(item: schemasP.Produtos_S, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para adicionar produtos!")
        
        #Criando um objeto para manipular e apenas retornar a % de ganho em cima do produto em _valor_venda
        item = modelsP.Produtos_Cad(
            nome=item.nome.capitalize(),
            tipo=item.tipo.capitalize(),
            valor_compra=item.valor_compra,
            valor_venda=item.valor_venda,
            quantidade=item.quantidade,
            tamanho=item.tamanho.lower(),
            data_validade=item.data_validade,
        )
        
        if not isinstance(item.nome, str):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome do produto inválido.")

        # tipo = session.query(modelsP.Produtos_Cad).filter(modelsP.Produtos_Cad.tipo == item.tipo).first()
        # produto = session.query(tipo).filter(modelsP.Produtos_Cad.nome == item.nome).first()
        # if produto is not None:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto já adicionado!")
        
        print("item que está vindo: ", item.tipo)
        if item.tipo not in (
            'Doses',
            'Barrigudinhas', 'Cerveja 269mla', 'Cerveja long neck 330mla', 'Cerveja 350mla', 'Cerveja tubaoa', 'Cerveja 600mla', 
            'Cerveja 269mlna', 'Cerveja long neck 330mlna', 'Cerveja 350mlna', 'Cerveja tubaona', 'Cerveja 600mlna',
            'Whiskyg', 'Ging', 'Vodkag', 'Cachacag', 'Licorg', 'Vinhos',
            'Whiskyc2l', 'Ginc2l', 'Vodkac2l', 'Whiskycel', 'Gincel', 'Vodkacel',  
            'Drinks prontos',
            'Combo vodka', 'Combo gin', 'Combo whisky', 
            'Refrigerante descartavel', 'Refrigerante retornavel', 'Refrigerante 1l', 'Refrigerante 600ml', 'Refrigerante 200ml', 'Refrigerante lata',
            'Gatorade', 'Energeticos 2l', 'Energeticos lata 473ml', 'Energeticos lata 269ml',
            'Isqueiros', 'Cigarros', 'Palheiros', 'Piteira', 'Tabaco', 'Slick', 'Cuia', 'Sedas', 'Essencias', 'Carvao narga',
            'Carvao', 'Gelo', 'Fabitos', 'Batata', 'Torcida',
            'Balas', 'Chiclete', 'Doces de pote', 'Chocolate', 'Pirulito'
            ):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de produto não disponível")

        validar_data(item.data_validade)

        if item.valor_compra <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valor de compra do produto não pode ser menor ou igual a 0!")

        if item.valor_venda <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valor de venda do produto não pode ser menor ou igual a 0!")

        if item.quantidade <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantidade do produto não pode ser igual ou menor que 0!")

        if not re.fullmatch(r"\d+(ml|l|g|kg)", item.tamanho, re.IGNORECASE):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tamanho desconhecido (ml/L/G/Kg)!")
        
        #Criando o novo produto no banco
        novo_produto = modelsP.Produtos_Cad(
            nome=item.nome.capitalize(),
            tipo=item.tipo.capitalize(),
            valor_compra=item.valor_compra,
            valor_venda=item.valor_venda,
            quantidade=item.quantidade,
            tamanho=item.tamanho.lower(),
            data_validade=item.data_validade,
        )

        session.add(novo_produto)
        session.commit()
        session.refresh(novo_produto)
        logging.info("Produto adicionado com sucesso.")
        return f"Olá, {user.username}, o produto desejado foi adicionado!", item
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

async def updateItemService(nome:str, item:schemasP.AttProdutos, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try:
        itemObject = session.query(modelsP.Produtos_Cad).filter_by(nome=nome.capitalize()).first() #Pegando o valor que foi passado pelo int, de qual objeto salvo é
        
        if not itemObject:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto não encontrado")
        
        itemObject.nome, itemObject.tamanho, itemObject.tipo, itemObject.valor_compra, itemObject.valor_venda, itemObject.quantidade, itemObject.data_validade = item.nome, item.tamanho, item.tipo.capitalize(), item.valor_compra, item.valor_venda, item.quantidade, item.data_validade
        
        if not item.nome:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome vazio! Coloque um valor.")
        
        produto = session.query(modelsP.Produtos_Cad).filter_by(nome = item.nome).first()
        
        if produto == None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Produto de nome {item.nome} já existente!")
            
        if not re.search("[0-9][ml, L, G, Kg]", item.tamanho):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tamanho desconhecido (ml/L/G/Kg)!")

        if not itemObject.tipo in ('Barrigudinhas', 'Comida', 'Refrigerante Descartável', 'Refrigerante Retornável', 
                             'Refrigerante Lata', 'Doses', 'Vinhos', 'Energéticos De Lata', 'Energéticos 2L', 
                             'Cigarros', 'Palheiros', 'Sedas', 'Carvão', 'Gelo', 'Fabitos', 'Batata', 'Torcida', 'Doces'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de produto não disponível")
        
        if item.valor_compra <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valor de compra do produto não pode ser menor ou igual a 0!")
        
        if item.valor_venda <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valor de venda do produto não pode ser menor ou igual a 0!")
        
        if item.quantidade <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantidade de produto não pode ser menor ou igual que 0!")
        
        validar_data(itemObject.data_validade)
        
        session.commit() #comitando a mudança
        if item.quantidade <= 10:
            return f"Atualizando o produto de nome:{nome}, {user.username}. Para: ", itemObject, f"Atenção {user.username} o produto {itemObject.nome} chegou na quantidade mínima 10! Agora está em {item.quantidade}, fica esperto!"
        else:
            return f"Atualizando o produto de nome:{nome}, {user.username}. Para: ", itemObject
        
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
async def atualizarItemIdService(id: int, item:schemasP.AttProdutos, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        itemObject2 = session.query(modelsP.Produtos_Cad).get(id)
        
        if not itemObject2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Produto de id:{id} inexistente!")
        
        itemObject2.nome, itemObject2.tamanho, itemObject2.tipo, itemObject2.valor_compra, itemObject2.valor_venda, itemObject2.quantidade, itemObject2.data_validade = item.nome, item.tamanho, item.tipo.capitalize(), item.valor_compra, item.valor_venda, item.quantidade, item.data_validade
        
        if not item.nome:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome vazio! Coloque um valor.")
        
        produto = session.query(modelsP.Produtos_Cad).filter_by(nome = item.nome).first()
        
        if produto == None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Produto de nome {item.nome} já existente!")
            
        if not re.search("[0-9][ml, L, G, Kg]", item.tamanho):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tamanho desconhecido (ml/L/G/Kg)!")

        if not itemObject2.tipo in ('Barrigudinhas', 'Comida', 'Refrigerante Descartável', 'Refrigerante Retornável', 
                             'Refrigerante Lata', 'Doses', 'Vinhos', 'Energéticos De Lata', 'Energéticos 2L', 
                             'Cigarros', 'Palheiros', 'Sedas', 'Carvão', 'Gelo', 'Fabitos', 'Batata', 'Torcida', 'Doces'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de produto não disponível")
        
        if item.valor_compra <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valor de compra do produto não pode ser menor ou igual a 0")
        
        if item.valor_venda <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valor de venda do produto não pode ser menor ou igual a 0")
        
        if item.quantidade <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantidade de produto não pode ser menor ou igual a 0")
        
        validar_data(itemObject2.data_validade)
        
        session.commit()
        if item.quantidade <= 10:
            return "Atualizando o produto de id:{}, {}. Para: ".format(id, user.username), itemObject2, "Atenção {} o produto {} chegou na quantidade mínima 10! Agora está em {}, fica esperto!".format(user.username, id, item.quantidade)  
        else:
            return "Atualizando o produto de id:{}, {}. Para: ".format(id, user.username), itemObject2      
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
async def deleteItemService(nome:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try: 
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para deletar produtos!"
            )
    
        #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
        itemObject = session.query(modelsP.Produtos_Cad).filter_by(nome=nome.capitalize()).first() #Pegando o valor que foi passado pelo nome, e procurando no bnaco pra ver se existe algo com esse nome
        if not itemObject:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Produto {nome}, não encontrado")
        id = itemObject.idProduto
        session.delete(itemObject) #comitando a mudança
        session.commit() #Comitando as mudanças
        session.close() #Fechando o banco
        return f"Olá {user.username}, o item {nome} e id {id}, foi deletado! Produto:", itemObject
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
async def deleteItemByIdService(id: int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem autorização para deletar produtos!")
    
        item = session.query(modelsP.Produtos_Cad).get(id)
        if not item:
            # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Produto de id:{id}, não encontrado")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto de id:{}, não encontrado".format(id))
        produto = item.nome
        session.delete(item)
        session.commit()
        session.close()
        return "Olá {}, o item de id:{} e nome:{}, foi deletado! Produto:".format(user.username, id, produto), item
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))
    