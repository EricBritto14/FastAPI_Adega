import models, schemas
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter #APIRouter para fazer as rotas
from endpoints.loginn import *
import re
from datetime import datetime, date

router = APIRouter() #Criando o router para por no lugar do @app.get, vai virar router.get

async def get_session(): #Função para pegar a sessão, e abrir e fechar o banco de dados
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

data_hoje = date.today()
data_formatada = data_hoje.strftime('%d/%m/%Y')

#Validando se está vindo em formato de data, e se a data de vencimendo do produto é menor que a data de hoje ou não
def validar_data(data_val):
    try:
        data_hoje = date.today()
        data_valF1 = datetime.strptime(data_val, '%d/%m/%Y').date()
            #data_valF = data_valF1.strftime('%d/%m/%Y')
        if not data_valF1 < data_hoje:
            return data_valF1.strftime('%d/%m/%Y')
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data de validade menor que a data de hoje!")        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data de validade em formato errado! (**/**/****) OU data de validação menor que a data de hoje!")

#Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
@router.get("/produtos")
async def getItems(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session. E verificando se o usuário está logado, com o get_current_user
    try:
        items = session.query(models.Produtos).all()
        if items is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum produto existente!")
        else:
            return f"Pegando todos os itens para você, {user.username}", items
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))


#Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
@router.get("/produtos/produto_name/{nome}") #Router para trazer as informações de acordo com o id
async def getItem(nome:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    try:
        item = session.query(models.Produtos).filter_by(nome=nome.capitalize()).first()
        if item is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto de nome:{}, não encontrado".format(nome))
        #return fakeDataBase[id] #Retornando o valor do dicionário, de acordo com o ID que ele digitar
        return f"Pegando o produto de nome:{nome} para você, {user.username}", item
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.get("/produtos/produto_id/{id}")
async def getItemId(id:int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        itemId = session.query(models.Produtos).get(id)
        if itemId is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto inexistente!")
        else:
            return f"Pegando o produto de id:{id} para você, {user.username}", itemId   
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))
        

@router.post("/produtos/adicionar")
async def addItem(item:schemas.Produtos, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para adicionar produtos!")
        #capitalize é para colocar a primeira letra maiscula e o resto minuscula
        item = models.Produtos(nome = item.nome.capitalize(), tipo = item.tipo.capitalize(), valor = item.valor, quantidade = item.quantidade, tamanho = item.tamanho.lower(), data_validade = item.data_validade, data_cadastro = data_formatada)

        produto = session.query(models.Produtos).filter_by(nome = item.nome).first()
        if produto != None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto já adicionado!")
        
        if not item.tipo in ('Comida', 'Alcoólicas', 'Não alcoólicas', 'Tabacaria'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de produto não disponível")
        
        validar_data(item.data_validade)
        
        if item.valor <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valor do produto não pode ser 0 ou menor que 0!")

        if item.quantidade <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantidade do produto não pode ser igual ou menor que 0!")
            
        if not re.search("[0-9][ml, L, G, Kg]", item.tamanho):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tamanho desconhecido (ml/L/G/Kg)!")
        
        session.add(item) #Adicionando no banco
        session.commit()  #comitando a mudança
        session.refresh(item) #Dando um refresh para atualizar o banco
        return f"Olá, {user.username}, o produto desejado foi adicionado!", item
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))

#Atualizando valores
#@router.put("/produtos/atualizar/{id}")
#itemObject = session.query(models.Produtos).get(id) #Mudanças para pegar pelo id não pelo nome
@router.put("/produtos/atualizar_by_name/{nome}") #Tentar pegar pelo nome, não pelo id
async def updateItem(nome:str, item:schemas.AttProdutos, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try:
        #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
        # item = session.query(models.Produtos).filter_by(nome=nome.capitalize()).first() 
        itemObject = session.query(models.Produtos).filter_by(nome=nome.capitalize()).first() #Pegando o valor que foi passado pelo int, de qual objeto salvo é
        
        if itemObject is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto não encontrado")
        
        itemObject.tipo, itemObject.valor, itemObject.quantidade, itemObject.data_validade, itemObject.data_cadastro = item.tipo.capitalize(), item.valor, item.quantidade, item.data_validade, data_formatada #atualizando com esses valores novos 
        
        if not itemObject.tipo in ('Doces', 'Alcoólicas', 'Não alcoólicas'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de produto não disponível")
        
        if item.valor <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valor do produto não pode ser 0 ou igual a 0!")
        
        if item.quantidade <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantidade de produto não pode ser igual ou menor que 0!")
        
        validar_data(itemObject.data_validade)
        
        # if not re.search("[0-9][ml][l]", itemObject.tamanho):
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Tamanho desconhecido (ml/l)")

        session.commit() #comitando a mudança
        if item.quantidade <= 10:
            return f"Atualizando o produto de nome:{nome}, {user.username}. Para: ", itemObject, f"Atenção {user.username} o produto {itemObject.nome} chegou na quantidade mínima 10! Agora está em {item.quantidade}, fica esperto!"
        else:
            return f"Atualizando o produto de nome:{nome}, {user.username}. Para: ", itemObject
        
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.put("/produtos/atualizar_by_id/{id}")
async def atualizarItemId(id: int, item:schemas.AttProdutos, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        itemObject2 = session.query(models.Produtos).get(id)
        if itemObject2 is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Produto de id:{id} inexistente!")
        
        itemObject2.tipo, itemObject2.valor, itemObject2.quantidade, itemObject2.data_validade, itemObject2.data_cadastro = item.tipo.capitalize(), item.valor, item.quantidade, item.data_validade, data_formatada
        
        if not itemObject2.tipo in ('Doces', 'Alcoólicas', 'Não alcoólicas'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de produto não disponível")
        
        if item.valor <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valor do produto não pode ser 0 ou igual a 0")
        
        if item.quantidade <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantidade de produto não pode ser 0 ou igual a 0")
        
        validar_data(itemObject2.data_validade)
        
        session.commit()
        if item.quantidade <= 10:
            return "Atualizando o produto de id:{}, {}. Para: ".format(id, user.username), itemObject2, "Atenção {} o produto {} chegou na quantidade mínima 10! Agora está em {}, fica esperto!".format(user.username, id, item.quantidade)  
        else:
            return "Atualizando o produto de id:{}, {}. Para: ".format(id, user.username), itemObject2      
        
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

#Deletando valores
@router.delete("/produtos/delete_by_name/{nome}")
async def deleteItem(nome:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try: 
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para deletar produtos!"
            )
    
        #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
        itemObject = session.query(models.Produtos).filter_by(nome=nome.capitalize()).first() #Pegando o valor que foi passado pelo nome, e procurando no bnaco pra ver se existe algo com esse nome
        if itemObject is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Produto {nome}, não encontrado")
        id = itemObject.idProduto
        session.delete(itemObject) #comitando a mudança
        session.commit() #Comitando as mudanças
        session.close() #Fechando o banco
        return f"Olá {user.username}, o item {nome} e id {id}, foi deletado! Produto:", itemObject
    except Exception as e:
        session.rollback() #Session rollback serve para que se cair na exception, garantir que não faça nada no banco. Então rollback para garantir que não deu nada, antes de dar erro.
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.delete("/produtos/delete_by_id/{id}")
async def deleteItemById(id: int, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem autorização para deletar produtos!")
    
        item = session.query(models.Produtos).get(id)
        if item is None:
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
    