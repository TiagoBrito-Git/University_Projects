"""
System tests — exercitam a aplicação completa via HTTP sem conhecimento
da implementação interna.

Run with:
    pytest tests/test_sistema.py -v -m sistema

Requerem MySQL em localhost:3306. Cada teste que cria dados na BD limpa-os
num bloco finally, garantindo idempotência.
"""
import os
import uuid
import pytest
import bcrypt
import mysql.connector
from datetime import date, timedelta
from fastapi.testclient import TestClient

from main import app
from auth import criar_token

pytestmark = pytest.mark.sistema

_DB_CONFIG = dict(
    host="localhost", port=int(os.getenv("DB_PORT", "3307")),
    database="scooterfix", user="api_user", password="api123",
)

# IDs dos utilizadores inseridos pelo script de seed
_ADMIN_ID = 1       # administrador — todas as permissões
_TECNICO_ID = 2     # tecnico — ler*, editarOS
_SECRETARIA_ID = 3  # secretaria — criar/ler clientes, criar/ler OS, pagarFatura

# Dados do seed para criação de OS
_NIF_CLIENTE_SEED = "123456789"   # cliente id=1 (João Silva)
_SERIE_TROTINETE_SEED = "XM2023001"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _uid() -> str:
    return uuid.uuid4().hex[:8].upper()


def _valid_nif() -> str:
    """Gera um NIF português pseudo-aleatório que passa o checksum módulo 11."""
    base_int = uuid.uuid4().int % 90_000_000 + 10_000_000
    digits = list(str(base_int))
    if digits[0] not in "12356789":
        digits[0] = "5"
    base = "".join(digits)
    total = sum(int(base[i]) * (9 - i) for i in range(8))
    check = 11 - (total % 11)
    if check >= 10:
        check = 0
    return base + str(check)


def _auth(user_id: int) -> dict:
    """Cabeçalho Bearer com token JWT válido para o utilizador dado."""
    token = criar_token({"sub": str(user_id)})
    return {"Authorization": f"Bearer {token}"}


def _cleanup(db, table: str, field: str, value) -> None:
    cur = db.cursor()
    cur.execute(f"DELETE FROM {table} WHERE {field} = %s", (value,))
    db.commit()
    cur.close()


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def client():
    """TestClient partilhado pelo módulo — inicia a app uma única vez."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def db():
    """Ligação MySQL direta para setup/cleanup de dados de teste."""
    conn = mysql.connector.connect(**_DB_CONFIG)
    yield conn
    conn.close()


# ── TestSistema_HealthCheck ───────────────────────────────────────────────────

class TestSistema_HealthCheck:
    """Verifica que a API está acessível e a responder."""

    def test_root_retorna_ok(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_health_retorna_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


# ── TestSistema_Autenticacao ──────────────────────────────────────────────────

class TestSistema_Autenticacao:
    """Testa o endpoint POST /auth/login e a validação de tokens."""

    def test_login_username_inexistente_retorna_401(self, client):
        r = client.post("/auth/login", json={
            "username": "naoexiste@oficina.pt",
            "password": "qualquercoisa",
        })
        assert r.status_code == 401

    def test_login_password_errada_retorna_401(self, client):
        r = client.post("/auth/login", json={
            "username": "joao.silva@oficina.pt",
            "password": "passworderrada",
        })
        assert r.status_code == 401

    def test_login_sem_body_retorna_422(self, client):
        r = client.post("/auth/login", json={})
        assert r.status_code == 422

    def test_login_utilizador_inativo_retorna_403(self, client, db):
        password = "TestInativo123"
        salt = bcrypt.gensalt()
        h = bcrypt.hashpw(password.encode(), salt).decode()
        username = f"inativo_{_uid()}@test.pt"
        cur = db.cursor()
        cur.execute(
            "INSERT INTO utilizadores "
            "(nome, username, password_hash, password_salt, perfil, ativo, data_registo) "
            "VALUES (%s, %s, %s, %s, 'tecnico', 0, CURDATE())",
            (f"Inativo {_uid()}", username, h, salt.decode()),
        )
        uid_inserido = cur.lastrowid
        db.commit()
        cur.close()
        try:
            r = client.post("/auth/login", json={"username": username, "password": password})
            assert r.status_code == 403
            assert "desativada" in r.json()["detail"].lower()
        finally:
            _cleanup(db, "utilizadores", "id", uid_inserido)

    def test_login_utilizador_ativo_retorna_200_com_token(self, client, db):
        password = "TestAtivo456"
        salt = bcrypt.gensalt()
        h = bcrypt.hashpw(password.encode(), salt).decode()
        username = f"ativo_{_uid()}@test.pt"
        cur = db.cursor()
        cur.execute(
            "INSERT INTO utilizadores "
            "(nome, username, password_hash, password_salt, perfil, ativo, data_registo) "
            "VALUES (%s, %s, %s, %s, 'tecnico', 1, CURDATE())",
            (f"Ativo {_uid()}", username, h, salt.decode()),
        )
        uid_inserido = cur.lastrowid
        db.commit()
        cur.close()
        try:
            r = client.post("/auth/login", json={"username": username, "password": password})
            assert r.status_code == 200
            body = r.json()
            assert "access_token" in body
            assert body["perfil"] == "tecnico"
            assert len(body["access_token"]) > 20
        finally:
            _cleanup(db, "utilizadores", "id", uid_inserido)

    def test_sem_token_retorna_401(self, client):
        r = client.get("/clientes/")
        assert r.status_code == 401

    def test_token_invalido_retorna_401(self, client):
        r = client.get("/clientes/", headers={"Authorization": "Bearer token.invalido.xyz"})
        assert r.status_code == 401


# ── TestSistema_Permissoes ────────────────────────────────────────────────────

class TestSistema_Permissoes:
    """Verifica que a middleware de permissões aplica as restrições corretas."""

    def test_tecnico_sem_criarCliente_retorna_403(self, client):
        r = client.post("/clientes/", json={
            "nome": "X", "nif": _valid_nif(),
            "contacto": "910000000", "email": "x@t.pt", "morada": "Rua A",
        }, headers=_auth(_TECNICO_ID))
        assert r.status_code == 403

    def test_tecnico_com_lerCliente_pode_listar(self, client):
        r = client.get("/clientes/", headers=_auth(_TECNICO_ID))
        assert r.status_code == 200

    def test_secretaria_sem_criarPeca_retorna_403(self, client):
        r = client.post("/stock/", json={
            "nome": "Peca X", "descricao": "d", "fornecedor": "f",
            "categoria": "c", "stock": 10, "stock_minimo": 2, "preco": 5.0,
        }, headers=_auth(_SECRETARIA_ID))
        assert r.status_code == 403

    def test_admin_com_criarPeca_retorna_201(self, client, db):
        nome = f"PermTest-{_uid()}"
        r = client.post("/stock/", json={
            "nome": nome, "descricao": "d", "fornecedor": "f",
            "categoria": "c", "stock": 5, "stock_minimo": 1, "preco": 1.0,
        }, headers=_auth(_ADMIN_ID))
        assert r.status_code == 201
        cur = db.cursor()
        cur.execute("DELETE FROM pecas WHERE nome = %s", (nome,))
        db.commit()
        cur.close()

    def test_401_sem_token_vs_403_sem_permissao(self, client):
        # Token ausente → 401 (HTTPBearer não encontra credenciais)
        sem_token = client.get("/clientes/")
        assert sem_token.status_code == 401
        # Token válido mas sem permissão → 403 (requer_operacao rejeita)
        sem_perm = client.post("/clientes/", json={
            "nome": "X", "nif": _valid_nif(),
            "contacto": "910000000", "email": "x@t.pt", "morada": "Rua A",
        }, headers=_auth(_TECNICO_ID))
        assert sem_perm.status_code == 403


# ── TestSistema_Clientes ──────────────────────────────────────────────────────

class TestSistema_Clientes:
    """Ciclo CRUD completo de clientes através dos endpoints HTTP."""

    def test_listar_clientes_retorna_lista_com_estrutura(self, client):
        r = client.get("/clientes/", headers=_auth(_ADMIN_ID))
        assert r.status_code == 200
        lista = r.json()
        assert isinstance(lista, list)
        assert len(lista) > 0
        primeiro = lista[0]
        assert "id" in primeiro
        assert "nome" in primeiro
        assert "nif" in primeiro

    def test_criar_cliente_retorna_201(self, client, db):
        nif = _valid_nif()
        r = client.post("/clientes/", json={
            "nome": f"SysTest-{_uid()}", "nif": nif,
            "contacto": "910000001", "email": f"{_uid()}@t.pt", "morada": "Rua B",
        }, headers=_auth(_ADMIN_ID))
        try:
            assert r.status_code == 201
            assert "sucesso" in r.json()["message"].lower()
        finally:
            _cleanup(db, "clientes", "nif", nif)

    def test_criar_cliente_nif_duplicado_retorna_400(self, client, db):
        nif = _valid_nif()
        payload = {
            "nome": f"Dup-{_uid()}", "nif": nif,
            "contacto": "910000002", "email": f"{_uid()}@t.pt", "morada": "Rua C",
        }
        client.post("/clientes/", json=payload, headers=_auth(_ADMIN_ID))
        try:
            r2 = client.post("/clientes/", json=payload, headers=_auth(_ADMIN_ID))
            assert r2.status_code == 400
        finally:
            _cleanup(db, "clientes", "nif", nif)

    def test_editar_cliente_altera_dados_e_retorna_200(self, client, db):
        nif = _valid_nif()
        client.post("/clientes/", json={
            "nome": "Antes", "nif": nif,
            "contacto": "910000003", "email": f"{_uid()}@t.pt", "morada": "Rua D",
        }, headers=_auth(_ADMIN_ID))
        lista = client.get("/clientes/", headers=_auth(_ADMIN_ID)).json()
        cid = next(c["id"] for c in lista if c["nif"] == nif)
        try:
            r = client.put(f"/clientes/{cid}", json={
                "nome": "Depois", "nif": _valid_nif(),
                "contacto": "920000000", "email": f"{_uid()}@t.pt", "morada": "Rua E",
            }, headers=_auth(_ADMIN_ID))
            assert r.status_code == 200
            assert "sucesso" in r.json()["message"].lower()
        finally:
            _cleanup(db, "clientes", "id", cid)

    def test_editar_cliente_inexistente_retorna_404(self, client):
        r = client.put("/clientes/999999", json={
            "nome": "X", "nif": _valid_nif(),
            "contacto": "910000000", "email": "x@t.pt", "morada": "Y",
        }, headers=_auth(_ADMIN_ID))
        assert r.status_code == 404

    def test_remover_cliente_sem_historico_retorna_200(self, client, db):
        nif = _valid_nif()
        client.post("/clientes/", json={
            "nome": f"Remover-{_uid()}", "nif": nif,
            "contacto": "910000004", "email": f"{_uid()}@t.pt", "morada": "Rua F",
        }, headers=_auth(_ADMIN_ID))
        lista = client.get("/clientes/", headers=_auth(_ADMIN_ID)).json()
        cid = next(c["id"] for c in lista if c["nif"] == nif)
        r = client.delete(f"/clientes/{cid}", headers=_auth(_ADMIN_ID))
        assert r.status_code == 200
        # confirmar que desapareceu da listagem
        lista_apos = client.get("/clientes/", headers=_auth(_ADMIN_ID)).json()
        assert not any(c["id"] == cid for c in lista_apos)

    def test_remover_cliente_inexistente_retorna_404(self, client):
        r = client.delete("/clientes/999999", headers=_auth(_ADMIN_ID))
        assert r.status_code == 404

    def test_criar_cliente_campo_obrigatorio_em_falta_retorna_422(self, client):
        r = client.post("/clientes/", json={"nome": "Só nome"},
                        headers=_auth(_ADMIN_ID))
        assert r.status_code == 422


# ── TestSistema_Stock ─────────────────────────────────────────────────────────

class TestSistema_Stock:
    """CRUD de peças de stock via HTTP."""

    def test_listar_pecas_retorna_lista_com_estrutura(self, client):
        r = client.get("/stock/", headers=_auth(_ADMIN_ID))
        assert r.status_code == 200
        lista = r.json()
        assert isinstance(lista, list)
        assert len(lista) > 0
        p = lista[0]
        assert "codigo" in p
        assert "nome" in p
        assert "stock" in p

    def test_criar_peca_retorna_201(self, client, db):
        nome = f"SysPeca-{_uid()}"
        r = client.post("/stock/", json={
            "nome": nome, "descricao": "desc", "fornecedor": "forn",
            "categoria": "cat", "stock": 10, "stock_minimo": 2, "preco": 9.99,
        }, headers=_auth(_ADMIN_ID))
        try:
            assert r.status_code == 201
        finally:
            cur = db.cursor()
            cur.execute("DELETE FROM pecas WHERE nome = %s", (nome,))
            db.commit()
            cur.close()

    def test_criar_peca_campos_em_falta_retorna_422(self, client):
        r = client.post("/stock/", json={"nome": "sem campos"},
                        headers=_auth(_ADMIN_ID))
        assert r.status_code == 422

    def test_editar_peca_retorna_200(self, client, db):
        nome = f"SysPecaEdit-{_uid()}"
        client.post("/stock/", json={
            "nome": nome, "descricao": "d", "fornecedor": "f",
            "categoria": "c", "stock": 5, "stock_minimo": 1, "preco": 1.0,
        }, headers=_auth(_ADMIN_ID))
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT id FROM pecas WHERE nome = %s", (nome,))
        pid = cur.fetchone()["id"]
        cur.close()
        try:
            r = client.put(f"/stock/{pid}", json={
                "nome": nome, "descricao": "novo desc", "fornecedor": "f",
                "categoria": "c", "stock": 8, "stock_minimo": 1, "preco": 2.50,
            }, headers=_auth(_ADMIN_ID))
            assert r.status_code == 200
        finally:
            _cleanup(db, "pecas", "id", pid)

    def test_secretaria_pode_listar_pecas(self, client):
        r = client.get("/stock/", headers=_auth(_SECRETARIA_ID))
        assert r.status_code == 200


# ── TestSistema_OS ────────────────────────────────────────────────────────────

class TestSistema_OS:
    """Testes do ciclo de vida das Ordens de Serviço via HTTP."""

    def _payload_os(self, descricao: str) -> dict:
        return {
            "descricao": descricao,
            "nif_cliente": _NIF_CLIENTE_SEED,
            "n_serie_trotinete": _SERIE_TROTINETE_SEED,
            "id_tecnico": _TECNICO_ID,
            "data_conclusao": str(date.today() + timedelta(days=7)),
        }

    def test_listar_os_retorna_lista_com_estrutura(self, client):
        r = client.get("/os/", headers=_auth(_ADMIN_ID))
        assert r.status_code == 200
        lista = r.json()
        assert isinstance(lista, list)
        if lista:
            os_ = lista[0]
            assert "id" in os_
            assert "estado" in os_
            assert "descricao" in os_

    def test_criar_os_retorna_201(self, client, db):
        descricao = f"SysTest-OS-{_uid()}"
        r = client.post("/os/", json=self._payload_os(descricao),
                        headers=_auth(_ADMIN_ID))
        try:
            assert r.status_code == 201
            assert "sucesso" in r.json()["message"].lower()
        finally:
            cur = db.cursor()
            cur.execute("DELETE FROM ordem_de_servico WHERE descricao = %s", (descricao,))
            db.commit()
            cur.close()

    def test_criar_os_estado_inicial_e_aguarda_diagnostico(self, client, db):
        descricao = f"SysEstado-OS-{_uid()}"
        client.post("/os/", json=self._payload_os(descricao),
                    headers=_auth(_ADMIN_ID))
        try:
            lista = client.get("/os/", headers=_auth(_ADMIN_ID)).json()
            os_criada = next((o for o in lista if o["descricao"] == descricao), None)
            assert os_criada is not None
            assert os_criada["estado"] == "Aguarda Diagnóstico"
        finally:
            cur = db.cursor()
            cur.execute("DELETE FROM ordem_de_servico WHERE descricao = %s", (descricao,))
            db.commit()
            cur.close()

    def test_criar_os_cliente_inexistente_retorna_404(self, client):
        r = client.post("/os/", json={
            "descricao": "OS inválida",
            "nif_cliente": "100000000",  # NIF válido por checksum mas não existe na BD
            "n_serie_trotinete": _SERIE_TROTINETE_SEED,
            "id_tecnico": _TECNICO_ID,
            "data_conclusao": str(date.today() + timedelta(days=7)),
        }, headers=_auth(_ADMIN_ID))
        assert r.status_code == 404

    def test_criar_os_trotinete_inexistente_retorna_404(self, client):
        r = client.post("/os/", json={
            "descricao": "OS inválida",
            "nif_cliente": _NIF_CLIENTE_SEED,
            "n_serie_trotinete": "SERIE-INEXISTENTE-XYZ",
            "id_tecnico": _TECNICO_ID,
            "data_conclusao": str(date.today() + timedelta(days=7)),
        }, headers=_auth(_ADMIN_ID))
        assert r.status_code == 404

    def test_avancar_estado_os_inexistente_retorna_400(self, client):
        r = client.put("/os/999999/avancar", headers=_auth(_ADMIN_ID))
        assert r.status_code == 400

    def test_config_os_retorna_taxas(self, client):
        r = client.get("/os/config", headers=_auth(_ADMIN_ID))
        assert r.status_code == 200
        body = r.json()
        assert "taxa_mao_obra" in body
        assert "taxa_diagnostico" in body
        assert body["taxa_mao_obra"] > 0
