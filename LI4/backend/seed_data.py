import argparse
import json
import os
import sys
import bcrypt
from datetime import datetime, date
from typing import Optional

sys.path.insert(0, os.path.dirname(__file__))

from database import get_pool
from Model.ClientSubsystem.Cliente import Cliente
from Model.ClientSubsystem.ClienteDAO import ClienteDAO
from Model.ClientSubsystem.Trotinete import Trotinete
from Model.ClientSubsystem.TrotineteDAO import TrotineteDAO
from Model.StockSubsystem.Peca import Peca
from Model.StockSubsystem.PecaDAO import PecaDAO
from Model.RepairSubsystem.OrdemDeServico import OrdemDeServico
from Model.RepairSubsystem.OrdemDeServicoDAO import OrdemDeServicoDAO
from Model.RepairSubsystem.Diagnostico import Diagnostico
from Model.RepairSubsystem.DiagnosticoDAO import DiagnosticoDAO
from Model.RepairSubsystem.Intervencao import Intervencao
from Model.RepairSubsystem.IntervencaoDAO import IntervencaoDAO
from Model.PaymentsSubsystem.Fatura import Fatura
from Model.PaymentsSubsystem.FaturaDAO import FaturaDAO
from Model.SecuritySubsystem.Utilizador import Utilizador
from Model.SecuritySubsystem.UtilizadorDAO import UtilizadorDAO

SEED_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "seed-data.json")
)

PERFIS_Permissoes = {
    "administrador": [
        "lerUtilizador", "criarUtilizador", "editarUtilizador", "desativarUtilizador",
        "lerCliente", "criarCliente", "editarCliente", "removerCliente",
        "lerTrotinete", "criarTrotinete", "editarTrotinete", "removerTrotinete",
        "lerOS", "criarOS", "editarOS",
        "lerPeca", "criarPeca", "editarPeca",
        "lerRelatorio",
        "lerFatura", "pagarFatura",
    ],
    "gestor": [
        "lerUtilizador", "criarUtilizador", "editarUtilizador", "desativarUtilizador",
        "lerCliente", "criarCliente", "editarCliente", "removerCliente",
        "lerTrotinete", "criarTrotinete", "editarTrotinete", "removerTrotinete",
        "lerOS", "criarOS", "editarOS",
        "lerPeca", "criarPeca", "editarPeca",
        "lerRelatorio",
        "lerFatura",
    ],
    "tecnico": [
        "lerUtilizador",
        "lerCliente",
        "lerTrotinete",
        "lerOS", "editarOS",
        "lerPeca",
    ],
    "secretaria": [
        "lerCliente", "criarCliente", "editarCliente", "removerCliente",
        "lerTrotinete", "criarTrotinete", "editarTrotinete", "removerTrotinete",
        "lerOS", "criarOS",
        "lerPeca",
        "lerFatura",
    ],
}


def parse_date(d: Optional[str]) -> Optional[date]:
    if not d:
        return None
    return datetime.strptime(d, "%d/%m/%Y").date()


def seed_perfis_permissoes(conn):
    count = 0
    with conn.cursor() as cursor:
        for perfil, permissoes in PERFIS_Permissoes.items():
            for permissao in permissoes:
                cursor.execute(
                    "INSERT IGNORE INTO perfis_permissoes (perfil, permissao, ativo) VALUES (%s, %s, TRUE)",
                    (perfil, permissao),
                )
                count += cursor.rowcount
        conn.commit()
    print(f"  perfis_permissoes: {count} novas linhas")


def seed_utilizadores(conn):
    default_users = [
        ("Admin", "admin", "admin123", "administrador"),
        ("Gestor", "gestor", "gestor123", "gestor"),
        ("Técnico", "tecnico", "tecnico123", "tecnico"),
        ("Secretária", "secretaria", "secretaria123", "secretaria"),
    ]
    dao = UtilizadorDAO(conn)
    count = 0
    for nome, username, password, perfil in default_users:
        existing = dao.consultar_por_username(username)
        if existing:
            continue
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)
        user = Utilizador(
            id=0,
            nome=nome,
            username=username,
            password_hash=password_hash.decode(),
            password_salt=salt.decode(),
            perfil=perfil,
            ativo=True,
            data_registo=date.today(),
        )
        dao.inserir(user, salt)
        count += 1
    print(f"  utilizadores: {count} novos")


def seed_pecas(conn, data: list[dict]):
    dao = PecaDAO(conn)
    count = 0
    for item in data:
        peca = Peca(
            id=item["id"],
            nome=item["nome"],
            descricao=item.get("descricao", ""),
            fornecedor=item.get("fornecedor", ""),
            categoria=item.get("categoria", ""),
            preco=item["precoUnitario"],
            stock=item.get("stockDisponivel", item.get("stockTotal", 0)),
            quantidade_minima=item.get("stockMinimo", 0),
        )
        existing = dao.consultar_por_id(item["id"])
        if existing:
            continue
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO pecas (id, nome, descricao, fornecedor, categoria, preco, stock, quantidade_minima)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    peca.id, peca.nome, peca.descricao, peca.fornecedor,
                    peca.categoria, peca.preco, peca.stock, peca.quantidade_minima,
                ),
            )
            conn.commit()
        count += 1
    print(f"  pecas: {count} novas")


def seed_clientes(conn, data: list[dict]):
    dao = ClienteDAO(conn)
    count = 0
    for item in data:
        cliente = Cliente(
            id=item["id"],
            nome=item["nome"],
            nif=item["nif"],
            contacto=item.get("telefone"),
            email=item.get("email"),
            morada=item.get("morada"),
        )
        if dao.criarCliente(cliente):
            count += 1
    print(f"  clientes: {count} novos")


def seed_trotinetes(conn, data: list[dict]):
    dao = TrotineteDAO(conn)
    count = 0
    for item in data:
        trotinete = Trotinete(
            id=item["id"],
            marca=item["marca"],
            modelo=item["modelo"],
            numero_serie=item["serie"],
            data_registo=parse_date(item["registado"]),
            id_cliente=item["clienteId"],
        )
        existing = dao.consultarTrotinete(item["id"])
        if existing:
            continue
        if dao.criarTrotinete(trotinete):
            count += 1
    print(f"  trotinetes: {count} novas")


def seed_ordens_servico(conn, data: list[dict]):
    os_dao = OrdemDeServicoDAO(conn)
    diag_dao = DiagnosticoDAO(conn)
    inter_dao = IntervencaoDAO(conn)
    os_count = diag_count = inter_count = 0
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM trotinetes LIMIT 1")
        row = cursor.fetchone()
        id_trotinete = row[0] if row else 1
        cursor.execute("SELECT id FROM clientes LIMIT 1")
        row = cursor.fetchone()
        id_cliente = row[0] if row else 1
        cursor.execute("SELECT id FROM utilizadores WHERE perfil = 'tecnico' LIMIT 1")
        row = cursor.fetchone()
        id_tecnico = row[0] if row else 3
    for item in data:
        existing = os_dao.consultar_por_id(item["id"])
        if existing:
            continue
        os_obj = OrdemDeServico(
            id=item["id"],
            data_abertura=datetime.now(),
            data_conclusao=None,
            estado=item.get("estado", "Aguarda Diagnóstico"),
            descricao=item["descricao"],
            id_trotinete=id_trotinete,
            id_tecnico=id_tecnico,
            id_cliente=id_cliente,
        )
        os_id = os_dao.inserir(os_obj)
        os_count += 1
        diag_data = item.get("diagnostico")
        if diag_data:
            pecas = {}
            for p in diag_data.get("pecas", []):
                pecas[p["id"]] = {"quantidade": p.get("quantidade", 1), "preco_unitario": p.get("preco_unitario", 0)}
            diagnostico = Diagnostico(
                id=-1,
                descricao=diag_data["descricao"],
                orcamento_estimado=float(diag_data.get("custo", 0)),
                horas_mao_de_obra=float(diag_data.get("tempo_estimado", 0)),
                data=parse_date(diag_data.get("data_diagnostico", "")),
                id_os=os_id,
                id_tecnico=3,
                decisao_cliente="Indefinido",
                pecas=pecas,
            )
            diag_dao.inserir(diagnostico)
            diag_count += 1
        for iv in item.get("intervencoes", []):
            pecas = {}
            for p in iv.get("pecas", []):
                pecas[p["id"]] = {"quantidade": p.get("quantidade", 1), "preco_unitario": p.get("preco_unitario", 0)}
            intervencao = Intervencao(
                id=-1,
                descricao=iv["descricao"],
                horas_trabalhadas=float(iv.get("tempo", 0)) / 60.0,
                data=parse_date(iv.get("data", "")),
                id_os=os_id,
                id_tecnico=3,
                custo_total=0.0,
                pecas_usadas=pecas,
            )
            inter_dao.inserir(intervencao)
            inter_count += 1
    print(f"  ordens_servico: {os_count} novas, diagnosticos: {diag_count}, intervencoes: {inter_count}")


def seed_faturas(conn, data: list[dict]):
    dao = FaturaDAO(conn)
    count = 0
    for item in data:
        existing = dao.consultar_por_id(item["id"])
        if existing:
            continue
        pecas = {}
        for it in item.get("itens", []):
            peca_id = it.get("pecaId")
            if peca_id is None:
                continue
            pecas[peca_id] = {
                "nome": it.get("descricao", ""),
                "quantidade": it.get("qty", 1),
                "preco_unitario": float(it.get("preco", 0)),
            }
        estado = "paga" if item.get("estado") == "Paga" else "pendente"
        fatura = Fatura(
            id=item["id"],
            numero=item["numero"],
            data=parse_date(item["emissao"]),
            sub_total_pecas=float(item.get("subtotal", 0)),
            sub_total_mao_obra=float(item.get("subtotal_mao_obra", 0)),
            total=float(item["total"]),
            estado=estado,
            tipo_pagamento="transferência",
            id_os=item.get("ordemId", 1),
            pecas=pecas,
        )
        dao.inserir(fatura)
        count += 1
    print(f"  faturas: {count} novas")


VALID_TABLES = {
    "fatura_peca", "fatura",
    "intervencao_peca", "intervencoes",
    "diagnostico_peca", "diagnostico",
    "ordem_de_servico",
    "trotinetes", "clientes",
    "pecas",
    "perfis_permissoes", "utilizadores",
}

def truncate_all(conn):
    with conn.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for table in VALID_TABLES:
            cursor.execute(f"TRUNCATE TABLE {table}")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
    print("  todas as tabelas truncadas")


def load_data():
    if not os.path.exists(SEED_FILE):
        print(f"AVISO: ficheiro seed não encontrado: {SEED_FILE}")
        return {}

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_if_empty():
    """Seed the database only if tables are empty. Safe to call on every startup."""
    pool = get_pool()
    conn = pool.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM clientes")
            if cursor.fetchone()[0] > 0:
                return

        data = load_data()
        if not data:
            return

        print("[seed] A semear base de dados...")
        seed_perfis_permissoes(conn)
        seed_utilizadores(conn)
        seed_pecas(conn, data.get("pecas", []))
        seed_clientes(conn, data.get("clientes", []))
        seed_trotinetes(conn, data.get("equipamentos", []))
        seed_ordens_servico(conn, data.get("ordensServico", []))
        seed_faturas(conn, data.get("faturas", []))
        print("[seed] Seed concluído!")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Carrega seed-data.json na base de dados")
    parser.add_argument("--reset", action="store_true", help="Trunca todas as tabelas antes de semear")
    parser.add_argument("--truncate-only", action="store_true", help="Apenas trunca todas as tabelas (nao semeia)")
    args = parser.parse_args()

    pool = get_pool()
    conn = pool.get_connection()

    try:
        if args.reset or args.truncate_only:
            print("A truncar dados existentes...")
            truncate_all(conn)
            if args.truncate_only:
                print("\nTabelas truncadas com sucesso!")
                return

        data = load_data()
        if not data:
            sys.exit(1)

        print("A semear perfis_permissoes...")
        seed_perfis_permissoes(conn)

        print("A semear utilizadores...")
        seed_utilizadores(conn)

        print("A semear pecas...")
        seed_pecas(conn, data.get("pecas", []))

        print("A semear clientes...")
        seed_clientes(conn, data.get("clientes", []))

        print("A semear trotinetes...")
        seed_trotinetes(conn, data.get("equipamentos", []))

        print("A semear ordens de serviço...")
        seed_ordens_servico(conn, data.get("ordensServico", []))

        print("A semear faturas...")
        seed_faturas(conn, data.get("faturas", []))

        print("\nSeed concluído com sucesso!")

    except Exception as e:
        conn.rollback()
        print(f"ERRO: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
