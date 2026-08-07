from Model.SecuritySubsystem.Utilizador import Utilizador
from datetime import date
from typing import List, Optional
import mysql.connector


class UtilizadorDAO:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    # ── Mapeamento DB → Modelo ─────────────────────────────────────────────────
    @staticmethod
    def _row_to_utilizador(row: dict) -> Utilizador:
        """Constrói um Utilizador a partir de uma row da DB,
        mapeando explicitamente os nomes das colunas para os parâmetros do modelo."""
        return Utilizador(
            id=row["id"],
            nome=row["nome"],
            username=row["username"],
            password_hash=row["password_hash"],
            password_salt=row["password_salt"],
            perfil=row["perfil"],          # coluna DB: perfil  →  modelo: perfil
            ativo=row["ativo"],
            data_registo=row["data_registo"],
        )

    # ✅ INSERIR
    def inserir(self, utilizador: Utilizador, password_salt) -> int:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        query = """
        INSERT INTO utilizadores
        (nome, username, password_hash, password_salt, perfil, ativo, data_registo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(query, (
                utilizador.nome,
                utilizador.username,
                utilizador.password_hash,
                password_salt,
                utilizador.perfil,
                utilizador.ativo,
                utilizador.data_registo,
            ))
            self.db_conn.commit()
            return cursor.lastrowid
        except Exception as e:
            self.db_conn.rollback()
            raise e
        finally:
            cursor.close()

    # 🔍 LISTAR TODOS
    def listar_utilizadores(self) -> List[Utilizador]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM utilizadores")
            rows = cursor.fetchall()
            return [self._row_to_utilizador(r) for r in rows]
        finally:
            cursor.close()

    # 🔍 CONSULTAR POR ID
    def consultar_por_id(self, user_id: int) -> Optional[Utilizador]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM utilizadores WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            return self._row_to_utilizador(row) if row else None
        finally:
            cursor.close()

    # 🔍 CONSULTAR POR USERNAME
    def consultar_por_username(self, username: str) -> Optional[Utilizador]:
        cursor = self.db_conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM utilizadores WHERE username = %s", (username,))
            row = cursor.fetchone()
            return self._row_to_utilizador(row) if row else None
        finally:
            cursor.close()

    # ❌ REMOVER
    def desativar(self, user_id: int) -> bool:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        cursor = self.db_conn.cursor()
        try:
            cursor.execute("UPDATE utilizadores SET ativo = FALSE WHERE id = %s", (user_id,))
            self.db_conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_conn.rollback()
            raise e
        finally:
            cursor.close()

    def remover(self, user_id: int) -> bool:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        cursor = self.db_conn.cursor()
        try:
            cursor.execute("SELECT id FROM utilizadores WHERE id = %s FOR UPDATE", (user_id,))
            cursor.execute("DELETE FROM utilizadores WHERE id = %s", (user_id,))
            self.db_conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_conn.rollback()
            raise e
        finally:
            cursor.close()

    # ✏️ ALTERAR NOME
    def alterar_nome(self, user_id: int, novo_nome: str) -> bool:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        cursor = self.db_conn.cursor()
        try:
            cursor.execute("UPDATE utilizadores SET nome = %s WHERE id = %s", (novo_nome, user_id))
            self.db_conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_conn.rollback()
            raise e
        finally:
            cursor.close()

    # ✏️ ALTERAR PERFIL
    def alterar_perfil(self, user_id: int, novo_perfil: str) -> bool:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        cursor = self.db_conn.cursor()
        try:
            cursor.execute("UPDATE utilizadores SET perfil = %s WHERE id = %s", (novo_perfil, user_id))
            self.db_conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_conn.rollback()
            raise e
        finally:
            cursor.close()

    # 🔐 ALTERAR PASSWORD
    def alterar_password(self, user_id: int, password_hash: str, password_salt: str) -> bool:
        try:
            self.db_conn.rollback()
        except Exception:
            pass
        query = """
        UPDATE utilizadores
        SET password_hash = %s, password_salt = %s
        WHERE id = %s
        """
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(query, (password_hash, password_salt, user_id))
            self.db_conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_conn.rollback()
            raise e
        finally:
            cursor.close()
        


    def verificar_permissao(self, id: int, permissao: str) -> bool:
        query = """
        SELECT 1
        FROM utilizadores u
        JOIN perfis_permissoes pp
            ON u.perfil = pp.perfil
        WHERE u.id = %s
        AND pp.permissao = %s
        AND pp.ativo = TRUE
        LIMIT 1
        """

        cursor = self.db_conn.cursor()

        try:
            cursor.execute(query, (id, permissao))
            resultado = cursor.fetchone()

            return resultado is not None

        finally:
            cursor.close()