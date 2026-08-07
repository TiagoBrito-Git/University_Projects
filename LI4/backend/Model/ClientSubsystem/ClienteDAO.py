from typing import Optional, List
from mysql.connector import Error

from .Cliente import Cliente


class ClienteDAO:
    """
    Data Access Object para Cliente.
    Usa uma ligação à base de dados injetada (FastAPI Depends).
    """

    def __init__(self, db):
        self.db = db

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def criarCliente(self, cliente: Cliente) -> bool:
        """Insere um cliente. False se o NIF já existir."""
        sql = """
            INSERT INTO clientes (id, nome, nif, contacto, email, morada)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            cliente.get_id(),
            cliente.get_nome(),
            cliente.get_nif(),
            cliente.get_contacto(),
            cliente.get_email(),
            cliente.get_morada(),
        )
        try:
            self.db.rollback()
        except Exception:
            pass
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql, params)
            self.db.commit()
            return 1
        except Error as e:
            if hasattr(e, "errno") and e.errno == 1062:
                return 0
            raise RuntimeError(f"Erro ao criar cliente: {e}") from e

    def consultarCliente(self, id: str) -> Optional[Cliente]:
        """Devolve o Cliente pelo ID, ou None."""
        sql = """
            SELECT id, nome, nif, contacto, email, morada
            FROM clientes WHERE id = %s
        """
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql, (id,))
                row = cursor.fetchone()
            return self._row_para_cliente(row) if row else None
        except Error as e:
            raise RuntimeError(f"Erro ao consultar cliente: {e}") from e

    def consultarClienteNIF(self, nif: str) -> Optional[Cliente]:
        """Devolve o Cliente pelo NIF, ou None."""
        sql = """
            SELECT id, nome, nif, contacto, email, morada
            FROM clientes WHERE nif = %s
        """
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql, (nif,))
                row = cursor.fetchone()
            return self._row_para_cliente(row) if row else None
        except Error as e:
            raise RuntimeError(f"Erro ao consultar cliente: {e}") from e

    def editarCliente(self, id: int, nome: str, nif: str, contacto: str, email: str, morada: str) -> bool:
        """Atualiza dados do cliente identificado pelo ID."""
        sql = """
            UPDATE clientes
            SET nome = %s, nif = %s, contacto = %s, email = %s, morada = %s
            WHERE id = %s
        """
        try:
            self.db.rollback()
        except Exception:
            pass
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql, (nome, nif, contacto, email, morada, id))
                atualizado = cursor.rowcount > 0
            self.db.commit()
            return atualizado
        except Error as e:
            raise RuntimeError(f"Erro ao editar cliente: {e}") from e

    def tem_historico(self, id_cliente: int) -> bool:
        """Devolve True se o cliente tem ordens de serviço associadas."""
        sql = """
            SELECT 1
            FROM trotinetes t
            JOIN ordem_de_servico os ON os.id_trotinete = t.id
            WHERE t.id_cliente = %s
            LIMIT 1
        """
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql, (id_cliente,))
                return cursor.fetchone() is not None
        except Error as e:
            raise RuntimeError(f"Erro ao verificar histórico do cliente: {e}") from e

    def anonimizarCliente(self, id: int) -> bool:
        """Substitui dados pessoais por valores anónimos (RGPD). Não apaga o registo. NIF mantido para efeitos fiscais."""
        sql = """
            UPDATE clientes
            SET nome     = 'Cliente Anónimo',
                contacto = NULL,
                email    = NULL,
                morada   = NULL
            WHERE id = %s
        """
        try:
            self.db.rollback()
        except Exception:
            pass
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql, (id,))
                atualizado = cursor.rowcount > 0
            self.db.commit()
            return atualizado
        except Error as e:
            raise RuntimeError(f"Erro ao anonimizar cliente: {e}") from e

    def _exec_anonimizar(self, cursor, id: int) -> bool:
        cursor.execute(
            """UPDATE clientes
               SET nome     = 'Cliente Anónimo',
                   contacto = NULL,
                   email    = NULL,
                   morada   = NULL
               WHERE id = %s""",
            (id,),
        )
        return cursor.rowcount > 0

    def _exec_remover(self, cursor, id: int) -> bool:
        cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
        return cursor.rowcount > 0

    def listarClientes(self) -> List[Cliente]:
        """Todos os clientes, ordenados por nome."""
        sql = """
            SELECT id, nome, nif, contacto, email, morada
            FROM clientes
            ORDER BY nome
        """
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
            return [self._row_para_cliente(r) for r in rows]
        except Error as e:
            raise RuntimeError(f"Erro ao listar clientes: {e}") from e

    # ------------------------------------------------------------------
    # Auxiliar
    # ------------------------------------------------------------------

    @staticmethod
    def _row_para_cliente(row: tuple) -> Cliente:
        id_, nome, nif, contacto, email, morada = row
        return Cliente(
            id=id_,
            nome=nome,
            nif=nif,
            contacto=contacto,
            email=email,
            morada=morada
        )
