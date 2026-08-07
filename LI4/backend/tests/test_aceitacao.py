"""
Acceptance tests — BDD com pytest-bdd, mapeados directamente às User Stories.

Run with:
    pytest tests/test_aceitacao.py -v -m aceitacao

Feature files: tests/features/
Cada cenário corresponde a um critério de aceitação de uma User Story.
"""
import os
import uuid
import pytest
import bcrypt
import mysql.connector
from datetime import date
from fastapi.testclient import TestClient
from pytest_bdd import given, when, then, parsers, scenarios

from main import app
from auth import criar_token

pytestmark = pytest.mark.aceitacao

# ── Constantes ────────────────────────────────────────────────────────────────
_ADMIN_ID = 1
_TECNICO_ID = 2
_SECRETARIA_ID = 3
_NIF_SEED = "123456789"       # cliente id=1 (João Silva) — dados de seed
_SERIE_SEED = "XM2023001"     # trotinete do cliente id=1

_DB_CONFIG = dict(
    host="localhost", port=int(os.getenv("DB_PORT", "3307")),
    database="scooterfix", user="api_user", password="api123",
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _uid() -> str:
    return uuid.uuid4().hex[:8].upper()


def _valid_nif() -> str:
    """NIF português gerado algoritmicamente (módulo 11)."""
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


def _auth_headers(user_id: int) -> dict:
    token = criar_token({"sub": str(user_id)})
    return {"Authorization": f"Bearer {token}"}


def _exec_sql(conn, sql: str, params=()) -> None:
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    cur.close()


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def http():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def db_conn():
    conn = mysql.connector.connect(**_DB_CONFIG)
    yield conn
    conn.close()


@pytest.fixture
def ctx():
    """Estado partilhado entre os steps de um cenário."""
    return {}


@pytest.fixture(autouse=True)
def _run_cleanup(ctx, db_conn):
    """Executa as funções de limpeza registadas em ctx["_cleanup"] após cada cenário."""
    yield
    for fn in ctx.get("_cleanup", []):
        try:
            fn()
        except Exception:
            pass


# ── Recolha dos cenários ──────────────────────────────────────────────────────

scenarios("features/us01_registar_cliente.feature")
scenarios("features/us02_editar_cliente.feature")
scenarios("features/us03_remover_cliente.feature")
scenarios("features/us04_registar_trotinete.feature")
scenarios("features/us04b_editar_remover_trotinete.feature")
scenarios("features/us05_gestao_utilizadores.feature")
scenarios("features/us06_criar_os.feature")
scenarios("features/us07_estados_os.feature")
scenarios("features/us09_diagnostico_os.feature")
scenarios("features/us10_decisao_cliente.feature")
scenarios("features/us11_stock.feature")
scenarios("features/us12_faturacao.feature")
scenarios("features/us16_intervencao_estado.feature")
scenarios("features/us23_autenticacao.feature")
scenarios("features/us24_permissoes.feature")
scenarios("features/us41_permissoes_utilizadores.feature")


# ── Steps: Perfil de utilizador ───────────────────────────────────────────────

@given("estou autenticado como administrador")
def _dado_admin(ctx):
    ctx["headers"] = _auth_headers(_ADMIN_ID)


@given("estou autenticado como técnico")
def _dado_tecnico(ctx):
    ctx["headers"] = _auth_headers(_TECNICO_ID)


@given("estou autenticado como secretaria")
def _dado_secretaria(ctx):
    ctx["headers"] = _auth_headers(_SECRETARIA_ID)


# ── Steps: Clientes ───────────────────────────────────────────────────────────

@given("existe um cliente registado com um NIF")
def _dado_cliente_com_nif(ctx, http, db_conn):
    ctx.setdefault("headers", _auth_headers(_ADMIN_ID))
    nif = _valid_nif()
    ctx["nif"] = nif
    http.post("/clientes/", json={
        "nome": f"AC-{_uid()}", "nif": nif,
        "contacto": "910000001", "email": f"{_uid()}@t.pt", "morada": "Rua A",
    }, headers=ctx["headers"])
    lista = http.get("/clientes/", headers=ctx["headers"]).json()
    cid = next(c["id"] for c in lista if c["nif"] == nif)
    ctx["cliente_id"] = cid
    ctx.setdefault("_cleanup", []).append(
        lambda cid=cid: _exec_sql(db_conn, "DELETE FROM clientes WHERE id=%s", (cid,))
    )


@given("existe um cliente sem ordens de serviço associadas")
def _dado_cliente_sem_historico(ctx, http, db_conn):
    ctx.setdefault("headers", _auth_headers(_ADMIN_ID))
    nif = _valid_nif()
    ctx["nif"] = nif
    http.post("/clientes/", json={
        "nome": f"SH-{_uid()}", "nif": nif,
        "contacto": "910000002", "email": f"{_uid()}@t.pt", "morada": "Rua B",
    }, headers=ctx["headers"])
    lista = http.get("/clientes/", headers=ctx["headers"]).json()
    cid = next(c["id"] for c in lista if c["nif"] == nif)
    ctx["cliente_id"] = cid
    # Regista cleanup de segurança (no-op se o teste apagou com sucesso)
    ctx.setdefault("_cleanup", []).append(
        lambda cid=cid: _exec_sql(db_conn, "DELETE FROM clientes WHERE id=%s", (cid,))
    )


@when("registo um cliente com NIF único e dados completos")
def _quando_crio_cliente_valido(ctx, http, db_conn):
    nif = _valid_nif()
    ctx["nif_criado"] = nif
    ctx["response"] = http.post("/clientes/", json={
        "nome": f"AC-{_uid()}", "nif": nif,
        "contacto": "910000003", "email": f"{_uid()}@t.pt", "morada": "Rua C",
    }, headers=ctx["headers"])
    ctx.setdefault("_cleanup", []).append(
        lambda nif=nif: _exec_sql(db_conn, "DELETE FROM clientes WHERE nif=%s", (nif,))
    )


@when("registo outro cliente com o mesmo NIF")
def _quando_crio_cliente_nif_duplicado(ctx, http):
    ctx["response"] = http.post("/clientes/", json={
        "nome": f"Dup-{_uid()}", "nif": ctx["nif"],
        "contacto": "910000004", "email": f"{_uid()}@t.pt", "morada": "Rua D",
    }, headers=ctx.get("headers", _auth_headers(_ADMIN_ID)))


@when("registo um cliente sem indicar o NIF")
def _quando_crio_cliente_sem_nif(ctx, http):
    ctx["response"] = http.post("/clientes/", json={
        "nome": "Sem NIF", "contacto": "910000005",
        "email": f"{_uid()}@t.pt", "morada": "Rua E",
    }, headers=ctx["headers"])


@when("registo um cliente com dados válidos")
def _quando_crio_cliente_dados_validos(ctx, http, db_conn):
    nif = _valid_nif()
    ctx["response"] = http.post("/clientes/", json={
        "nome": f"Perm-{_uid()}", "nif": nif,
        "contacto": "910000006", "email": f"{_uid()}@t.pt", "morada": "Rua F",
    }, headers=ctx["headers"])
    if ctx["response"].status_code == 201:
        ctx.setdefault("_cleanup", []).append(
            lambda nif=nif: _exec_sql(db_conn, "DELETE FROM clientes WHERE nif=%s", (nif,))
        )


@when("o administrador remove esse cliente")
def _quando_admin_remove(ctx, http):
    ctx["response"] = http.delete(
        f"/clientes/{ctx['cliente_id']}",
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@when("o administrador tenta remover um cliente inexistente")
def _quando_admin_remove_inexistente(ctx, http):
    ctx["response"] = http.delete(
        "/clientes/999999",
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@then("o cliente aparece na listagem")
def _entao_cliente_aparece(ctx, http):
    lista = http.get("/clientes/", headers=ctx.get("headers", _auth_headers(_ADMIN_ID))).json()
    nif = ctx.get("nif_criado") or ctx.get("nif")
    assert any(c["nif"] == nif for c in lista)


@then("o cliente deixa de existir na listagem")
def _entao_cliente_nao_existe(ctx, http):
    lista = http.get("/clientes/", headers=_auth_headers(_ADMIN_ID)).json()
    assert not any(c["id"] == ctx["cliente_id"] for c in lista)


# ── Steps: Ordens de Serviço ──────────────────────────────────────────────────

@when("crio uma OS para um cliente e trotinete existentes")
def _quando_crio_os(ctx, http, db_conn):
    descricao = f"AC-OS-{_uid()}"
    ctx["os_descricao"] = descricao
    ctx["response"] = http.post("/os/", json={
        "descricao": descricao,
        "nif_cliente": _NIF_SEED,
        "n_serie_trotinete": _SERIE_SEED,
        "id_tecnico": _TECNICO_ID,
    }, headers=ctx["headers"])
    ctx.setdefault("_cleanup", []).append(
        lambda d=descricao: _exec_sql(
            db_conn, "DELETE FROM ordem_de_servico WHERE descricao=%s", (d,)
        )
    )


@when("crio uma OS com número de série inexistente")
def _quando_crio_os_serie_invalida(ctx, http):
    ctx["response"] = http.post("/os/", json={
        "descricao": "OS-SERIE-INVALIDA",
        "nif_cliente": _NIF_SEED,
        "n_serie_trotinete": "SERIE-NAO-EXISTE-XYZ",
        "id_tecnico": _TECNICO_ID,
    }, headers=ctx["headers"])


@when("crio uma OS com NIF de cliente inexistente")
def _quando_crio_os_cliente_invalido(ctx, http):
    ctx["response"] = http.post("/os/", json={
        "descricao": "OS-NIF-INVALIDO",
        "nif_cliente": "100000000",   # NIF válido por checksum, não existe na BD
        "n_serie_trotinete": _SERIE_SEED,
        "id_tecnico": _TECNICO_ID,
    }, headers=ctx["headers"])


@given('existe uma OS no estado "Aguarda Diagnóstico"')
def _dado_os_aguarda_diagnostico(ctx, http, db_conn):
    ctx.setdefault("headers", _auth_headers(_ADMIN_ID))
    descricao = f"AC-OS-ESTADO-{_uid()}"
    http.post("/os/", json={
        "descricao": descricao,
        "nif_cliente": _NIF_SEED,
        "n_serie_trotinete": _SERIE_SEED,
        "id_tecnico": _TECNICO_ID,
    }, headers=ctx["headers"])
    lista = http.get("/os/", headers=ctx["headers"]).json()
    os_ = next((o for o in lista if o["descricao"] == descricao), None)
    assert os_ is not None, f"OS com descrição '{descricao}' não encontrada na listagem"
    ctx["os_id"] = os_["id"]
    ctx.setdefault("_cleanup", []).append(
        lambda d=descricao: _exec_sql(
            db_conn, "DELETE FROM ordem_de_servico WHERE descricao=%s", (d,)
        )
    )


@when('avanço o estado para "Em Reparação" directamente')
def _quando_avanço_estado_invalido(ctx, http):
    ctx["response"] = http.put(
        f"/os/{ctx['os_id']}/proximo_estado",
        json={"id": ctx["os_id"], "estado": "Em Reparação", "tipo_pagamento": "dinheiro"},
        headers=ctx["headers"],
    )


@when("avanço o estado de uma OS inexistente")
def _quando_avanço_os_inexistente(ctx, http):
    ctx["response"] = http.put(
        "/os/999999/avancar",
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@then(parsers.parse('a OS é criada com estado "{estado}"'))
def _entao_os_estado(ctx, http, estado):
    lista = http.get("/os/", headers=ctx.get("headers", _auth_headers(_ADMIN_ID))).json()
    os_ = next((o for o in lista if o["descricao"] == ctx["os_descricao"]), None)
    assert os_ is not None
    assert os_["estado"] == estado


# ── Steps: Autenticação ───────────────────────────────────────────────────────

@when(parsers.parse('autentico com username "{username}" e password "{password}"'))
def _quando_autentico_credenciais(ctx, http, username, password):
    ctx["response"] = http.post("/auth/login", json={
        "username": username, "password": password,
    })


@given("existe uma conta desativada no sistema")
def _dado_conta_desativada(ctx, db_conn):
    password = "TestAC789"
    salt = bcrypt.gensalt()
    h = bcrypt.hashpw(password.encode(), salt).decode()
    username = f"inativo_ac_{_uid()}@test.pt"
    cur = db_conn.cursor()
    cur.execute(
        "INSERT INTO utilizadores "
        "(nome, username, password_hash, password_salt, perfil, ativo, data_registo) "
        "VALUES (%s, %s, %s, %s, 'tecnico', 0, CURDATE())",
        (f"Inativo AC {_uid()}", username, h, salt.decode()),
    )
    uid = cur.lastrowid
    db_conn.commit()
    cur.close()
    ctx["username"] = username
    ctx["password"] = password
    ctx.setdefault("_cleanup", []).append(
        lambda uid=uid: _exec_sql(db_conn, "DELETE FROM utilizadores WHERE id=%s", (uid,))
    )


@when("autentico com as credenciais dessa conta")
def _quando_autentico_conta(ctx, http):
    ctx["response"] = http.post("/auth/login", json={
        "username": ctx["username"], "password": ctx["password"],
    })


@when("acedo a um recurso protegido sem token")
def _quando_acedo_sem_token(ctx, http):
    ctx["response"] = http.get("/clientes/")


# ── Steps: Stock ──────────────────────────────────────────────────────────────

@when("registo uma nova peça de stock")
def _quando_crio_peca(ctx, http, db_conn):
    nome = f"AC-Peca-{_uid()}"
    ctx["response"] = http.post("/stock/", json={
        "nome": nome, "descricao": "desc", "fornecedor": "forn",
        "categoria": "cat", "stock": 5, "stock_minimo": 1, "preco": 1.0,
    }, headers=ctx["headers"])
    if ctx["response"].status_code == 201:
        ctx.setdefault("_cleanup", []).append(
            lambda nome=nome: _exec_sql(db_conn, "DELETE FROM pecas WHERE nome=%s", (nome,))
        )


@when("consulto a lista de clientes")
def _quando_consulto_clientes(ctx, http):
    ctx["response"] = http.get("/clientes/", headers=ctx["headers"])


# ── Steps: Editar cliente (US02) ──────────────────────────────────────────────

@when("o administrador edita os dados desse cliente")
def _quando_admin_edita_cliente(ctx, http):
    ctx["response"] = http.put(
        f"/clientes/{ctx['cliente_id']}",
        json={
            "nome": f"Editado-{_uid()}", "nif": ctx["nif"],
            "contacto": "910000099", "email": f"{_uid()}@t.pt", "morada": "Rua Z",
        },
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@when("o administrador tenta editar um cliente inexistente")
def _quando_admin_edita_inexistente(ctx, http):
    ctx["response"] = http.put(
        "/clientes/999999",
        json={
            "nome": "Ghost", "nif": "999999990",
            "contacto": "910000000", "email": "ghost@t.pt", "morada": "Rua X",
        },
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


# ── Steps: Trotinetes (US04) ──────────────────────────────────────────────────

@when("registo uma trotinete para esse cliente")
def _quando_crio_trotinete(ctx, http, db_conn):
    serie = f"AC-{_uid()}"
    ctx["trotinete_serie"] = serie
    ctx["response"] = http.post("/trotinetes/", json={
        "marca": "Marca AC", "modelo": "Modelo AC",
        "serie": serie, "clienteId": ctx["cliente_id"],
    }, headers=ctx.get("headers", _auth_headers(_ADMIN_ID)))
    if ctx["response"].status_code == 201:
        ctx.setdefault("_cleanup", []).append(
            lambda s=serie: _exec_sql(db_conn, "DELETE FROM trotinetes WHERE numero_serie=%s", (s,))
        )


@given("existe uma trotinete registada com uma série")
def _dado_trotinete_com_serie(ctx):
    ctx.setdefault("headers", _auth_headers(_ADMIN_ID))
    ctx["serie"] = _SERIE_SEED


@when("registo outra trotinete com a mesma série")
def _quando_crio_trotinete_serie_duplicada(ctx, http):
    ctx["response"] = http.post("/trotinetes/", json={
        "marca": "Dup", "modelo": "Dup",
        "serie": ctx["serie"], "clienteId": 1,
    }, headers=ctx.get("headers", _auth_headers(_ADMIN_ID)))


@then("a trotinete aparece na listagem")
def _entao_trotinete_aparece(ctx, http):
    lista = http.get("/trotinetes/", headers=_auth_headers(_ADMIN_ID)).json()
    assert any(t["serie"] == ctx["trotinete_serie"] for t in lista)


# ── Steps: Utilizadores (US05) ────────────────────────────────────────────────

@given("existe um utilizador técnico no sistema")
def _dado_utilizador_tecnico(ctx, http, db_conn):
    ctx.setdefault("headers", _auth_headers(_ADMIN_ID))
    username = f"tecnico_ac_{_uid()}@test.pt"
    r = http.post("/utilizadores", json={
        "nome": f"Tecnico AC {_uid()}",
        "username": username,
        "password": "Teste1234",
        "perfil": "tecnico",
    }, headers=ctx["headers"])
    uid = r.json()["id"]
    ctx["utilizador_id"] = uid
    ctx.setdefault("_cleanup", []).append(
        lambda uid=uid: _exec_sql(db_conn, "DELETE FROM utilizadores WHERE id=%s", (uid,))
    )


@when("o administrador edita o nome desse utilizador")
def _quando_admin_edita_utilizador(ctx, http):
    ctx["response"] = http.put(
        f"/utilizadores/{ctx['utilizador_id']}",
        json={"nome": f"Editado-{_uid()}", "perfil": "tecnico"},
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@when("o administrador desativa esse utilizador")
def _quando_admin_desativa_utilizador(ctx, http):
    ctx["response"] = http.put(
        f"/utilizadores/{ctx['utilizador_id']}/desativar",
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@when("o administrador tenta desativar a própria conta")
def _quando_admin_desativa_propria_conta(ctx, http):
    ctx["response"] = http.put(
        f"/utilizadores/{_ADMIN_ID}/desativar",
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


# ── Steps: Diagnóstico (US09) ─────────────────────────────────────────────────

@when("o técnico regista um diagnóstico nessa OS")
def _quando_tecnico_regista_diagnostico(ctx, http):
    ctx["response"] = http.put(
        f"/os/{ctx['os_id']}/diagnostico",
        json={"descricao": "Bateria danificada", "tempo_estimado": 1.5, "pecas": {}},
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@when('tento avançar a OS para "Aguarda Resposta" sem diagnóstico')
def _quando_avanço_sem_diagnostico(ctx, http):
    ctx["response"] = http.put(
        f"/os/{ctx['os_id']}/proximo_estado",
        json={"id": ctx["os_id"], "estado": "Aguarda Resposta", "tipo_pagamento": "dinheiro"},
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


# ── Steps: Decisão do cliente (US10) ─────────────────────────────────────────

@given('existe uma OS em "Aguarda Resposta"')
def _dado_os_aguarda_resposta(ctx, http, db_conn):
    ctx.setdefault("headers", _auth_headers(_ADMIN_ID))
    descricao = f"AC-OS-AR-{_uid()}"
    http.post("/os/", json={
        "descricao": descricao,
        "nif_cliente": _NIF_SEED,
        "n_serie_trotinete": _SERIE_SEED,
        "id_tecnico": _TECNICO_ID,
    }, headers=ctx["headers"])
    lista = http.get("/os/", headers=ctx["headers"]).json()
    os_ = next((o for o in lista if o["descricao"] == descricao), None)
    assert os_ is not None, f"OS '{descricao}' não encontrada"
    os_id = os_["id"]

    http.put(f"/os/{os_id}/diagnostico", json={
        "descricao": "Diagnóstico AC", "tempo_estimado": 1.0, "pecas": {},
    }, headers=ctx["headers"])
    http.put(f"/os/{os_id}/proximo_estado", json={
        "id": os_id, "estado": "Aguarda Resposta", "tipo_pagamento": "dinheiro",
    }, headers=ctx["headers"])

    ctx["os_id"] = os_id
    # fatura pode ser criada se o cliente recusar; apagar antes da OS (sem CASCADE)
    ctx.setdefault("_cleanup", []).append(
        lambda oid=os_id: _exec_sql(db_conn, "DELETE FROM fatura WHERE id_os=%s", (oid,))
    )
    ctx.setdefault("_cleanup", []).append(
        lambda d=descricao: _exec_sql(
            db_conn, "DELETE FROM ordem_de_servico WHERE descricao=%s", (d,)
        )
    )


@when("o cliente aprova o orçamento")
def _quando_cliente_aprova(ctx, http):
    ctx["response"] = http.put(
        f"/os/{ctx['os_id']}/decisao-cliente",
        json={"decisao": "Aprovado"},
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@when("o cliente recusa o orçamento")
def _quando_cliente_recusa(ctx, http):
    ctx["response"] = http.put(
        f"/os/{ctx['os_id']}/decisao-cliente",
        json={"decisao": "Rejeitado"},
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@when("registo uma decisão inválida do cliente")
def _quando_decisao_invalida(ctx, http):
    ctx["response"] = http.put(
        f"/os/{ctx['os_id']}/decisao-cliente",
        json={"decisao": "Talvez"},
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


# ── Steps: Stock (US11) ───────────────────────────────────────────────────────

@when("crio uma peça com stock e nível mínimo definidos")
def _quando_crio_peca_com_minimo(ctx, http, db_conn):
    nome = f"AC-PecaMin-{_uid()}"
    ctx["peca_nome"] = nome
    ctx["peca_stock_minimo"] = 3
    ctx["response"] = http.post("/stock/", json={
        "nome": nome, "descricao": "desc", "fornecedor": "forn",
        "categoria": "cat", "stock": 10, "stock_minimo": 3, "preco": 2.5,
    }, headers=ctx.get("headers", _auth_headers(_ADMIN_ID)))
    if ctx["response"].status_code == 201:
        ctx.setdefault("_cleanup", []).append(
            lambda nome=nome: _exec_sql(db_conn, "DELETE FROM pecas WHERE nome=%s", (nome,))
        )


@then("a peça aparece na listagem com o nível mínimo correto")
def _entao_peca_nivel_minimo(ctx, http):
    lista = http.get("/stock/", headers=_auth_headers(_ADMIN_ID)).json()
    peca = next((p for p in lista if p["nome"] == ctx["peca_nome"]), None)
    assert peca is not None, "Peça não encontrada na listagem"
    assert peca["stock_minimo"] == ctx["peca_stock_minimo"]


@given("existe uma peça de stock no sistema")
def _dado_peca_no_sistema(ctx, http, db_conn):
    ctx.setdefault("headers", _auth_headers(_ADMIN_ID))
    nome = f"AC-PecaExist-{_uid()}"
    ctx["peca_nome"] = nome
    http.post("/stock/", json={
        "nome": nome, "descricao": "desc", "fornecedor": "forn",
        "categoria": "cat", "stock": 5, "stock_minimo": 1, "preco": 1.0,
    }, headers=ctx["headers"])
    lista = http.get("/stock/", headers=ctx["headers"]).json()
    peca = next((p for p in lista if p["nome"] == nome), None)
    assert peca is not None
    ctx["peca_id"] = peca["codigo"]
    ctx.setdefault("_cleanup", []).append(
        lambda nome=nome: _exec_sql(db_conn, "DELETE FROM pecas WHERE nome=%s", (nome,))
    )


@when("o administrador atualiza o stock dessa peça")
def _quando_admin_atualiza_stock(ctx, http):
    ctx["response"] = http.put(
        f"/stock/{ctx['peca_id']}",
        json={
            "nome": ctx["peca_nome"], "descricao": "desc", "fornecedor": "forn",
            "categoria": "cat", "stock": 20, "stock_minimo": 1, "preco": 1.0,
        },
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


# ── Steps: Editar/Remover Trotinete (US04b) ──────────────────────────────────

@given("existe uma trotinete registada com uma série")
def _dado_trotinete_com_serie(ctx, http):
    ctx.setdefault("headers", _auth_headers(_ADMIN_ID))
    lista = http.get("/trotinetes/", headers=ctx["headers"]).json()
    t = next((t for t in lista if t["serie"] == _SERIE_SEED), None)
    assert t is not None, "Trotinete seed não encontrada"
    ctx["serie"] = _SERIE_SEED
    ctx["trotinete_id"] = t["id"]
    ctx["trotinete_cliente_id"] = t["clienteId"]


@when("edito os dados dessa trotinete")
def _quando_edito_trotinete(ctx, http):
    ctx["response"] = http.put(
        f"/trotinetes/{ctx['trotinete_id']}",
        json={
            "marca": f"Editado-{_uid()}",
            "modelo": "Modelo Editado",
            "serie": ctx["serie"],
            "clienteId": ctx.get("trotinete_cliente_id", 1),
        },
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@when("edito uma trotinete inexistente")
def _quando_edito_trotinete_inexistente(ctx, http):
    ctx["response"] = http.put(
        "/trotinetes/999999",
        json={"marca": "Ghost", "modelo": "Ghost", "serie": "GHOST-001", "clienteId": 1},
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@given("existe uma trotinete sem OS associadas")
def _dado_trotinete_sem_os(ctx, http, db_conn):
    ctx.setdefault("headers", _auth_headers(_ADMIN_ID))
    serie = f"NOOS-{_uid()}"
    http.post("/trotinetes/", json={
        "marca": "Test", "modelo": "Test", "serie": serie, "clienteId": 1,
    }, headers=ctx["headers"])
    lista = http.get("/trotinetes/", headers=ctx["headers"]).json()
    t = next((t for t in lista if t["serie"] == serie), None)
    assert t is not None
    ctx["trotinete_id"] = t["id"]
    ctx.setdefault("_cleanup", []).append(
        lambda s=serie: _exec_sql(db_conn, "DELETE FROM trotinetes WHERE numero_serie=%s", (s,))
    )


@when("o administrador remove essa trotinete pelo id")
def _quando_admin_remove_trotinete_por_id(ctx, http):
    ctx["response"] = http.delete(
        f"/trotinetes/{ctx['trotinete_id']}",
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@when("o administrador remove uma trotinete inexistente")
def _quando_admin_remove_trotinete_inexistente(ctx, http):
    ctx["response"] = http.delete(
        "/trotinetes/999999",
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


# ── Steps: Intervenção / RF24 (US16) ─────────────────────────────────────────

@when("o técnico tenta registar uma intervenção nessa OS")
def _quando_tecnico_tenta_intervencao(ctx, http):
    ctx["response"] = http.put(
        f"/os/{ctx['os_id']}/intervencao",
        json={"descricao": "Intervencao inválida", "tempo": 1.0, "pecas": {}},
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


@given('existe uma OS em "Em Reparação"')
def _dado_os_em_reparacao(ctx, http, db_conn):
    ctx.setdefault("headers", _auth_headers(_ADMIN_ID))
    descricao = f"AC-OS-ER-{_uid()}"
    http.post("/os/", json={
        "descricao": descricao,
        "nif_cliente": _NIF_SEED,
        "n_serie_trotinete": _SERIE_SEED,
        "id_tecnico": _TECNICO_ID,
    }, headers=ctx["headers"])
    lista = http.get("/os/", headers=ctx["headers"]).json()
    os_ = next((o for o in lista if o["descricao"] == descricao), None)
    assert os_ is not None, f"OS '{descricao}' não encontrada"
    os_id = os_["id"]

    http.put(f"/os/{os_id}/diagnostico", json={
        "descricao": "Diagnóstico AC", "tempo_estimado": 1.0, "pecas": {},
    }, headers=ctx["headers"])
    http.put(f"/os/{os_id}/proximo_estado", json={
        "id": os_id, "estado": "Aguarda Resposta", "tipo_pagamento": "dinheiro",
    }, headers=ctx["headers"])
    http.put(f"/os/{os_id}/decisao-cliente", json={"decisao": "Aprovado"}, headers=ctx["headers"])

    ctx["os_id"] = os_id
    ctx.setdefault("_cleanup", []).append(
        lambda d=descricao: _exec_sql(
            db_conn, "DELETE FROM ordem_de_servico WHERE descricao=%s", (d,)
        )
    )


@when("o técnico regista uma intervenção nessa OS")
def _quando_tecnico_regista_intervencao_valida(ctx, http):
    ctx["response"] = http.put(
        f"/os/{ctx['os_id']}/intervencao",
        json={"descricao": "Substituição de bateria", "tempo": 0.5, "pecas": {}},
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


# ── Steps: Permissões criação utilizadores (US41) ────────────────────────────

@when("tento criar um utilizador com perfil técnico")
def _quando_tento_criar_utilizador(ctx, http):
    ctx["response"] = http.post("/utilizadores", json={
        "nome": f"Test-{_uid()}",
        "username": f"test_{_uid()}@t.pt",
        "password": "Teste1234",
        "perfil": "tecnico",
    }, headers=ctx.get("headers", _auth_headers(_TECNICO_ID)))


# ── Steps: Faturas (US12) ─────────────────────────────────────────────────────

@when("consulto a listagem de faturas")
def _quando_consulto_faturas(ctx, http):
    ctx["response"] = http.get("/fatura/", headers=ctx["headers"])


@when("faço download de uma fatura inexistente")
def _quando_download_fatura_inexistente(ctx, http):
    ctx["response"] = http.get(
        "/fatura/999999/download",
        headers=ctx.get("headers", _auth_headers(_ADMIN_ID)),
    )


# ── Step: Verificação genérica ────────────────────────────────────────────────

@then(parsers.parse("a resposta tem código {codigo:d}"))
def _entao_codigo(ctx, codigo):
    assert ctx["response"].status_code == codigo, (
        f"Esperava {codigo}, obteve {ctx['response'].status_code}: "
        f"{ctx['response'].text[:200]}"
    )
