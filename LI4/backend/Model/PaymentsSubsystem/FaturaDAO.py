import mysql.connector
from Model.PaymentsSubsystem.Fatura import Fatura
 
 
class FaturaDAO:
    def __init__(self, db_connection):
        self.db = db_connection
 
    # ------------------------------------------------------------------ #
    # GET ALL                                                              #
    # ------------------------------------------------------------------ #
    def listar(self) -> list[Fatura]:
        cursor = self.db.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT f.*,
                       c.nome   AS nome_cliente,
                       c.nif    AS nif_cliente,
                       c.email  AS email_cliente,
                       c.morada AS morada_cliente
                FROM fatura f
                JOIN ordem_de_servico os ON os.id = f.id_os
                JOIN clientes c          ON c.id  = os.id_cliente
            """)
            rows = cursor.fetchall()
            if not rows:
                return []

            ids = [r["id"] for r in rows]
            fmt = ",".join(["%s"] * len(ids))
            cursor.execute(f"""
                SELECT fp.id_fatura, fp.id_peca, p.nome, fp.quantidade, fp.preco_unitario
                FROM fatura_peca fp
                JOIN pecas p ON p.id = fp.id_peca
                WHERE fp.id_fatura IN ({fmt})
            """, ids)
            pecas_rows = cursor.fetchall()
        finally:
            cursor.close()

        pecas_por_fatura: dict = {}
        for pr in pecas_rows:
            fid = pr["id_fatura"]
            pecas_por_fatura.setdefault(fid, {})[pr["id_peca"]] = {
                "nome": pr["nome"],
                "quantidade": pr["quantidade"],
                "preco_unitario": float(pr["preco_unitario"]),
            }

        faturas = []
        for r in rows:
            fid = r["id"]
            f = Fatura(
                id=fid,
                numero=r["numero"],
                data=r["data_emissao"],
                sub_total_pecas=float(r["subtotal_pecas"]),
                sub_total_mao_obra=float(r["subtotal_mao_obra"]),
                total=float(r["total"]),
                estado=r["estado"],
                tipo_pagamento=r["tipo_pagamento"],
                id_os=r["id_os"],
                pecas=pecas_por_fatura.get(fid, {}),
                nome_cliente=r.get("nome_cliente"),
                nif_cliente=r.get("nif_cliente"),
                email_cliente=r.get("email_cliente"),
                morada_cliente=r.get("morada_cliente"),
            )
            faturas.append(f)
        return faturas
 
    # ------------------------------------------------------------------ #
    # GET BY ID                                                            #
    # ------------------------------------------------------------------ #
    def consultar_por_id(self, id_fatura: int) -> Fatura | None:
        cursor = self.db.cursor(dictionary=True)
        try:
            # 1. Dados principais da fatura
            cursor.execute("SELECT * FROM fatura WHERE id = %s", (id_fatura,))
            f_row = cursor.fetchone()
            if not f_row:
                return None
 
            # 2. Linhas de peças — junta com a tabela pecas para obter o nome
            #    Estrutura resultante: {id_peca: {nome, quantidade, preco_unitario}}
            cursor.execute("""
                SELECT
                    fp.id_peca,
                    p.nome,
                    fp.quantidade,
                    fp.preco_unitario
                FROM fatura_peca fp
                JOIN pecas p ON p.id = fp.id_peca
                WHERE fp.id_fatura = %s
            """, (id_fatura,))
            linhas = cursor.fetchall()
 
            pecas_dict = {
                l["id_peca"]: {
                    "nome":            l["nome"],
                    "quantidade":      l["quantidade"],
                    "preco_unitario":  float(l["preco_unitario"]),
                }
                for l in linhas
            }
 
            return Fatura(
                id=f_row["id"],
                numero=f_row["numero"],
                data=f_row["data_emissao"],          # nome correto da coluna
                sub_total_pecas=float(f_row["subtotal_pecas"]),
                sub_total_mao_obra=float(f_row["subtotal_mao_obra"]),
                total=float(f_row["total"]),
                estado=f_row["estado"],              # setter já normaliza para minúsculas
                tipo_pagamento=f_row["tipo_pagamento"],
                id_os=f_row["id_os"],
                pecas=pecas_dict,
            )
        finally:
            cursor.close()
 
    # ------------------------------------------------------------------ #
    # CREATE                                                               #
    # ------------------------------------------------------------------ #
    def inserir(self, fatura: Fatura) -> int:
        try:
            self.db.rollback()
        except Exception:
            pass
        cursor = self.db.cursor()
        try:
            # 1. Inserir a fatura principal
            cursor.execute("""
                INSERT INTO fatura
                    (numero, data_emissao, subtotal_pecas, subtotal_mao_obra,
                     total, estado, tipo_pagamento, id_os)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                fatura.numero,
                fatura.data,
                fatura.sub_total_pecas,
                fatura.sub_total_mao_obra,
                fatura.total,
                fatura.estado,
                fatura.tipo_pagamento,
                fatura.id_os,
            ))
            novo_id = cursor.lastrowid
 
            # 2. Inserir as linhas de peças em fatura_peca
            #    fatura.pecas = {id_peca: {nome, quantidade, preco_unitario}}
            for id_peca, dados in fatura.pecas.items():
                cursor.execute("""
                    INSERT INTO fatura_peca (id_fatura, id_peca, quantidade, preco_unitario)
                    VALUES (%s, %s, %s, %s)
                """, (
                    novo_id,
                    id_peca,
                    dados["quantidade"],
                    dados["preco_unitario"],
                ))
 
            self.db.commit()
            return novo_id
 
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()
 
    # ------------------------------------------------------------------ #
    # CREATE (sem commit — para transações geridas externamente)           #
    # ------------------------------------------------------------------ #
    def inserir_em_transacao(self, fatura: Fatura) -> int:
        """Insere a fatura e as suas peças sem commit. O chamador gere a transação."""
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                INSERT INTO fatura
                    (numero, data_emissao, subtotal_pecas, subtotal_mao_obra,
                     total, estado, tipo_pagamento, id_os)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                fatura.numero,
                fatura.data,
                fatura.sub_total_pecas,
                fatura.sub_total_mao_obra,
                fatura.total,
                fatura.estado,
                fatura.tipo_pagamento,
                fatura.id_os,
            ))
            novo_id = cursor.lastrowid

            for id_peca, dados in fatura.pecas.items():
                cursor.execute("""
                    INSERT INTO fatura_peca (id_fatura, id_peca, quantidade, preco_unitario)
                    VALUES (%s, %s, %s, %s)
                """, (
                    novo_id,
                    id_peca,
                    dados["quantidade"],
                    dados["preco_unitario"],
                ))

            return novo_id
        finally:
            cursor.close()

    def obter_lucro_mes(self, mes: int, ano: int) -> float:
        cursor = self.db.cursor()
        try:
            query = """
                SELECT SUM(total) 
                FROM fatura 
                WHERE estado = 'paga' 
                  AND MONTH(data_emissao) = %s 
                  AND YEAR(data_emissao) = %s
            """
            cursor.execute(query, (mes, ano))
            resultado = cursor.fetchone()
            
            return float(resultado[0]) if resultado and resultado[0] else 0.0
        finally:
            cursor.close()