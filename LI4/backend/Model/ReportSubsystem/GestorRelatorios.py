import os
from datetime import datetime

from Model.ReportSubsystem.RelatorioDAO import RelatorioDAO
from Model.ReportSubsystem.Relatorio import Relatorio
from Model.ReportSubsystem.RelatorioEconomico import gerar_relatorio_economico
from Model.ReportSubsystem.RelatorioStock import gerar_relatorio_stock
from Model.ReportSubsystem.RelatorioPerformance import gerar_relatorio_performance
from Model.ReportSubsystem.I_GestorRelatorios import I_GestorRelatorios

# Pasta onde os PDFs são guardados no servidor
RELATORIOS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "relatorios_gerados")


class GestorRelatorios(I_GestorRelatorios):
    def __init__(self, dao: RelatorioDAO):
        self.relatorio_dao = dao
        os.makedirs(RELATORIOS_DIR, exist_ok=True)

    # ------------------------------------------------------------------
    # Leitura
    # ------------------------------------------------------------------
    def listar_relatorios(self) -> list[Relatorio]:
        return self.relatorio_dao.listar_todos()

    def get_caminho_relatorio(self, id: int) -> str | None:
        """Devolve o caminho físico do ficheiro PDF, ou None se não existir."""
        relatorio: Relatorio = self.relatorio_dao.consultar_por_id(id)
        if relatorio is None:
            return None
        return relatorio.caminho

    # ------------------------------------------------------------------
    # Geração
    # ------------------------------------------------------------------

    def gerar_economico(
        self,
        ordens: int,
        lucro: float,
        crescimento: float,
        mes_referencia: str = None,
    ) -> int:
        """
        Gera um relatório económico em PDF, guarda-o em disco
        e regista-o na BD. Devolve o ID do relatório criado.
        """
        mes = mes_referencia or datetime.now().strftime("%B_%Y")
        nome_ficheiro = f"Economico_{mes}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        caminho = os.path.join(RELATORIOS_DIR, nome_ficheiro)

        gerar_relatorio_economico(caminho, ordens, lucro, crescimento)

        relatorio = Relatorio(
            id=None,
            titulo=f"Relatório Económico — {mes}",
            caminho=caminho,
            tipo="Económico",
        )
        return self.relatorio_dao.inserir(relatorio)

    def gerar_stock(
        self,
        pecas_usadas: dict,
        mes_referencia: str = None,
    ) -> int:
        """
        Gera um relatório de stock em PDF.

        pecas_usadas: {nome_peca: quantidade}
        Devolve o ID do relatório criado.
        """
        mes = mes_referencia or datetime.now().strftime("%B_%Y")
        nome_ficheiro = f"Stock_{mes}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        caminho = os.path.join(RELATORIOS_DIR, nome_ficheiro)

        gerar_relatorio_stock(caminho, pecas_usadas, mes)

        relatorio = Relatorio(
            id=None,
            titulo=f"Relatório de Stock — {mes}",
            caminho=caminho,
            tipo="Stock",
        )
        return self.relatorio_dao.inserir(relatorio)

    def gerar_performance(
        self,
        tempo_medio: float,
        diff_tempo: float,
        pct_nao_avancadas: float,
        diff_nao_avancadas: float,
        num_ordens: int,
        diff_ordens: float,
        mes_referencia: str = None,
    ) -> int:
        """
        Gera um relatório de performance em PDF.
        Devolve o ID do relatório criado.
        """
        mes = mes_referencia or datetime.now().strftime("%B_%Y")
        nome_ficheiro = f"Performance_{mes}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        caminho = os.path.join(RELATORIOS_DIR, nome_ficheiro)

        gerar_relatorio_performance(
            caminho,
            tempo_medio, diff_tempo,
            pct_nao_avancadas, diff_nao_avancadas,
            num_ordens, diff_ordens,
        )

        relatorio = Relatorio(
            id=None,
            titulo=f"Relatório de Performance — {mes}",
            caminho=caminho,
            tipo="Performance",
        )
        return self.relatorio_dao.inserir(relatorio)
