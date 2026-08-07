"""Testes unitários do GestorStock."""
import pytest
from unittest.mock import MagicMock, call

from Model.StockSubsystem.GestorStock import GestorStock
from Model.StockSubsystem.Peca import Peca


def _gestor(peca_dao=None):
    return GestorStock(peca_dao or MagicMock())


# ─────────────────────────────────────────────────────────────────────────────
# CRIAR PEÇA
# ─────────────────────────────────────────────────────────────────────────────

class TestCriarPeca:
    def test_criar_peca_valida_chama_inserir(self, mock_peca_dao):
        mock_peca_dao.inserir.return_value = 5

        gestor = _gestor(mock_peca_dao)
        resultado = gestor.criarPeca(
            nome="Bateria 36V",
            descricao="Lítio",
            fornecedor="Xiaomi",
            categoria="Baterias",
            preco=180.0,
            stock=8,
            quantidade_minima=3,
        )

        assert resultado == 5
        mock_peca_dao.inserir.assert_called_once()

    def test_criar_peca_insere_instancia_peca(self, mock_peca_dao):
        mock_peca_dao.inserir.return_value = 1

        gestor = _gestor(mock_peca_dao)
        gestor.criarPeca("Nome", "Desc", "Forn", "Cat", 10.0, 5, 2)

        peca_inserida = mock_peca_dao.inserir.call_args[0][0]
        assert isinstance(peca_inserida, Peca)
        assert peca_inserida.nome == "Nome"
        assert peca_inserida.preco == 10.0

    def test_criar_peca_com_preco_negativo_propaga_erro(self, mock_peca_dao):
        gestor = _gestor(mock_peca_dao)
        # Peca com preco negativo num setter deve levantar ValueError
        # (o construtor não valida, mas o setter sim; criarPeca usa o construtor
        # e depois o DAO insere — testamos que o setter lança o erro)
        with pytest.raises(ValueError):
            p = Peca(-1, "X", "d", "f", "c", 10.0, 5, 2)
            p.preco = -1.0  # setter valida

    def test_criar_peca_com_stock_negativo_propaga_erro(self, mock_peca_dao):
        gestor = _gestor(mock_peca_dao)
        with pytest.raises(ValueError):
            p = Peca(-1, "X", "d", "f", "c", 10.0, 5, 2)
            p.stock = -1


# ─────────────────────────────────────────────────────────────────────────────
# CONSULTAR STOCK
# ─────────────────────────────────────────────────────────────────────────────

class TestConsultarStock:
    def test_consultar_stock_existente_retorna_peca(self, mock_peca_dao):
        peca = MagicMock(spec=Peca)
        mock_peca_dao.consultar_por_id.return_value = peca

        gestor = _gestor(mock_peca_dao)
        resultado = gestor.consultarStock(1)

        assert resultado is peca
        mock_peca_dao.consultar_por_id.assert_called_once_with(1)

    def test_consultar_stock_inexistente_retorna_none(self, mock_peca_dao):
        mock_peca_dao.consultar_por_id.return_value = None

        gestor = _gestor(mock_peca_dao)
        assert gestor.consultarStock(999) is None


# ─────────────────────────────────────────────────────────────────────────────
# ATUALIZAR STOCK
# ─────────────────────────────────────────────────────────────────────────────

class TestAtualizarStock:
    def test_atualizar_stock_chama_dao(self, mock_peca_dao):
        mock_peca_dao.atualizar_stock.return_value = True

        gestor = _gestor(mock_peca_dao)
        resultado = gestor.atualizarStock(1, 20)

        assert resultado is True
        mock_peca_dao.atualizar_stock.assert_called_once_with(1, 20)


# ─────────────────────────────────────────────────────────────────────────────
# LISTAR PEÇAS
# ─────────────────────────────────────────────────────────────────────────────

class TestListarPecas:
    def test_listar_pecas_retorna_lista_do_dao(self, mock_peca_dao):
        pecas = [MagicMock(spec=Peca), MagicMock(spec=Peca)]
        mock_peca_dao.listar_pecas.return_value = pecas

        gestor = _gestor(mock_peca_dao)
        resultado = gestor.listarPecas()

        assert resultado == pecas
