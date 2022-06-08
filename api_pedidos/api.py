from http import HTTPStatus
from urllib.request import Request
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from uuid import UUID
from api_pedidos.esquema import Item
from api_pedidos.excecao import PedidoNaoEncontradoError
from typing import List
app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    return {"status":"ok"}

def recuperar_itens_por_pedido(identificacao_do_pedido: UUID) -> List[Item]:
    pass

@app.get("/orders/{identificacao_do_pedido}/items")
def listar_itens(itens: List[Item] = Depends(recuperar_itens_por_pedido)):
    return itens

@app.exception_handler(PedidoNaoEncontradoError)
def tratar_erro_pedido_nao_encontrado(request: Request, exc: PedidoNaoEncontradoError):
    return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message":"Pedido não encontrado"})

