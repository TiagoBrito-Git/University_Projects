from datetime import datetime

from celery_app import celery_app

from database import get_db
from Model.ReportSubsystem.Relatorio import Relatorio
from Model.ReportSubsystem.RelatorioDAO import RelatorioDAO
from Model.ReportSubsystem.RelatorioStock import gerar_relatorio_stock
from Model.ReportSubsystem.RelatorioPerformance import gerar_relatorio_performance
from Model.ReportSubsystem.RelatorioEconomico import gerar_relatorio_economico
from Model.StockSubsystem.GestorStock import GestorStock
from Model.RepairSubsystem.GestorOrdensDeServico import GestorOrdensDeServico


@celery_app.task
def gerar_relatorio_mensal():

    conn = get_db()

    dao = RelatorioDAO(conn)

    nome_stock = f"relatorio_stock_{datetime.now().strftime('%Y_%m')}.pdf"
    nome_performance = f"relatorio_performance_{datetime.now().strftime('%Y_%m')}.pdf"
    nome_economico = f"relatorio_economico_{datetime.now().strftime('%Y_%m')}.pdf"

    caminho = f"./relatorios/{nome_stock}"

    gerar_relatorio_stock(nome_stock,
                          pecas_usadas=None,
                          mes_referencia=datetime.now().month)

    gerar_relatorio_performance(nome_performance,
                                tempo_medio=None,
                                diff_tempo=None,
                                pct_nao_avancadas=None,
                                num_ordens=None,
                                diff_ordens=None)

    gerar_relatorio_economico(nome_economico,
                              ordens=None,
                              lucro=None,
                              crescimento=None
                              )

    relatorio_stock = Relatorio(
        id=None,
        titulo=nome_stock,
        caminho=caminho,
        tipo="stock"
    )
    relatorio_performance= Relatorio(
        id=None,
        titulo=nome_performance,
        caminho=caminho,
        tipo="performance"
    )
    relatorio_economico = Relatorio(
        id=None,
        titulo=nome_economico,
        caminho=caminho,
        tipo="económico"
    )

    dao.inserir(relatorio_stock)
    dao.inserir(relatorio_performance)
    dao.inserir(relatorio_economico)

    print("Relatórios mensais criados.")