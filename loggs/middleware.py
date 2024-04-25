from fastapi import Request
from .logger import logger
#import time

#@app.middleware("http") #Middleware serve para fazer realmente esse log, e serve essencialmente para rodar em todos os requests que forem feitos
async def log_middleware(request: Request, call_next): #Criando os "props" padrão para o log_middleware
    #start = time.time() #Se quiser saber o tempo que começou o processo para depois lá embaixo calcular o tempo que acabou na hora de retornar pro usuário, pra mostrar pra ele quanto q demorou (mas achei sem necessidade)
     #Aqui está armazenando a actual response para o cliente, se deu bom, se deu ruim... se deu bom vai retornar o log, ou um ok
    body = await request.body()
    #process_time = time.time() - start #Process_time seria o calculo do start lá em cima, com o agora, pra calcular quanto demorou o processo... mas achei sem necessidade
    if body.decode() == "":
        default = "Pegando os produtos, ou deletando algo"
    else:
        default = body.decode()

    log_dict = { #Criando dicionario que retornará os valores do log
        "url": request.url.path,
        "metodo usado": request.method, 
        "o que foi foi feito": default,
        #"process_time": process_time #Se quiser adicionar algo é desse jeito, e se quiser adicionar o precess time seria assim.
    }

    #Pega a resposta do servidor, se deu ruim ou bom, e retorna
    response = await call_next(request)
    #Resposta do servidor, se deu certo ou errado a requisição
    if response.status_code == 400: 
        dict = {"status": "Erro 400 (Nao funcionou a aquisicao)"}
    elif response.status_code == 404:
        dict = {"status": "Erro 400 (Nao encontrado)"}
    elif response.status_code == 422:
        dict = {"status": "Erro 422 (Erro ao tentar cadastrar e passou tudo errado)"}
    elif response.status_code == 200:
        dict = {"status": "Codigo 200 (Funcionou a aquisicao)"}
    elif response.status_code == 500:
        dict = {"status": "Codigo 500 (Erro no servidor)"}
    elif response.status_code == 401:
        dict = {"status": "Codigo 401 (Erro na autenticacao)"}
    elif response.status_code == 203:
        dict = {"status": "Codigo 203 (Nao autorizado para tal requisicao)"}
    else:
        dict = {"status": "Erro nao cadastrado, mas deu erro"}
    
    log_dict.update(dict)
    logger.info(log_dict, extra=log_dict) #dando um "return" com o valor do log_dict, o logger info já tras as informações padrão que colocamos no logger.py
    
    return response #Retornando a resposta para o cliente
