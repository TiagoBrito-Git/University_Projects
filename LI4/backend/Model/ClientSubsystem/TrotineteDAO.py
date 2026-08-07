from datetime import date
from typing import List, Optional

import mysql.connector
from mysql.connector import Error, MySQLConnection

from .Trotinete import Trotinete


class TrotineteDAO:
    """
    Data Access Object para Trotinete.
    Recebe a conexão externamente para maior flexibilidade e testabilidade.
    """

    def __init__(self, connection):
        """
        Injeta a conexão à base de dados.
        """
        self._conn = connection

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def criarTrotinete(self, trotinete: Trotinete) -> bool:
        sql = """
            INSERT INTO trotinetes (marca, modelo, numero_serie, data_registo, id_cliente)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            trotinete.get_marca(),
            trotinete.get_modelo(),
            trotinete.get_numero_serie(),
            trotinete.get_data_registo(),
            trotinete.get_id_cliente(),
        )
        try:
            self._conn.rollback()
        except Exception:
            pass
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(sql, params)
            self._conn.commit()
            return True
        except mysql.connector.IntegrityError:
            return False
        except Error as e:
            raise RuntimeError(f"Erro ao criar trotinete: {e}") from e

    def consultarTrotinete(self, id: int) -> Optional[Trotinete]:
        sql = """
            SELECT id, marca, modelo, numero_serie, data_registo, id_cliente
            FROM trotinetes WHERE id = %s
        """
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(sql, (id,))
                row = cursor.fetchone()
            return self._row_para_trotinete(row) if row else None
        except Error as e:
            raise RuntimeError(f"Erro ao consultar trotinete: {e}") from e
        

    def consultarTrotinete_numero_serie(self, numero_serie: str) -> Optional[Trotinete]:
        sql = """
            SELECT id, marca, modelo, numero_serie, data_registo, id_cliente
            FROM trotinetes WHERE numero_serie = %s
        """
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(sql, (numero_serie,))
                row = cursor.fetchone()
            return self._row_para_trotinete(row) if row else None
        except Error as e:
            raise RuntimeError(f"Erro ao consultar trotinete: {e}") from e

    def editarTrotineteById(self, id: int, marca: str, modelo: str, numero_serie: str, id_cliente: int) -> bool:
        try:
            self._conn.rollback()
        except Exception:
            pass
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE trotinetes SET marca=%s, modelo=%s, numero_serie=%s, id_cliente=%s WHERE id=%s",
                    (marca, modelo, numero_serie, id_cliente, id),
                )
                atualizado = cursor.rowcount > 0
            self._conn.commit()
            return atualizado
        except mysql.connector.IntegrityError:
            return False
        except Error as e:
            raise RuntimeError(f"Erro ao editar trotinete: {e}") from e

    def temOrdensAssociadas(self, id: int) -> bool:
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM ordem_de_servico WHERE id_trotinete=%s", (id,)
                )
                return cursor.fetchone()[0] > 0
        except Error as e:
            raise RuntimeError(f"Erro ao verificar ordens da trotinete: {e}") from e

    def removerTrotineteById(self, id: int) -> bool:
        try:
            self._conn.rollback()
        except Exception:
            pass
        try:
            with self._conn.cursor() as cursor:
                cursor.execute("DELETE FROM trotinetes WHERE id=%s", (id,))
                removido = cursor.rowcount > 0
            self._conn.commit()
            return removido
        except Error as e:
            raise RuntimeError(f"Erro ao remover trotinete: {e}") from e

    def anonimizarTrotinete(self, id: int) -> bool:
        try:
            self._conn.rollback()
        except Exception:
            pass
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE trotinetes SET numero_serie = CONCAT('ANON-', id) WHERE id=%s",
                    (id,),
                )
                atualizado = cursor.rowcount > 0
            self._conn.commit()
            return atualizado
        except Error as e:
            raise RuntimeError(f"Erro ao anonimizar trotinete: {e}") from e

    def editarTrotinete(self, numero_serie: str, marca: str, modelo: str, id_cliente: int) -> bool:
        try:
            self._conn.rollback()
        except Exception:
            pass
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE trotinetes SET marca=%s, modelo=%s, id_cliente=%s WHERE numero_serie=%s",
                    (marca, modelo, id_cliente, numero_serie),
                )
                atualizado = cursor.rowcount > 0
            self._conn.commit()
            return atualizado
        except Error as e:
            raise RuntimeError(f"Erro ao editar trotinete: {e}") from e

    def removerTrotinete(self, numero_serie: str) -> bool:
        try:
            self._conn.rollback()
        except Exception:
            pass
        try:
            with self._conn.cursor() as cursor:
                cursor.execute("DELETE FROM trotinetes WHERE numero_serie = %s", (numero_serie,))
                removido = cursor.rowcount > 0
            self._conn.commit()
            return removido
        except Error as e:
            raise RuntimeError(f"Erro ao remover trotinete: {e}") from e

    # ------------------------------------------------------------------
    # Listagens
    # ------------------------------------------------------------------

    def listarTrotinetes(self) -> List[Trotinete]:
        sql = """
            SELECT id, marca, modelo, numero_serie, data_registo, id_cliente
            FROM trotinetes ORDER BY marca, modelo
        """
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(sql)
                return [self._row_para_trotinete(r) for r in cursor.fetchall()]
        except Error as e:
            raise RuntimeError(f"Erro ao listar trotinetes: {e}") from e

    def listarTrotinetesPorCliente(self, id_cliente: int) -> List[Trotinete]:
        sql = """
            SELECT id, marca, modelo, numero_serie, data_registo, id_cliente
            FROM trotinetes WHERE id_cliente = %s ORDER BY marca, modelo
        """
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(sql, (id_cliente,))
                return [self._row_para_trotinete(r) for r in cursor.fetchall()]
        except Error as e:
            raise RuntimeError(f"Erro ao listar trotinetes por cliente: {e}") from e

    def anonimizarTrotinetesPorCliente(self, id_cliente: int) -> int:
        """Substitui o número de série por um valor anónimo (RGPD)."""
        try:
            self._conn.rollback()
        except Exception:
            pass
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE trotinetes SET numero_serie = CONCAT('ANON-', id) WHERE id_cliente = %s",
                    (id_cliente,),
                )
                atualizadas = cursor.rowcount
            self._conn.commit()
            return atualizadas
        except Error as e:
            raise RuntimeError(f"Erro ao anonimizar trotinetes: {e}") from e

    def _exec_anonimizar_por_cliente(self, cursor, id_cliente: int) -> None:
        cursor.execute(
            "UPDATE trotinetes SET numero_serie = CONCAT('ANON-', id) WHERE id_cliente = %s",
            (id_cliente,),
        )

    def _exec_remover_por_cliente(self, cursor, id_cliente: int) -> None:
        cursor.execute("DELETE FROM trotinetes WHERE id_cliente = %s", (id_cliente,))

    # ------------------------------------------------------------------
    # Auxiliar
    # ------------------------------------------------------------------

    @staticmethod
    def _row_para_trotinete(row: tuple) -> Trotinete:
        id_, marca, modelo, numero_serie, data_registo, id_cliente = row
        return Trotinete(
            id=id_,
            marca=marca,
            modelo=modelo,
            numero_serie=numero_serie,
            data_registo=data_registo if isinstance(data_registo, date)
                         else date.fromisoformat(str(data_registo)),
            id_cliente=id_cliente,
        )
    
    