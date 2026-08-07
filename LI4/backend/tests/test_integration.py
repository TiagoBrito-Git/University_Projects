"""
Integration tests — require a running MySQL instance at localhost:3306.

Run with:
    pytest tests/test_integration.py -v -m integration

These tests use the real 'scooterfix' database and always clean up after
themselves via finally blocks.  They intentionally bypass mocks so that
SQL correctness, constraints, and transaction behaviour are exercised
against a real engine.
"""
import os
import uuid
import pytest
import mysql.connector

from Model.StockSubsystem.PecaDAO import PecaDAO
from Model.StockSubsystem.Peca import Peca
from Model.ClientSubsystem.Cliente import Cliente
from Model.ClientSubsystem.ClienteDAO import ClienteDAO
from Model.ClientSubsystem.TrotineteDAO import TrotineteDAO
from Model.ClientSubsystem.GestorClientes import GestorClientes
from Model.PaymentsSubsystem.FaturaDAO import FaturaDAO

pytestmark = pytest.mark.integration

_DB_CONFIG = dict(
    host="localhost", port=int(os.getenv("DB_PORT", "3307")),
    database="scooterfix", user="api_user", password="api123",
)


def _uid() -> str:
    """Short unique suffix used to avoid collisions between test runs."""
    return uuid.uuid4().hex[:8].upper()


def _valid_nif() -> str:
    """Generate a pseudo-random Portuguese NIF that passes the checksum."""
    base_int = uuid.uuid4().int % 90_000_000 + 10_000_000  # 8 digits
    digits = list(str(base_int))
    # First digit must be one of 1,2,3,5,6,7,8,9
    if digits[0] not in "12356789":
        digits[0] = "5"
    base = "".join(digits)
    total = sum(int(base[i]) * (9 - i) for i in range(8))
    check = 11 - (total % 11)
    if check >= 10:
        check = 0
    return base + str(check)


@pytest.fixture(scope="module")
def db():
    conn = mysql.connector.connect(**_DB_CONFIG)
    yield conn
    conn.close()


def _cleanup(db, table: str, field: str, value) -> None:
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE {field} = %s", (value,))
    db.commit()
    cursor.close()


# ── PecaDAO ───────────────────────────────────────────────────────────────────

class TestPecaDAOIntegracao:
    """Verifica SQL real, locks e lógica de retry do PecaDAO."""

    def _insert_peca(self, db, stock: int = 20) -> tuple[int, Peca]:
        dao = PecaDAO(db)
        p = Peca(-1, f"TestPeca-{_uid()}", "desc", "forn", "cat", 9.99, stock, 2)
        pid = dao.inserir(p)
        return pid, p

    def test_inserir_e_consultar_round_trip(self, db):
        pid, p = self._insert_peca(db)
        try:
            resultado = PecaDAO(db).consultar_por_id(pid)
            assert resultado is not None
            assert resultado.nome == p.nome
            assert resultado.stock == p.stock
            assert float(resultado.preco) == pytest.approx(p.preco)
        finally:
            _cleanup(db, "pecas", "id", pid)

    def test_listar_inclui_peca_inserida(self, db):
        pid, p = self._insert_peca(db)
        try:
            lista = PecaDAO(db).listar_pecas()
            ids = [x.id for x in lista]
            assert pid in ids
        finally:
            _cleanup(db, "pecas", "id", pid)

    def test_atualizar_stock_incremento(self, db):
        pid, _ = self._insert_peca(db, stock=10)
        try:
            ok = PecaDAO(db).atualizar_stock(pid, 5)
            assert ok is True
            assert PecaDAO(db).consultar_por_id(pid).stock == 15
        finally:
            _cleanup(db, "pecas", "id", pid)

    def test_atualizar_stock_decremento(self, db):
        pid, _ = self._insert_peca(db, stock=10)
        try:
            ok = PecaDAO(db).atualizar_stock(pid, -3)
            assert ok is True
            assert PecaDAO(db).consultar_por_id(pid).stock == 7
        finally:
            _cleanup(db, "pecas", "id", pid)

    def test_atualizar_stock_insuficiente_levanta_valor_error(self, db):
        pid, _ = self._insert_peca(db, stock=3)
        try:
            with pytest.raises(ValueError, match="Stock insuficiente"):
                PecaDAO(db).atualizar_stock(pid, -10)
            # rollback garantido — stock não foi alterado
            assert PecaDAO(db).consultar_por_id(pid).stock == 3
        finally:
            _cleanup(db, "pecas", "id", pid)

    def test_atualizar_stock_peca_inexistente_retorna_false(self, db):
        assert PecaDAO(db).atualizar_stock(999_999_999, 5) is False

    def test_atualizar_peca_inexistente_retorna_false(self, db):
        fantasma = Peca(999_999_999, "Ghost", "d", "f", "c", 1.0, 0, 0)
        assert PecaDAO(db).atualizar(fantasma) is False

    def test_atualizar_campos_persistidos(self, db):
        pid, _ = self._insert_peca(db, stock=5)
        try:
            p_atualizada = Peca(pid, "NomeNovo", "d2", "f2", "c2", 19.99, 8, 1)
            PecaDAO(db).atualizar(p_atualizada)
            lida = PecaDAO(db).consultar_por_id(pid)
            assert lida.nome == "NomeNovo"
            assert float(lida.preco) == pytest.approx(19.99)
            assert lida.stock == 8
        finally:
            _cleanup(db, "pecas", "id", pid)

    def test_stock_zero_apos_decremento_completo(self, db):
        pid, _ = self._insert_peca(db, stock=5)
        try:
            PecaDAO(db).atualizar_stock(pid, -5)
            assert PecaDAO(db).consultar_por_id(pid).stock == 0
        finally:
            _cleanup(db, "pecas", "id", pid)

    def test_consultar_abaixo_minimo_inclui_peca_critica(self, db):
        # stock=1, minimo=5 → deve aparecer nos alertas
        pid, _ = self._insert_peca(db, stock=1)
        # atualizar quantidade_minima para 5 via atualizar()
        p = Peca(pid, f"Alerta-{_uid()}", "d", "f", "c", 1.0, 1, 5)
        PecaDAO(db).atualizar(p)
        try:
            alertas = PecaDAO(db).consultar_abaixo_minimo()
            ids_alerta = [x.id for x in alertas]
            assert pid in ids_alerta
        finally:
            _cleanup(db, "pecas", "id", pid)


# ── ClienteDAO ────────────────────────────────────────────────────────────────

class TestClienteDAOIntegracao:
    """Verifica CRUD real do ClienteDAO contra MySQL."""

    def _insert_cliente(self, db) -> tuple[int, str]:
        nif = _valid_nif()
        c = Cliente(None, f"Test-{_uid()}", nif, "910000000", f"{_uid()}@t.pt", "Rua A")
        ClienteDAO(db).criarCliente(c)
        encontrado = ClienteDAO(db).consultarClienteNIF(nif)
        return encontrado.get_id(), nif

    def test_criar_e_consultar_por_id(self, db):
        cid, nif = self._insert_cliente(db)
        try:
            c = ClienteDAO(db).consultarCliente(cid)
            assert c is not None
            assert c.get_nif() == nif
        finally:
            _cleanup(db, "clientes", "id", cid)

    def test_criar_nif_duplicado_retorna_zero(self, db):
        nif = _valid_nif()
        dao = ClienteDAO(db)
        c1 = Cliente(None, f"A-{_uid()}", nif, "910000001", f"{_uid()}@t.pt", "Rua B")
        c2 = Cliente(None, f"B-{_uid()}", nif, "910000002", f"{_uid()}@t.pt", "Rua C")
        dao.criarCliente(c1)
        try:
            assert dao.criarCliente(c2) == 0
        finally:
            _cleanup(db, "clientes", "nif", nif)

    def test_editar_cliente_altera_dados(self, db):
        cid, nif = self._insert_cliente(db)
        try:
            ok = ClienteDAO(db).editarCliente(cid, "Novo Nome", nif, "920000000", "x@t.pt", "Rua E")
            assert ok is True
            atualizado = ClienteDAO(db).consultarCliente(cid)
            assert atualizado.get_nome() == "Novo Nome"
            assert atualizado.get_contacto() == "920000000"
        finally:
            _cleanup(db, "clientes", "id", cid)

    def test_editar_cliente_inexistente_retorna_false(self, db):
        result = ClienteDAO(db).editarCliente(999_999_999, "X", _valid_nif(), "0", "x@t.pt", "Y")
        assert result is False

    def test_listar_clientes_inclui_inserido(self, db):
        cid, nif = self._insert_cliente(db)
        try:
            ids = [c.get_id() for c in ClienteDAO(db).listarClientes()]
            assert cid in ids
        finally:
            _cleanup(db, "clientes", "id", cid)

    def test_consultar_cliente_inexistente_retorna_none(self, db):
        assert ClienteDAO(db).consultarCliente(999_999_999) is None

    def test_tem_historico_cliente_sem_os(self, db):
        cid, _ = self._insert_cliente(db)
        try:
            assert ClienteDAO(db).tem_historico(cid) is False
        finally:
            _cleanup(db, "clientes", "id", cid)


# ── GestorClientes ────────────────────────────────────────────────────────────

class TestGestorClientesIntegracao:
    """Verifica a gestão de transações do GestorClientes com BD real."""

    def _gestor(self, db) -> GestorClientes:
        return GestorClientes(ClienteDAO(db), TrotineteDAO(db))

    def test_remover_cliente_sem_historico_apaga_registo(self, db):
        nif = _valid_nif()
        dao = ClienteDAO(db)
        dao.criarCliente(Cliente(None, f"Remove-{_uid()}", nif, "910000004", f"{_uid()}@t.pt", "Rua F"))
        cid = dao.consultarClienteNIF(nif).get_id()

        resultado = self._gestor(db).remover_cliente(cid)

        assert resultado is True
        assert dao.consultarCliente(cid) is None  # apagado da BD

    def test_remover_cliente_inexistente_retorna_false(self, db):
        assert self._gestor(db).remover_cliente(999_999_999) is False

    def test_editar_cliente_via_gestor(self, db):
        nif = _valid_nif()
        dao = ClienteDAO(db)
        dao.criarCliente(Cliente(None, f"Antes-{_uid()}", nif, "910000005", f"{_uid()}@t.pt", "Rua G"))
        cid = dao.consultarClienteNIF(nif).get_id()
        try:
            novo_nif = _valid_nif()
            ok = self._gestor(db).editar_cliente(cid, "Depois", novo_nif, "930000000", "d@t.pt", "Rua H")
            assert ok is True
            assert dao.consultarCliente(cid).get_nome() == "Depois"
        finally:
            _cleanup(db, "clientes", "id", cid)

    def test_editar_cliente_inexistente_retorna_menos_um(self, db):
        resultado = self._gestor(db).editar_cliente(999_999_999, "X", _valid_nif(), "0", "x@t.pt", "Y")
        assert resultado == -1


# ── FaturaDAO ─────────────────────────────────────────────────────────────────

class TestFaturaDAOIntegracao:
    """Verifica que o JOIN e a query secundária do FaturaDAO.listar funcionam."""

    def test_listar_retorna_lista(self, db):
        faturas = FaturaDAO(db).listar()
        assert isinstance(faturas, list)

    def test_listar_objetos_tem_campos_obrigatorios(self, db):
        for f in FaturaDAO(db).listar():
            assert isinstance(f.id, int)
            assert isinstance(f.total, float)
            assert f.estado in ("pendente", "paga")
            assert isinstance(f.pecas, dict)

    def test_listar_pecas_dict_estrutura_correta(self, db):
        for fatura in FaturaDAO(db).listar():
            for id_peca, dados in fatura.pecas.items():
                assert "nome" in dados
                assert "quantidade" in dados
                assert "preco_unitario" in dados
                assert isinstance(dados["preco_unitario"], float)
                assert dados["quantidade"] > 0

    def test_consultar_por_id_inexistente_retorna_none(self, db):
        assert FaturaDAO(db).consultar_por_id(999_999_999) is None
