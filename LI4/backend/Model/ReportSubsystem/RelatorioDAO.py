import mysql.connector
from Model.ReportSubsystem.Relatorio import Relatorio


class RelatorioDAO:
    def __init__(self, db_connection):
        """Recebe a conexão ativa com a base de dados."""
        self.conn = db_connection
        self.cursor = self.conn.cursor(dictionary=True)

    def inserir(self, relatorio:Relatorio):
        """
        Insere um relatório na base de dados.
        Recebe um objeto Relatorio.
        """

        query = """
            INSERT INTO relatorios (titulo, caminho, tipo)
            VALUES (%s, %s, %s)
        """

        try:
            valores = (
                relatorio.titulo,
                relatorio.caminho,
                relatorio.tipo
            )

            self.cursor.execute(query, valores)
            self.conn.commit()

            relatorio.id = self.cursor.lastrowid

            print("Relatório inserido com sucesso.")
            return relatorio.id

        except mysql.connector.Error as err:
            print(f"Erro ao inserir relatório: {err}")
            return None

    def listar_todos(self):
        """
        Retorna todos os relatórios como objetos Relatorio.
        """

        query = "SELECT * FROM relatorios ORDER BY id DESC"

        try:
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            relatorios = []

            for row in resultados:
                relatorio = Relatorio(
                    id=row["id"],
                    titulo=row["titulo"],
                    caminho=row["caminho"],
                    tipo=row["tipo"]
                )

                relatorios.append(relatorio)

            return relatorios

        except mysql.connector.Error as err:
            print(f"Erro ao listar relatórios: {err}")
            return []

    def consultar_por_id(self, id_relatorio):
        """
        Procura um relatório pelo ID.
        """

        query = "SELECT * FROM relatorios WHERE id = %s"

        try:
            self.cursor.execute(query, (id_relatorio,))
            row = self.cursor.fetchone()

            if row:
                return Relatorio(
                    id=row["id"],
                    titulo=row["titulo"],
                    caminho=row["caminho"],
                    tipo=row["tipo"]
                )

            return None

        except mysql.connector.Error as err:
            print(f"Erro ao consultar relatório: {err}")
            return None

    def remover(self, id_relatorio):
        """
        Remove um relatório da base de dados.
        """

        query = "DELETE FROM relatorios WHERE id = %s"

        try:
            self.cursor.execute(query, (id_relatorio,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print("Relatório removido com sucesso.")
                return True

            return False

        except mysql.connector.Error as err:
            print(f"Erro ao remover relatório: {err}")
            return False

    def atualizar(self, relatorio):
        """
        Atualiza os dados de um relatório.
        """

        query = """
            UPDATE relatorios
            SET titulo = %s,
                caminho = %s,
                tipo = %s
            WHERE id = %s
        """

        try:
            valores = (
                relatorio.titulo,
                relatorio.caminho,
                relatorio.tipo,
                relatorio.id
            )

            self.cursor.execute(query, valores)
            self.conn.commit()

            print("Relatório atualizado com sucesso.")
            return True

        except mysql.connector.Error as err:
            print(f"Erro ao atualizar relatório: {err}")
            return False