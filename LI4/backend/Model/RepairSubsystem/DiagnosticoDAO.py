from typing import List, Optional
from Model.RepairSubsystem.Diagnostico import Diagnostico
import mysql.connector


class DiagnosticoDAO:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    # --------- CREATE ---------
    def inserir(self, diagnostico: Diagnostico) -> int:
        """
        Insere um novo diagnóstico e as suas peças associadas.
        Usa transação para garantir consistência entre as duas tabelas.
        """
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        cursor = self.db_conn.cursor()
        try:
            # 1. Inserir o diagnóstico principal
            query_diag = """
                INSERT INTO diagnostico 
                    (descricao, orcamentoEstimado, horasMaoDeObra, data,
                     decisaoCliente, dataDecisao, idOS, idTecnico)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_diag, (
                diagnostico.descricao,
                diagnostico.orcamento_estimado,
                diagnostico.horas_mao_de_obra,
                diagnostico.data,
                diagnostico.decisao_cliente,
                diagnostico.data_decisao,
                diagnostico.id_os,
                diagnostico.id_tecnico
            ))
            novo_id = cursor.lastrowid

            # 2. Inserir as peças associadas
            # pecas esperado: {id_peca: {"quantidade": int, "preco_unitario": float}}
            self._inserir_pecas(cursor, novo_id, diagnostico.pecas)

            self.db_conn.commit()
            return novo_id

        except Exception:
            self.db_conn.rollback()
            raise
        finally:
            cursor.close()

    # --------- READ (BY ID) ---------
    def consultar_por_id(self, id: int) -> Optional[Diagnostico]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM diagnostico WHERE id = %s", (id,))
            row = cursor.fetchone()
            if not row:
                return None

            pecas = self._get_pecas(cursor, id)
            return self._map_row_to_obj(row, pecas)
        finally:
            cursor.close()

    # --------- READ (BY OS ID) ---------
    def consultar_por_os(self, id_os: int) -> Optional[Diagnostico]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM diagnostico WHERE idOS = %s"
            cursor.execute(query, (id_os,))
            row = cursor.fetchone()
            
            # ✅ Consumir quaisquer resultados pendentes antes de fechar
            cursor.fetchall()

            if not row:
                return None

            # ✅ Cursor separado para as peças
            cursor_pecas = self.db_conn.cursor(dictionary=True)
            try:
                pecas = self._get_pecas(cursor_pecas, row['id'])
            finally:
                cursor_pecas.close()

            return self._map_row_to_obj(row, pecas)

        except Exception as e:
            print(f"Erro ao consultar diagnóstico por OS: {e}")
            return None
        finally:
            cursor.close()

    # --------- READ (ALL) ---------
    def listar(self) -> List[Diagnostico]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM diagnostico")
            rows = cursor.fetchall()  # ✅ fetchall() aqui já consome tudo
            result = []
            for row in rows:
                # ✅ Cursor separado por iteração
                cursor_pecas = self.db_conn.cursor(dictionary=True)
                try:
                    pecas = self._get_pecas(cursor_pecas, row['id'])
                finally:
                    cursor_pecas.close()
                result.append(self._map_row_to_obj(row, pecas))
            return result
        finally:
            cursor.close()

    # --------- UPDATE ---------
    def atualizar(self, diagnostico: Diagnostico) -> bool:
        """
        Atualiza o diagnóstico e substitui todas as peças associadas.
        """
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(
                "SELECT id FROM diagnostico WHERE id = %s FOR UPDATE",
                (diagnostico.id,)
            )
            if cursor.fetchone() is None:
                self.db_conn.rollback()
                return False

            query_diag = """
                UPDATE diagnostico
                SET descricao=%s, orcamentoEstimado=%s, horasMaoDeObra=%s, data=%s,
                    decisaoCliente=%s, dataDecisao=%s, idOS=%s, idTecnico=%s
                WHERE id=%s
            """
            cursor.execute(query_diag, (
                diagnostico.descricao,
                diagnostico.orcamento_estimado,
                diagnostico.horas_mao_de_obra,
                diagnostico.data,
                diagnostico.decisao_cliente,
                diagnostico.data_decisao,
                diagnostico.id_os,
                diagnostico.id_tecnico,
                diagnostico.id
            ))

            # Substituir peças: apagar as antigas e reinserir
            cursor.execute(
                "DELETE FROM diagnostico_peca WHERE idDiagnostico = %s",
                (diagnostico.id,)
            )
            self._inserir_pecas(cursor, diagnostico.id, diagnostico.pecas)

            self.db_conn.commit()
            return cursor.rowcount > 0

        except Exception:
            self.db_conn.rollback()
            raise
        finally:
            cursor.close()

    # --------- DELETE ---------
    def remover(self, id: int) -> bool:
        """
        Apaga o diagnóstico. As peças são removidas em cascata pelo FK ON DELETE CASCADE.
        """
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        cursor = self.db_conn.cursor()
        try:
            # Lock antes de apagar
            cursor.execute(
                "SELECT id FROM diagnostico WHERE id = %s FOR UPDATE",
                (id,)
            )
            cursor.execute("DELETE FROM diagnostico WHERE id = %s", (id,))
            self.db_conn.commit()
            return cursor.rowcount > 0

        except Exception:
            self.db_conn.rollback()
            raise
        finally:
            cursor.close()

    # --------- AUXILIARES PRIVADOS ---------

    def _inserir_pecas(self, cursor, id_diagnostico: int, pecas: dict):
        """
        Insere as peças de um diagnóstico na tabela diagnostico_peca.
        pecas: {id_peca: {"quantidade": int, "preco_unitario": float}}
        """
        if not pecas:
            return

        query = """
            INSERT INTO diagnostico_peca (idDiagnostico, idPeca, quantidade, precoUnitario)
            VALUES (%s, %s, %s, %s)
        """
        rows = [
            (id_diagnostico, id_peca, info["quantidade"], info["preco_unitario"])
            for id_peca, info in pecas.items()
        ]
        cursor.executemany(query, rows)


    def _get_pecas(self, cursor, id_diagnostico: int) -> dict:
        """
        Lê as peças associadas a um diagnóstico.
        Devolve: {id_peca: {"quantidade": int, "preco_unitario": float}}
        """
        cursor.execute(
            """
            SELECT idPeca, quantidade, precoUnitario
            FROM diagnostico_peca
            WHERE idDiagnostico = %s
            """,
            (id_diagnostico,)
        )
        rows = cursor.fetchall()

        # Suporta tanto cursor dictionary=True como tuplos
        pecas = {}
        for row in rows:
            if isinstance(row, dict):
                pecas[row['idPeca']] = {
                    "quantidade": row['quantidade'],
                    "preco_unitario": float(row['precoUnitario'])
                }
            else:
                id_peca, quantidade, preco_unitario = row
                pecas[id_peca] = {
                    "quantidade": quantidade,
                    "preco_unitario": float(preco_unitario)
                }
        return pecas

    def _map_row_to_obj(self, row: dict, pecas: dict) -> Diagnostico:
        """Converte uma linha do BD num objeto Diagnostico."""
        return Diagnostico(
            id=row['id'],
            descricao=row['descricao'],
            orcamento_estimado=float(row['orcamentoEstimado']) if row['orcamentoEstimado'] is not None else 0.0,
            horas_mao_de_obra=float(row['horasMaoDeObra']) if row['horasMaoDeObra'] is not None else 0.0,
            data=row['data'],
            id_os=row['idOS'],
            id_tecnico=row['idTecnico'],
            decisao_cliente=row.get('decisaoCliente', 'Indefinido'),
            data_decisao=row.get('dataDecisao'),
            pecas=pecas
        )