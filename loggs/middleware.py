from fastapi import Request
from fastapi.responses import JSONResponse
from .logger import logger
#import time

#@app.middleware("http") #Middleware serve para fazer realmente esse log, e serve essencialmente para rodar em todos os requests que forem feitos
async def log_middleware(request: Request, call_next): #Criando os "props" padrão para o log_middleware
    #start = time.time() #Se quiser saber o tempo que começou o processo para depois lá embaixo calcular o tempo que acabou na hora de retornar pro usuário, pra mostrar pra ele quanto q demorou (mas achei sem necessidade)
     #Aqui está armazenando a actual response para o cliente, se deu bom, se deu ruim... se deu bom vai retornar o log, ou um ok
    try:
        binary_types = [
            "multipart/form-data",
            "application/octet-stream",
            "image/",
            "audio/",
            "video/"
        ]

        content_type = request.headers.get("content-type", "").lower()

        if any(content_type.startswith(bt) for bt in binary_types):
            default = f"<Conteúdo binário - tipo {content_type}>"
        else:
            try:
                    body = await request.body()
                    default = body.decode() if body else "Pegando os produtos, ou deletando algo"
            except Exception:
                    default = "<Erro ao tentar decodificar corpo>"

        try:
                response = await call_next(request)
        except Exception as e:
                 logger.error(f"Erro ao processar a requisição: {repr(e)}")
                 response = JSONResponse(
                      content={"detail" : "Erro interno no servidor"},
                      status_code = 500
                 )

        status_map = {
                    200: "Código 200 (Funcionou a requisicao)",
                    400: "Código 400 (Nao funcionou a aquisicao)",
                    401: "Código 401 (Erro na autenticacao)",
                    203: "Codigo 203 (Nao autorizado para tal requisicao)",
                    404: "Código 404 (Nao encontrado)",
                    422: "Código 422 (Erro ao tentar cadastrar e passou tudo errado)",
                    500: "Codigo 500 (Erro no servidor)"
        }

        log_dict = {
                    "url": request.url.path,
                    "método usado": request.method,
                    "o que foi feito": default,
                    "status" : status_map.get(response.status_code, "Erro nao cadastrado, mas deu erro")
        }

        logger.info(log_dict, extra=log_dict)   
        return response
        
    except Exception as e:
        logger.error(f"Erro no log_middleware: {repr(e)}")
        return JSONResponse(
              content={"detail" : "Erro interno no log_middleware"},
              status_code=500
        )
