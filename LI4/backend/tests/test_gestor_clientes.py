"""Testes unitários do GestorClientes."""
import pytest
from unittest.mock import MagicMock

from Model.ClientSubsystem.GestorClientes import GestorClientes
from Model.ClientSubsystem.Cliente import Cliente
from Model.ClientSubsystem.Trotinete import Trotinete


def _gestor(cliente_dao=None, trotinete_dao=None):
    return GestorClientes(
        cliente_dao=cliente_dao or MagicMock(),
        trotinete_dao=trotinete_dao or MagicMock(),
    )


def _cliente_mock(id=1, nif="123456789"):
    c = MagicMock(spec=Cliente)
    c.get_id.return_value = id
    c.get_nif.return_value = nif
    return c


# ─────────────────────────────────────────────────────────────────────────────
# CRIAR CLIENTE
# ─────────────────────────────────────────────────────────────────────────────

class TestCriarCliente:
    def test_criar_cliente_valido_chama_dao(self, mock_cliente_dao, mock_trotinete_dao):
        mock_cliente_dao.criarCliente.return_value = 1

        gestor = _gestor(cliente_dao=mock_cliente_dao, trotinete_dao=mock_trotinete_dao)
        resultado = gestor.criar_cliente(
            nome="Sofia Rodrigues",
            nif="681807024",
            contacto="934567890",
            email="sofia@email.pt",
            morada="Praça do Comércio, 78",
        )

        assert resultado == 1
        mock_cliente_dao.criarCliente.assert_called_once()

    def test_criar_cliente_com_nif_invalido_lanca_value_error(self, mock_cliente_dao, mock_trotinete_dao):
        gestor = _gestor(cliente_dao=mock_cliente_dao, trotinete_dao=mock_trotinete_dao)
        with pytest.raises(ValueError):
            gestor.criar_cliente(
                nome="Teste",
                nif="000000000",  # NIF inválido
                contacto="912345678",
                email="teste@email.pt",
                morada="Rua X",
            )

        mock_cliente_dao.criarCliente.assert_not_called()

    def test_criar_cliente_com_email_invalido_lanca_value_error(self, mock_cliente_dao, mock_trotinete_dao):
        gestor = _gestor(cliente_dao=mock_cliente_dao, trotinete_dao=mock_trotinete_dao)
        with pytest.raises(ValueError):
            gestor.criar_cliente(
                nome="Teste",
                nif="681807024",
                contacto="912345678",
                email="invalido",
                morada="Rua X",
            )

        mock_cliente_dao.criarCliente.assert_not_called()


# ─────────────────────────────────────────────────────────────────────────────
# EDITAR CLIENTE
# ─────────────────────────────────────────────────────────────────────────────

class TestEditarCliente:
    def test_editar_cliente_existente_retorna_true(self, mock_cliente_dao, mock_trotinete_dao):
        mock_cliente_dao.consultarCliente.return_value = _cliente_mock()
        mock_cliente_dao.editarCliente.return_value = True

        gestor = _gestor(cliente_dao=mock_cliente_dao, trotinete_dao=mock_trotinete_dao)
        resultado = gestor.editar_cliente(
            id=1,
            nome="Sofia Atualizada",
            nif="681807024",
            contacto="934567890",
            email="sofia@email.pt",
            morada="Nova Morada",
        )

        assert resultado is True
        mock_cliente_dao.editarCliente.assert_called_once()

    def test_editar_cliente_nao_existente_retorna_zero(self, mock_cliente_dao, mock_trotinete_dao):
        mock_cliente_dao.consultarCliente.return_value = None

        gestor = _gestor(cliente_dao=mock_cliente_dao, trotinete_dao=mock_trotinete_dao)
        resultado = gestor.editar_cliente(
            id=999,
            nome="X", nif="681807024", contacto="912345678",
            email="x@x.pt", morada="X",
        )

        assert resultado == 0
        mock_cliente_dao.editarCliente.assert_not_called()


# ─────────────────────────────────────────────────────────────────────────────
# REMOVER CLIENTE (cascade)
# ─────────────────────────────────────────────────────────────────────────────

class TestRemoverCliente:
    def _setup_db_mock(self, mock_cliente_dao):
        """Configura o mock da conexão usada internamente pelo remover_cliente."""
        mock_cursor = MagicMock()
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cliente_dao.db = mock_conn
        mock_cliente_dao.tem_historico.return_value = False
        return mock_conn, mock_cursor

    def test_remover_cliente_existente_cascata_para_trotinetes(self, mock_cliente_dao, mock_trotinete_dao):
        cliente = _cliente_mock(id=5, nif="681807024")
        mock_cliente_dao.consultarCliente.return_value = cliente
        mock_cliente_dao._exec_remover.return_value = True
        self._setup_db_mock(mock_cliente_dao)

        gestor = _gestor(cliente_dao=mock_cliente_dao, trotinete_dao=mock_trotinete_dao)
        resultado = gestor.remover_cliente(5)

        assert resultado is True
        mock_trotinete_dao._exec_remover_por_cliente.assert_called_once()
        mock_cliente_dao._exec_remover.assert_called_once()

    def test_remover_trotinetes_chamado_antes_de_remover_cliente(self, mock_cliente_dao, mock_trotinete_dao):
        """Verifica a ordem das operações (cascade correcta)."""
        cliente = _cliente_mock(id=5)
        mock_cliente_dao.consultarCliente.return_value = cliente
        chamadas = []
        mock_trotinete_dao._exec_remover_por_cliente.side_effect = lambda *_: chamadas.append("trotinetes")
        mock_cliente_dao._exec_remover.side_effect = lambda *_: chamadas.append("cliente") or True
        self._setup_db_mock(mock_cliente_dao)

        gestor = _gestor(cliente_dao=mock_cliente_dao, trotinete_dao=mock_trotinete_dao)
        gestor.remover_cliente(5)

        assert chamadas == ["trotinetes", "cliente"]

    def test_remover_cliente_nao_existente_retorna_false(self, mock_cliente_dao, mock_trotinete_dao):
        mock_cliente_dao.consultarCliente.return_value = None

        gestor = _gestor(cliente_dao=mock_cliente_dao, trotinete_dao=mock_trotinete_dao)
        resultado = gestor.remover_cliente(999)

        assert resultado is False
        mock_trotinete_dao._exec_remover_por_cliente.assert_not_called()


# ─────────────────────────────────────────────────────────────────────────────
# REGISTAR TROTINETE
# ─────────────────────────────────────────────────────────────────────────────

class TestRegistarTrotinete:
    def test_registar_trotinete_com_cliente_valido(self, mock_cliente_dao, mock_trotinete_dao):
        c = _cliente_mock(id=1)
        mock_cliente_dao.listarClientes.return_value = [c]
        mock_trotinete_dao.criarTrotinete.return_value = True

        gestor = _gestor(cliente_dao=mock_cliente_dao, trotinete_dao=mock_trotinete_dao)
        resultado = gestor.registar_trotinete(
            marca="Xiaomi", modelo="Pro 2",
            numero_serie="XM001", id_cliente=1,
        )

        assert resultado is True
        mock_trotinete_dao.criarTrotinete.assert_called_once()

    def test_registar_trotinete_com_cliente_invalido_retorna_false(self, mock_cliente_dao, mock_trotinete_dao):
        mock_cliente_dao.listarClientes.return_value = []

        gestor = _gestor(cliente_dao=mock_cliente_dao, trotinete_dao=mock_trotinete_dao)
        resultado = gestor.registar_trotinete(
            marca="Xiaomi", modelo="Pro 2",
            numero_serie="XM001", id_cliente=999,
        )

        assert resultado is False
        mock_trotinete_dao.criarTrotinete.assert_not_called()
