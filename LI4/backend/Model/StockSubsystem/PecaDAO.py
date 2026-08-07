from Model.StockSubsystem.Peca import Peca
from typing import List, Optional
import mysql.connector


class PecaDAO:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    # ➕ INSERIR
    def inserir(self, peca: Peca) -> int:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        cursor = self.db_conn.cursor()
        query = """
        INSERT INTO pecas
        (nome, descricao, fornecedor, categoria, preco, stock, quantidade_minima)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (
            peca.nome,
            peca.descricao,
            peca.fornecedor,
            peca.categoria,
            peca.preco,
            peca.stock,
            peca.quantidade_minima,
            ))
            self.db_conn.commit()
            return cursor.lastrowid
        except Exception:
            self.db_conn.rollback()
            raise
        finally:
            cursor.close()

    # 🔍 CONSULTAR POR ID
    def consultar_por_id(self, peca_id: int) -> Optional[Peca]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM pecas WHERE id = %s",
                (peca_id,)
            )
            row = cursor.fetchone()
            return Peca(**row) if row else None
        finally:
            cursor.close()

    # 📋 CONSULTAR TODAS
    def listar_pecas(self) -> List[Peca]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM pecas")
            return [Peca(**row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    # 🔍 CONSULTAR COM STOCK ABAIXO DO MÍNIMO
    def consultar_abaixo_minimo(self) -> List[Peca]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM pecas WHERE stock <= quantidade_minima"
            )
            return [Peca(**row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def atualizar(self, peca: Peca) -> bool:
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
                    "SELECT id FROM pecas WHERE id = %s FOR UPDATE",
                    (peca.id,)
                )
                if cursor.fetchone() is None:
                    self.db_conn.rollback()
                    return False

                cursor.execute("""
                    UPDATE pecas
                    SET nome = %s,
                        descricao = %s,
                        fornecedor = %s,
                        categoria = %s,
                        preco = %s,
                        stock = %s,
                        quantidade_minima = %s
                    WHERE id = %s
                """, (
                    peca.nome,
                    peca.descricao,
                    peca.fornecedor,
                    peca.categoria,
                    peca.preco,
                    peca.stock,
                    peca.quantidade_minima,
                    peca.id,
                ))

                self.db_conn.commit()
                return cursor.rowcount > 0

            except mysql.connector.errors.DatabaseError as e:
                self.db_conn.rollback()
                if e.errno == 1213 and tentativa < tentativas - 1:
                    continue
                raise
            finally:
                cursor.close()

    # 📦 ATUALIZAR STOCK (COM LOCK)
    def atualizar_stock(self, peca_id: int, quantidade: int) -> bool:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        tentativas = 3
        for tentativa in range(tentativas):
            cursor = self.db_conn.cursor()
            try:
                self.db_conn.start_transaction()

                # 🔒 lock da linha antes de alterar stock
                cursor.execute(
                    "SELECT stock FROM pecas WHERE id = %s FOR UPDATE",
                    (peca_id,)
                )
                row = cursor.fetchone()
                if row is None:
                    self.db_conn.rollback()
                    return False

                novo_stock = row[0] + quantidade
                if novo_stock < 0:
                    self.db_conn.rollback()
                    raise ValueError(f"Stock insuficiente (stock atual: {row[0]})")

                cursor.execute(
                    "UPDATE pecas SET stock = %s WHERE id = %s",
                    (novo_stock, peca_id)
                )
                self.db_conn.commit()
                return cursor.rowcount > 0

            except mysql.connector.errors.DatabaseError as e:
                self.db_conn.rollback()
                if e.errno == 1213 and tentativa < tentativas - 1:
                    continue  # 🔁 retry em caso de deadlock
                raise
            finally:
                cursor.close()

    # ❌ REMOVER (COM LOCK)
    def remover(self, peca_id: int) -> bool:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        tentativas = 3
        for tentativa in range(tentativas):
            cursor = self.db_conn.cursor()
            try:
                self.db_conn.start_transaction()

                # 🔒 lock da linha antes de apagar
                cursor.execute(
                    "SELECT id FROM pecas WHERE id = %s FOR UPDATE",
                    (peca_id,)
                )
                if cursor.fetchone() is None:
                    self.db_conn.rollback()
                    return False

                cursor.execute(
                    "DELETE FROM pecas WHERE id = %s",
                    (peca_id,)
                )
                self.db_conn.commit()
                return cursor.rowcount > 0

            except mysql.connector.errors.DatabaseError as e:
                self.db_conn.rollback()
                if e.errno == 1213 and tentativa < tentativas - 1:
                    continue  # 🔁 retry em caso de deadlock
                raise
            finally:
                cursor.close()