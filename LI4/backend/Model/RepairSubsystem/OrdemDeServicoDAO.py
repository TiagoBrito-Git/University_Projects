from Model.RepairSubsystem.OrdemDeServico import OrdemDeServico
from typing import Callable, List, Optional
import mysql.connector
from datetime import datetime

class OrdemDeServicoDAO:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    # --------- CREATE ---------
    def inserir(self, os:OrdemDeServico) -> int:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        query = """
        INSERT INTO ordem_de_servico
        (data_abertura, data_conclusao, estado, descricao, id_trotinete, id_tecnico, id_cliente)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor = self.db_conn.cursor()
        try:
            cursor.execute(query, (
                os.data_abertura,
                os.data_conclusao,
                os.estado,
                os.descricao,
                os.id_trotinete,
                os.id_tecnico,
                os.id_cliente,
            ))
            self.db_conn.commit()
            return cursor.lastrowid
        except Exception as e:
            self.db_conn.rollback()
            raise e
        finally:
            cursor.close()

    # --------- READ (ALL) ---------
    def listar(self) -> List[OrdemDeServico]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM ordem_de_servico"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            return [
                OrdemDeServico(
                    id=r['id'],
                    data_abertura=r['data_abertura'],
                    data_conclusao=r['data_conclusao'],
                    estado=r['estado'],
                    descricao=r['descricao'],
                    id_trotinete=r['id_trotinete'],
                    id_tecnico=r['id_tecnico'],
                    id_cliente=r['id_cliente']
                ) for r in rows
            ]
        finally:
            cursor.close()

    # --------- UPDATE ---------
    def atualizar(self, ordem: OrdemDeServico) -> bool:
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
                    "SELECT id FROM ordem_de_servico WHERE id = %s FOR UPDATE",
                    (ordem.id,)
                )
                if cursor.fetchone() is None:
                    self.db_conn.rollback()
                    return False

                cursor.execute("""
                    UPDATE ordem_de_servico
                    SET data_abertura=%s,
                        data_conclusao=%s,
                        estado=%s,
                        descricao=%s,
                        id_trotinete=%s,
                        id_tecnico=%s,
                        id_cliente=%s
                    WHERE id=%s
                """, (
                    ordem.data_abertura,
                    ordem.data_conclusao,
                    ordem.estado,
                    ordem.descricao,
                    ordem.id_trotinete,
                    ordem.id_tecnico,
                    ordem.id_cliente,
                    ordem.id,
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

    # --------- ALTERAR ESTADO (atómico, com gestão de transação) ---------
    def alterar_estado(self, id: int, validar_fn: Callable[[OrdemDeServico], Optional[str]]) -> bool:
        """SELECT FOR UPDATE → validar → UPDATE, tudo numa transação. Retry em deadlock."""
        # Limpa qualquer transação implícita pendente (ex: SELECT feito por outro dependency na mesma conexão)
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        tentativas = 3
        for tentativa in range(tentativas):
            cursor = self.db_conn.cursor(dictionary=True)
            try:
                self.db_conn.start_transaction()
                cursor.execute(
                    "SELECT * FROM ordem_de_servico WHERE id = %s FOR UPDATE",
                    (id,)
                )
                row = cursor.fetchone()
                if not row:
                    self.db_conn.rollback()
                    return False

                ordem = self._row_para_os(row)
                novo_estado = validar_fn(ordem)
                if novo_estado is None:
                    self.db_conn.rollback()
                    return False

                if novo_estado == "Aguarda Faturação":
                    cursor.execute(
                        "UPDATE ordem_de_servico SET estado = %s, data_conclusao = %s WHERE id = %s",
                        (novo_estado, datetime.now().date(), id)
                    )
                else:
                    cursor.execute(
                        "UPDATE ordem_de_servico SET estado = %s WHERE id = %s",
                        (novo_estado, id)
                    )
                self.db_conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.errors.DatabaseError as e:
                self.db_conn.rollback()
                if e.errno == 1213 and tentativa < tentativas - 1:
                    continue
                raise
            finally:
                cursor.close()

    # --------- ALTERAR ESTADO (sem commit — para transações geridas externamente) ---------
    def alterar_estado_sem_commit(self, id: int, validar_fn: Callable[[OrdemDeServico], Optional[str]]) -> bool:
        """SELECT FOR UPDATE → validar → UPDATE. Sem start_transaction/commit — o chamador gere a transação."""
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM ordem_de_servico WHERE id = %s FOR UPDATE",
                (id,)
            )
            row = cursor.fetchone()
            if not row:
                return False

            ordem = self._row_para_os(row)
            novo_estado = validar_fn(ordem)
            if novo_estado is None:
                return False

            if novo_estado == "Aguarda Faturação":
                cursor.execute(
                    "UPDATE ordem_de_servico SET estado = %s, data_conclusao = %s WHERE id = %s",
                    (novo_estado, datetime.now().date(), id)
                )
            else:
                cursor.execute(
                    "UPDATE ordem_de_servico SET estado = %s WHERE id = %s",
                    (novo_estado, id)
                )
            return cursor.rowcount > 0
        finally:
            cursor.close()

    # --------- AUXILIAR PRIVADO ---------
    @staticmethod
    def _row_para_os(row: dict) -> OrdemDeServico:
        return OrdemDeServico(
            id=row['id'],
            data_abertura=row['data_abertura'],
            data_conclusao=row['data_conclusao'],
            estado=row['estado'],
            descricao=row['descricao'],
            id_trotinete=row['id_trotinete'],
            id_tecnico=row['id_tecnico'],
            id_cliente=row['id_cliente'],
        )

    # --------- DELETE ---------
    def remover(self, id: int) -> bool:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        cursor = self.db_conn.cursor()
        try:
            # Lock para consistência durante a eliminação
            cursor.execute("SELECT id FROM ordem_de_servico WHERE id = %s FOR UPDATE", (id,))
            cursor.execute("DELETE FROM ordem_de_servico WHERE id = %s", (id,))
            self.db_conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_conn.rollback()
            raise e
        finally:
            cursor.close()
    


# --------- READ (BY ID) ---------
    def consultar_por_id(self, id: int) -> Optional[OrdemDeServico]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            # Seleciona a ordem de serviço específica pelo ID
            query = "SELECT * FROM ordem_de_servico WHERE id = %s"
            cursor.execute(query, (id,))
            row = cursor.fetchone()

            if row:
                return OrdemDeServico(
                    id=row['id'],
                    data_abertura=row['data_abertura'],
                    data_conclusao=row['data_conclusao'],
                    estado=row['estado'],
                    descricao=row['descricao'],
                    id_trotinete=row['id_trotinete'],
                    id_tecnico=row['id_tecnico'],
                    id_cliente=row['id_cliente']
                )
            return None
        finally:
            cursor.close()


    def contar_ordens_por_mes(self, mes: int, ano: int) -> int:
            cursor = self.db_conn.cursor()
            try:
                # Conta o número de IDs na tabela ordem_de_servico para o mês/ano
                query = """
                    SELECT COUNT(id) 
                    FROM ordem_de_servico 
                    WHERE MONTH(data_abertura) = %s 
                    AND YEAR(data_abertura) = %s
                """
                cursor.execute(query, (mes, ano))
                resultado = cursor.fetchone()
                
                return resultado[0] if resultado else 0
            finally:
                cursor.close()


    def contar_ordens_paradas_por_mes(self, mes: int, ano: int) -> int:
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(
                """
                SELECT COUNT(id) FROM ordem_de_servico
                WHERE estado = 'Cancelada'
                AND MONTH(data_abertura) = %s AND YEAR(data_abertura) = %s
                """,
                (mes, ano)
            )
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0
        finally:
            cursor.close()