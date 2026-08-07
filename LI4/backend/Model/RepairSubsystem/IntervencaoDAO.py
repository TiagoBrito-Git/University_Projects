from Model.RepairSubsystem.Intervencao import Intervencao
from typing import List, Optional
import mysql.connector


class IntervencaoDAO:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def _row_para_intervencao(self, row: dict) -> Intervencao:
        """Converte uma linha da BD num objeto Intervencao."""
        return Intervencao(
            id=row["id"],
            descricao=row["descricao"],
            horas_trabalhadas=row["horas_trabalho"],   # coluna BD: horas_trabalho
            data=row["data_"],                          # coluna BD: data_
            id_os=row["id_os"],
            id_tecnico=row["id_tecnico"],
            custo_total=row.get("custo_total", 0.0),
            pecas_usadas=row.get("pecas_usadas", {}),
        )

    # ─────────────────────────────────────────────────────────────
    # AUXILIARES PRIVADOS — intervencao_peca
    # ─────────────────────────────────────────────────────────────

    def _inserir_pecas(self, cursor, id_intervencao: int, pecas: dict) -> None:
        """
        Insere as peças de uma intervenção em intervencao_peca.

        pecas: {id_peca: {"quantidade": int, "preco_unitario": float}}
        """
        if not pecas:
            return

        query = """
            INSERT INTO intervencao_peca (idIntervencao, idPeca, quantidade, precoUnitario)
            VALUES (%s, %s, %s, %s)
        """
        rows = [
            (id_intervencao, id_peca, info["quantidade"], info["preco_unitario"])
            for id_peca, info in pecas.items()
        ]
        cursor.executemany(query, rows)

    def _get_pecas(self, cursor, id_intervencao: int) -> dict:
        """
        Lê as peças associadas a uma intervenção.

        Devolve: {id_peca: {"quantidade": int, "preco_unitario": float}}
        """
        cursor.execute(
            """
            SELECT idPeca, quantidade, precoUnitario
            FROM intervencao_peca
            WHERE idIntervencao = %s
            """,
            (id_intervencao,)
        )
        pecas = {}
        for row in cursor.fetchall():
            if isinstance(row, dict):
                pecas[row["idPeca"]] = {
                    "quantidade": row["quantidade"],
                    "preco_unitario": float(row["precoUnitario"]),
                }
            else:
                id_peca, quantidade, preco_unitario = row
                pecas[id_peca] = {
                    "quantidade": quantidade,
                    "preco_unitario": float(preco_unitario),
                }
        return pecas

    # ─────────────────────────────────────────────────────────────
    # INSERIR
    # ─────────────────────────────────────────────────────────────

    def inserir(self, intervencao: Intervencao) -> int:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        cursor = self.db_conn.cursor()
        query = """
            INSERT INTO intervencoes
                (descricao, horas_trabalho, data_, custo_total, id_os, id_tecnico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            # 1. Inserir a intervenção principal
            cursor.execute(query, (
                intervencao.descricao,
                intervencao.horas_trabalhadas,
                intervencao.data,
                intervencao.custo_total,
                intervencao.id_os,
                intervencao.id_tecnico,
            ))
            novo_id = cursor.lastrowid

            # 2. Inserir as peças associadas em intervencao_peca
            self._inserir_pecas(cursor, novo_id, intervencao.pecas_usadas)

            self.db_conn.commit()
            return novo_id

        except Exception:
            self.db_conn.rollback()
            raise
        finally:
            cursor.close()

    def inserir_sem_commit(self, intervencao: Intervencao, cursor) -> int:
        """Insere uma intervenção usando um cursor externo, sem gerir a transação."""
        cursor.execute(
            """
            INSERT INTO intervencoes
                (descricao, horas_trabalho, data_, custo_total, id_os, id_tecnico)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                intervencao.descricao,
                intervencao.horas_trabalhadas,
                intervencao.data,
                intervencao.custo_total,
                intervencao.id_os,
                intervencao.id_tecnico,
            ),
        )
        novo_id = cursor.lastrowid
        self._inserir_pecas(cursor, novo_id, intervencao.pecas_usadas)
        return novo_id

    # ─────────────────────────────────────────────────────────────
    # CONSULTAR POR ID
    # ─────────────────────────────────────────────────────────────

    def consultar_por_id(self, intervencao_id: int) -> Optional[Intervencao]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM intervencoes WHERE id = %s",
                (intervencao_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None

            pecas = self._get_pecas(cursor, intervencao_id)
            row["pecas_usadas"] = pecas
            return self._row_para_intervencao(row)
        finally:
            cursor.close()

    # ─────────────────────────────────────────────────────────────
    # CONSULTAR TODAS
    # ─────────────────────────────────────────────────────────────

    def listar(self) -> List[Intervencao]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM intervencoes")
            rows = cursor.fetchall()
        finally:
            cursor.close()

        result = []
        for row in rows:
            cursor_pecas = self.db_conn.cursor(dictionary=True)
            try:
                pecas = self._get_pecas(cursor_pecas, row["id"])
            finally:
                cursor_pecas.close()
            row["pecas_usadas"] = pecas
            result.append(self._row_para_intervencao(row))
        return result

    # ─────────────────────────────────────────────────────────────
    # CONSULTAR POR ORDEM DE SERVIÇO
    # ─────────────────────────────────────────────────────────────

    def consultar_por_os(self, id_os: int) -> List[Intervencao]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM intervencoes WHERE id_os = %s",
                (id_os,)
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()

        result = []
        for row in rows:
            cursor_pecas = self.db_conn.cursor(dictionary=True)
            try:
                pecas = self._get_pecas(cursor_pecas, row["id"])
            finally:
                cursor_pecas.close()
            row["pecas_usadas"] = pecas
            result.append(self._row_para_intervencao(row))
        return result

    # ─────────────────────────────────────────────────────────────
    # ATUALIZAR (COM LOCK)
    # ─────────────────────────────────────────────────────────────

    def atualizar(self, intervencao: Intervencao) -> bool:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        tentativas = 3
        for tentativa in range(tentativas):
            cursor = self.db_conn.cursor()
            try:
                self.db_conn.start_transaction()

                cursor.execute(
                    "SELECT id FROM intervencoes WHERE id = %s FOR UPDATE",
                    (intervencao.id,)
                )
                if cursor.fetchone() is None:
                    self.db_conn.rollback()
                    return False

                cursor.execute("""
                    UPDATE intervencoes SET
                        descricao      = %s,
                        horas_trabalho = %s,
                        data_          = %s,
                        id_os          = %s,
                        id_tecnico     = %s,
                        custo_total    = %s
                    WHERE id = %s
                """, (
                    intervencao.descricao,
                    intervencao.horas_trabalhadas,
                    intervencao.data,
                    intervencao.id_os,
                    intervencao.id_tecnico,
                    intervencao.custo_total,
                    intervencao.id,
                ))

                # Substituir peças: apagar as antigas e reinserir
                cursor.execute(
                    "DELETE FROM intervencao_peca WHERE idIntervencao = %s",
                    (intervencao.id,)
                )
                self._inserir_pecas(cursor, intervencao.id, intervencao.pecas_usadas)

                self.db_conn.commit()
                return cursor.rowcount > 0

            except mysql.connector.errors.DatabaseError as e:
                self.db_conn.rollback()
                if e.errno == 1213 and tentativa < tentativas - 1:
                    continue  # retry em caso de deadlock
                raise
            finally:
                cursor.close()

    # ─────────────────────────────────────────────────────────────
    # REMOVER (COM LOCK)
    # As peças são removidas em cascata pelo FK ON DELETE CASCADE
    # ─────────────────────────────────────────────────────────────

    def remover(self, intervencao_id: int) -> bool:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        tentativas = 3
        for tentativa in range(tentativas):
            cursor = self.db_conn.cursor()
            try:
                self.db_conn.start_transaction()

                cursor.execute(
                    "SELECT id FROM intervencoes WHERE id = %s FOR UPDATE",
                    (intervencao_id,)
                )
                if cursor.fetchone() is None:
                    self.db_conn.rollback()
                    return False

                cursor.execute(
                    "DELETE FROM intervencoes WHERE id = %s",
                    (intervencao_id,)
                )
                self.db_conn.commit()
                return cursor.rowcount > 0

            except mysql.connector.errors.DatabaseError as e:
                self.db_conn.rollback()
                if e.errno == 1213 and tentativa < tentativas - 1:
                    continue  # retry em caso de deadlock
                raise
            finally:
                cursor.close()

    def consultar_por_mes(self, mes: int, ano: int) -> List[Intervencao]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT * FROM intervencoes
                WHERE MONTH(data_) = %s AND YEAR(data_) = %s
                """,
                (mes, ano)
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()

        result = []
        for row in rows:
            cursor_pecas = self.db_conn.cursor(dictionary=True)
            try:
                pecas = self._get_pecas(cursor_pecas, row["id"])
            finally:
                cursor_pecas.close()
            row["pecas_usadas"] = pecas
            result.append(self._row_para_intervencao(row))
        return result


    def tempo_medio_por_mes(self, mes: int, ano: int) -> float:
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(
                """
                SELECT AVG(horas_trabalho) FROM intervencoes
                WHERE MONTH(data_) = %s AND YEAR(data_) = %s
                """,
                (mes, ano)
            )
            resultado = cursor.fetchone()[0]
            return float(resultado) if resultado else 0.0
        finally:
            cursor.close()