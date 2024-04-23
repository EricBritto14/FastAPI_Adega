import models, schemas
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter #APIRouter para fazer as rotas
from endpoints.loginn import *
import re
from datetime import datetime, date

router = APIRouter() #Criando o router para por no lugar do @app.get, vai virar router.get

def get_session(): #Função para pegar a sessão, e abrir e fechar o banco de dados
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
def getItems(session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Pegando os valores do banco de dados, Depends do get_session. E verificando se o usuário está logado, com o get_current_user
    try:
        items = session.query(models.Produtos).all()
        #print(datetime.now)
        return f"Pegando todos os itens para você, {user.username}", items
    except Exception as e:
        print("Erro", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro no serivdor")


#Aqui a gente chama a classe responsável pelos valores que vão ser necessitados aqui, e chamamos eles para passarem os valores e serem encaminhados para o banco de dados
@router.get("/produtos/{nome}") #Router para trazer as informações de acordo com o id
def getItem(nome:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Criando um getItem, (get). que espera receber uma variável (id) e com os dois pontos :int eu EXIJO que a variável que venha seja INT
    try:
        item = session.query(models.Produtos).filter_by(nome=nome.capitalize()).first() 
        #return fakeDataBase[id] #Retornando o valor do dicionário, de acordo com o ID que ele digitar
        return f"Pegando o produto de nome:{nome} para você, {user.username}", item
    except Exception as e:
        print("Erro: ", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro no servidor")

@router.post("/produtos/adicionar")
def addItem(item:schemas.Produtos, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para adicionar produtos!"
        )
    try:
        #capitalize é para colocar a primeira letra maiscula e o resto minuscula
        item = models.Produtos(nome = item.nome.capitalize(), tipo = item.tipo.capitalize(), valor = item.valor, quantidade = item.quantidade, tamanho = item.tamanho.lower(), data_validade = item.data_validade, data_cadastro = data_formatada)

        if not item.tipo in ('Doces', 'Alcoólicas', 'Não alcoólicas'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de produto não disponível")
        
        validar_data(item.data_validade)
            #  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data de validade menor do que o dia de hoje!")
        
        if not re.search("[0-9][ml, l]", item.tamanho):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tamanho desconhecido (ml/l)")
        
        session.add(item) #Adicionando no banco
        session.commit()  #comitando a mudança
        session.refresh(item) #Dando um refresh para atualizar o banco
        return f"Olá, {user.username}, o produto desejado foi adicionado!", item
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto já adicionado!")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

#Atualizando valores
#@router.put("/produtos/atualizar/{id}")
#itemObject = session.query(models.Produtos).get(id) #Mudanças para pegar pelo id não pelo nome
@router.put("/produtos/atualizar/{nome}") #Tentar pegar pelo nome, não pelo id
def updateItem(nome:str, item:schemas.AttProdutos, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    try:
        #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
        # item = session.query(models.Produtos).filter_by(nome=nome.capitalize()).first() 
        itemObject = session.query(models.Produtos).filter_by(nome=nome.capitalize()).first() #Pegando o valor que foi passado pelo int, de qual objeto salvo é
        itemObject.tipo, itemObject.valor, itemObject.quantidade, itemObject.data_validade, itemObject.data_cadastro = item.tipo.capitalize(), item.valor, item.quantidade, item.data_validade, data_formatada #atualizando com esses valores novos 

        if not itemObject.tipo in ('Doces', 'Alcoólicas', 'Não alcoólicas'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de produto não disponível")
        
        
        validar_data(itemObject.data_validade)
        
        # if not re.search("[0-9][ml][l]", itemObject.tamanho):
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Tamanho desconhecido (ml/l)")

        session.commit() #comitando a mudança
        #fakeDataBase[newId] = {"task":item.task, "valor":item.value} #Indicando que no fakedatabase no novo id, seja adicionado task + o valor que for passado
        #return fakeDataBase
        if item.quantidade <= 10:
            return f"Atualizando o produto de nome:{nome}, {user.username}. Para: ", itemObject, f"Atenção {user.username} o produto {itemObject.nome} chegou na quantidade mínima 10! Agora está em {item.quantidade}, fica esperto!"
        else:
            return f"Atualizando o produto de nome:{nome}, {user.username}. Para: ", itemObject
        
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto já adicionado!")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

#Deletando valores
@router.delete("/produtos/delete/{nome}")
def deleteItem(nome:str, session: Session = Depends(get_session), user: Cadastro_Users = Depends(get_current_user)): #Aqui se chamaria a classe, e o nome do classe dentro da classe, para pegar os valores e fazer um objeto
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para deletar produtos!"
        )
    try:
        #newId = len(fakeDataBase.keys()) + 1 #Pegando o tamanho do fakedatabase e adicionando o valor de +1 para que o próximo item que for adicionado seja na próxima key
        itemObject = session.query(models.Produtos).filter_by(nome=nome.capitalize()).first() #Pegando o valor que foi passado pelo nome, e procurando no bnaco pra ver se existe algo com esse nome
        id = itemObject.idProduto
        session.delete(itemObject) #comitando a mudança
        session.commit() #Comitando as mudanças
        session.close() #Fechando o banco
        return f"Olá {user.username}, o item {nome} e id {id}, foi deletado! Produto:", itemObject
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Produto {nome}, não encontrado")
