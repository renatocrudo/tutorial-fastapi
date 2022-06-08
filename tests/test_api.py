from uuid import UUID
from fastapi.testclient import TestClient
from http import HTTPStatus
from api_pedidos.api import app, recuperar_itens_por_pedido
import pytest
from api_pedidos.esquema import Item
from api_pedidos.excecao import PedidoNaoEncontradoError
from typing import List

#criando uma fixture (ambiente usado para testar consistentemente algum item)
@pytest.fixture
def cliente():
    return TestClient(app)

class TestHealthCheck:
    def test_quando_verificar_integridade_devo_ter_como_retorno_codigo_de_status_200(self, cliente):
        resposta = cliente.get("/healthcheck")
        assert resposta.status_code == HTTPStatus.OK
    
    def test_quando_verificar_integridade_formato_de_retorno_deve_ser_json(self, cliente):
        resposta = cliente.get("/healthcheck")
        assert resposta.headers["Content-Type"] == "application/json"

    def test_quando_verificar_integridade_deve_conter_informacoes(self, cliente):
        resposta = cliente.get("/healthcheck")
        assert resposta.json() == {
        "status":"ok",
        }


class TestListarPedidos:
    def test_obter_itens_quando_receber_identificacao_do_pedido_invalido_um_erro_deve_ser_retornado(self, cliente):
        resposta = cliente.get("/orders/valor-invalido/items")
        assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    
    def test_obter_itens_quando_identificacao_do_pedido_nao_encontrado_um_erro_deve_ser_retornado(self, cliente):
        def duble(identificacao_do_pedido: UUID) -> List[Item]:
            raise PedidoNaoEncontradoError()
        app.dependency_overrides[recuperar_itens_por_pedido] = duble
        resposta = cliente.get("/orders/7e290683-d67b-4f96-a940-44bef1f69d21/items")
        assert resposta.status_code == HTTPStatus.NOT_FOUND

    def test_obter_itens_quando_encontrar_pedido_codigo_ok_deve_ser_retornado(self, cliente):
        def duble(identificacao_do_pedido: UUID) -> List[Item]:
            return []
        app.dependency_overrides[recuperar_itens_por_pedido] = duble
        resposta = cliente.get("/orders/7e290683-d67b-4f96-a940-44bef1f69d21/items")
        assert resposta.status_code == HTTPStatus.OK

    def test_obter_itens_quando_encontrar_pedido_deve_retornar_itens(self, cliente):
        itens = [
            Item(sku='1', description='Item 1', image_url='http://url.com/img1', reference='ref1', quantity=1),
            Item(sku='2', description='Item 2', image_url='http://url.com/img2', reference='ref2', quantity=2),
        ]
        def duble(identificacao_do_pedido: UUID) -> List[Item]:
            return itens
        app.dependency_overrides[recuperar_itens_por_pedido] = duble
        resposta = cliente.get("/orders/7e290683-d67b-4f96-a940-44bef1f69d21/items")
        assert resposta.json() == itens









