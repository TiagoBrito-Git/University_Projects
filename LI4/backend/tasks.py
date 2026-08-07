from celery_app import celery_app # Importe sua instância do Celery
from database import get_db # Sua função de conexão
import datetime
# Importe seus DAOs e Gestores
from Model.RepairSubsystem.GestorOrdensDeServico import GestorOrdensDeServico , DiagnosticoDAO , IntervencaoDAO , OrdemDeServicoDAO
from Model.ReportSubsystem.GestorRelatorios import GestorRelatorios, RelatorioDAO
from Model.PaymentsSubsystem.GestorPagamentos import GestorPagamentos, FaturaDAO
# ... outros imports

@celery_app.task(name="gerar_relatorio_economico_task")
def task_gerar_economico():
    data = datetime.datetime.now()
    mes = data.month
    ano = data.year
    # 1. Criar conexão manual (já que não há Depends aqui)
    db_gen = get_db()
    db = next(db_gen)
    try:
        gestor_faturas = GestorPagamentos(db) 
        
        os_dao = OrdemDeServicoDAO(db)
        int_dao = IntervencaoDAO(db)
        diagn_dao = DiagnosticoDAO(db)
        gestor_os = GestorOrdensDeServico(os_dao,int_dao,diagn_dao) 
        
        gestor_relatorios = GestorRelatorios(RelatorioDAO(db))

        lucro = gestor_faturas.obter_lucro_mes(mes, ano)
        crescimento = gestor_faturas.obter_taxa_crescimento_mensal(mes, ano)
        c_os = gestor_os.obter_contagem_ordens_mes_atual(mes, ano)

        id_relatorio = gestor_relatorios.gerar_economico(
            ordens=c_os,
            lucro=lucro,
            crescimento=crescimento,
            mes_referencia=mes,
        )
        return {"status": "sucesso", "id": id_relatorio}
        
    except Exception as e:
        # Logar o erro
        return {"status": "erro", "message": str(e)}
    finally:
        try:
            next(db_gen) 
        except StopIteration:
            pass



@celery_app.task(name="gerar_relatorio_stock_task")
def task_gerar_stock():
    data = datetime.datetime.now()
    mes = data.month
    ano = data.year

    db_gen = get_db()
    db = next(db_gen)
    try:
        from Model.StockSubsystem.GestorStock import GestorStock
        from Model.StockSubsystem.PecaDAO import PecaDAO

        os_dao   = OrdemDeServicoDAO(db)
        int_dao  = IntervencaoDAO(db)
        diagn_dao = DiagnosticoDAO(db)
        gestor_os = GestorOrdensDeServico(os_dao, int_dao, diagn_dao)
        gestor_stock = GestorStock(PecaDAO(db))

        gestor_relatorios = GestorRelatorios(RelatorioDAO(db))

        # 1. Obtém {id_peca: quantidade_total} das intervenções do mês
        pecas_por_id = gestor_os.obter_pecas_usadas(mes, ano)

        # 2. Troca os IDs pelos nomes reais das peças
        pecas_usadas = {}
        for id_peca, quantidade in pecas_por_id.items():
            peca = gestor_stock.consultarStock(id_peca)
            nome = peca.nome if peca else f"Peça #{id_peca}"
            pecas_usadas[nome] = pecas_usadas.get(nome, 0) + quantidade

        # 3. Gera o relatório
        mes_ref = f"{data.strftime('%B')}_{ano}"
        id_relatorio = gestor_relatorios.gerar_stock(
            pecas_usadas=pecas_usadas,
            mes_referencia=mes_ref,
        )
        return {"status": "sucesso", "id": id_relatorio}

    except Exception as e:
        return {"status": "erro", "message": str(e)}
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass




@celery_app.task(name="gerar_relatorio_performance_task")
def task_gerar_performance():
    data = datetime.datetime.now()
    mes = data.month
    ano = data.year

    db_gen = get_db()
    db = next(db_gen)
    try:
        os_dao    = OrdemDeServicoDAO(db)
        int_dao   = IntervencaoDAO(db)
        diagn_dao = DiagnosticoDAO(db)
        gestor_os = GestorOrdensDeServico(os_dao, int_dao, diagn_dao)
        gestor_relatorios = GestorRelatorios(RelatorioDAO(db))

        kpis = gestor_os.obter_dados_performance(mes, ano)

        id_relatorio = gestor_relatorios.gerar_performance(
            tempo_medio         = kpis["tempo_medio"],
            diff_tempo          = kpis["diff_tempo"],
            pct_nao_avancadas   = kpis["pct_nao_avancadas"],
            diff_nao_avancadas  = kpis["diff_nao_avancadas"],
            num_ordens          = kpis["num_ordens"],
            diff_ordens         = kpis["diff_ordens"],
            mes_referencia      = f"{data.strftime('%B')}_{ano}",
        )
        return {"status": "sucesso", "id": id_relatorio}

    except Exception as e:
        return {"status": "erro", "message": str(e)}
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass