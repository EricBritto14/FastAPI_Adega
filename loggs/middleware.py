from fastapi import Request, Response
from .logger import logger
#import time

#Ver o log, pq sempre da 200 e não é sempre.

#@app.middleware("http") #Middleware serve para fazer realmente esse log, e serve essencialmente para rodar em todos os requests que forem feitos
async def log_middleware(request: Request, call_next, httpteste: Response = None): #Criando os "props" padrão para o log_middleware
    #start = time.time() #Se quiser saber o tempo que começou o processo para depois lá embaixo calcular o tempo que acabou na hora de retornar pro usuário, pra mostrar pra ele quanto q demorou (mas achei sem necessidade)
     #Aqui está armazenando a actual response para o cliente, se deu bom, se deu ruim... se deu bom vai retornar o log, ou um ok
    body = await request.body()
    #process_time = time.time() - start #Process_time seria o calculo do start lá em cima, com o agora, pra calcular quanto demorou o processo... mas achei sem necessidade
    # if request.method == "POST":
    #     print("Request Body:")
    #     print(body.decode())
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

    #Resposta do servidor, se deu certo ou errado a requisição
    if httpteste is None: #Como eu coloquei o response pra ser sempre None ali em cima, ele sempre virá None. Lá em cima eu precisei passar None, se não na main ia pedir pra passar um parametro
        httpteste = Response() #Então, preciso passar outro valor para o httpteste, e abrir o response dnv
        if httpteste.status_code == 400: 
                    dict = {"status": "Erro 400 (Nao funcionou a aquisicao)"}
        elif httpteste.status_code == 404:
                    dict = {"status": "Erro 400 (Nao encontrado)"}
        elif httpteste.status_code == 422:
                    dict = {"status": "Erro 422 (Erro ao tentar cadastrar e passou tudo errado)"}
        elif httpteste.status_code == 200:
                    dict = {"status": "Codigo 200 (Funcionou a aquisicao)"}
        else:
                    dict = {"status": "Erro nao cadastrado, mas deu erro"}
    
    log_dict.update(dict)
    
    response = await call_next(request)
    logger.info(log_dict, extra=log_dict) #dando um "return" com o valor do log_dict, o logger info já tras as informações padrão que colocamos no logger.py
    
    return response #Retornando a resposta para o cliente
