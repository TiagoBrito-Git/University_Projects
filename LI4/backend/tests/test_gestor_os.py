"""Testes unitários do GestorOrdensDeServico — máquina de estados e cálculos de custo."""
import pytest
from datetime import datetime
from unittest.mock import MagicMock, call

from Model.RepairSubsystem.GestorOrdensDeServico import GestorOrdensDeServico
from Model.RepairSubsystem.OrdemDeServico import OrdemDeServico
from Model.RepairSubsystem.Intervencao import Intervencao


def _make_gestor(os_dao=None, intervencao_dao=None, diagnostico_dao=None):
    return GestorOrdensDeServico(
        os_dao=os_dao or MagicMock(),
        intervencao_dao=intervencao_dao or MagicMock(),
        diagnostico_dao=diagnostico_dao or MagicMock(),
    )


def _ordem(estado: str, id: int = 1) -> OrdemDeServico:
    return OrdemDeServico(
        id=id,
        data_abertura=datetime(2024, 1, 10),
        data_conclusao=None,
        estado=estado,
        descricao="Problema de teste",
        id_trotinete=2,
        id_tecnico=3,
        id_cliente=1,
    )


# ─────────────────────────────────────────────────────────────────────────────
# MÁQUINA DE ESTADOS
# ─────────────────────────────────────────────────────────────────────────────

def _side_effect_alterar_estado(estado_atual: str, id: int = 1):
    """
    Simula o comportamento de OrdemDeServicoDAO.alterar_estado():
    chama a função de validação com a ordem no estado indicado e
    devolve True/False conforme o resultado da validação.
    """
    def side_effect(os_id, validar_fn):
        novo_estado = validar_fn(_ordem(estado_atual, id))
        return novo_estado is not None
    return side_effect


class TestAlterarEstado:
    def test_aguarda_diagnostico_para_aguarda_resposta_com_diagnostico(self,
            mock_os_dao, mock_diagnostico_dao, diagnostico_exemplo):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Aguarda Diagnóstico")
        mock_diagnostico_dao.consultar_por_os.return_value = diagnostico_exemplo

        gestor = _make_gestor(os_dao=mock_os_dao, diagnostico_dao=mock_diagnostico_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Aguarda Resposta") is True

    def test_aguarda_diagnostico_para_aguarda_resposta_sem_diagnostico(self,
            mock_os_dao, mock_diagnostico_dao):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Aguarda Diagnóstico")
        mock_diagnostico_dao.consultar_por_os.return_value = None

        gestor = _make_gestor(os_dao=mock_os_dao, diagnostico_dao=mock_diagnostico_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Aguarda Resposta") is False

    def test_aguarda_diagnostico_para_em_reparacao_invalido(self,
            mock_os_dao, mock_diagnostico_dao):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Aguarda Diagnóstico")
        mock_diagnostico_dao.consultar_por_os.return_value = MagicMock()

        gestor = _make_gestor(os_dao=mock_os_dao, diagnostico_dao=mock_diagnostico_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Em Reparação") is False

    def test_aguarda_resposta_para_em_reparacao(self, mock_os_dao):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Aguarda Resposta")

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Em Reparação") is True

    def test_aguarda_resposta_para_cancelada(self, mock_os_dao):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Aguarda Resposta")

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Cancelada") is True

    def test_em_reparacao_para_aguarda_faturacao(self, mock_os_dao):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Em Reparação")

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Aguarda Faturação") is True

    def test_em_reparacao_para_cancelada(self, mock_os_dao):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Em Reparação")

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Cancelada") is True

    def test_em_reparacao_para_concluido_invalido(self, mock_os_dao):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Em Reparação")

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Concluído") is False

    def test_aguarda_faturacao_para_faturada(self, mock_os_dao):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Aguarda Faturação")

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Faturada") is True

    def test_aguarda_faturacao_para_encerrada_invalido(self, mock_os_dao):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Aguarda Faturação")

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Encerrada") is False

    def test_faturada_para_encerrada(self, mock_os_dao):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Faturada")

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Encerrada") is True

    def test_encerrada_bloqueia_transicao(self, mock_os_dao):
        mock_os_dao.alterar_estado.side_effect = _side_effect_alterar_estado("Encerrada")

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.alterar_estado_ordem_de_servico(1, "Cancelada") is False

    def test_os_inexistente_retorna_false(self, mock_os_dao):
        mock_os_dao.alterar_estado.return_value = False

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.alterar_estado_ordem_de_servico(99, "Aguarda Resposta") is False


# ─────────────────────────────────────────────────────────────────────────────
# CÁLCULOS DE CUSTO
# ─────────────────────────────────────────────────────────────────────────────

class TestCriarDiagnostico:
    def test_custo_estimado_calculado_correctamente(self, mock_os_dao, mock_diagnostico_dao):
        # custo = orcamento_pecas + tempo * 20 + 20 (taxa diagnóstico)
        mock_os_dao.consultar_por_id.return_value = _ordem("Aguarda Diagnóstico")
        mock_diagnostico_dao.consultar_por_os.return_value = None  # sem diagnóstico existente → inserir
        mock_diagnostico_dao.inserir.return_value = 10

        gestor = _make_gestor(os_dao=mock_os_dao, diagnostico_dao=mock_diagnostico_dao)
        resultado = gestor.criar_diagnostico(
            id_os=1, id_tecnico=3,
            descricao="Bateria degradada",
            orcamento_pecas=100.0,
            pecas={},
            tempo_estimado=5,
        )

        assert resultado == 10
        diagnostico_inserido = mock_diagnostico_dao.inserir.call_args[0][0]
        # 100 + 5*20 + 20 = 220
        assert diagnostico_inserido.orcamento_estimado == pytest.approx(220.0)

    def test_os_inexistente_retorna_menos_1(self, mock_os_dao, mock_diagnostico_dao):
        mock_os_dao.consultar_por_id.return_value = None

        gestor = _make_gestor(os_dao=mock_os_dao, diagnostico_dao=mock_diagnostico_dao)
        resultado = gestor.criar_diagnostico(
            id_os=99, id_tecnico=3,
            descricao="x", orcamento_pecas=0, pecas={}, tempo_estimado=1,
        )

        assert resultado == -1


class TestCriarIntervencao:
    def test_custo_total_calculado_correctamente(self, mock_os_dao, mock_intervencao_dao):
        # custo = custo_pecas + tempo * 20
        mock_os_dao.consultar_por_id.return_value = _ordem("Em Reparação")
        mock_intervencao_dao.inserir.return_value = 20

        gestor = _make_gestor(os_dao=mock_os_dao, intervencao_dao=mock_intervencao_dao)
        resultado = gestor.criar_intervencao(
            id_os=1, id_tecnico=3,
            descricao="Substituição da bateria",
            tempo=3,
            custo_pecas=50.0,
            pecas={},
        )

        assert resultado == 20
        intervencao_inserida = mock_intervencao_dao.inserir.call_args[0][0]
        # 50 + 3*20 = 110
        assert intervencao_inserida.custo_total == pytest.approx(110.0)

    def test_custo_total_com_tempo_decimal(self, mock_os_dao, mock_intervencao_dao):
        # 2h30m = 2.5h → custo = 0 + 2.5*20 = 50
        mock_os_dao.consultar_por_id.return_value = _ordem("Em Reparação")
        mock_intervencao_dao.inserir.return_value = 21

        gestor = _make_gestor(os_dao=mock_os_dao, intervencao_dao=mock_intervencao_dao)
        gestor.criar_intervencao(
            id_os=1, id_tecnico=3,
            descricao="Ajuste de travões",
            tempo=2.5,
            custo_pecas=0.0,
            pecas={},
        )

        intervencao_inserida = mock_intervencao_dao.inserir.call_args[0][0]
        assert intervencao_inserida.custo_total == pytest.approx(50.0)

    def test_os_inexistente_retorna_menos_1(self, mock_os_dao):
        mock_os_dao.consultar_por_id.return_value = None

        gestor = _make_gestor(os_dao=mock_os_dao)
        resultado = gestor.criar_intervencao(
            id_os=99, id_tecnico=3,
            descricao="x", tempo=1, custo_pecas=0, pecas={},
        )

        assert resultado == -1


# ─────────────────────────────────────────────────────────────────────────────
# PREPARAR DADOS FINALIZAÇÃO
# ─────────────────────────────────────────────────────────────────────────────

class TestPrepararDadosFinalizacao:
    def test_cancelada_retorna_taxa_diagnostico_sem_pecas(self, mock_os_dao):
        mock_os_dao.consultar_por_id.return_value = _ordem("Cancelada")

        gestor = _make_gestor(os_dao=mock_os_dao)
        dados = gestor.preparar_dados_finalizacao(1, "Cancelada")

        assert dados["mao_de_obra"] == pytest.approx(20.0)
        assert dados["pecas"] == {}

    def test_aguarda_faturacao_soma_intervencoes(self, mock_os_dao, mock_intervencao_dao):
        mock_os_dao.consultar_por_id.return_value = _ordem("Aguarda Faturação")

        inv1 = Intervencao(1, "Trabalho A", 2.0, datetime.now(), 1, 3, 40.0,
                           {1: {"quantidade": 2, "preco_unitario": 10.0}})
        inv2 = Intervencao(2, "Trabalho B", 1.0, datetime.now(), 1, 3, 20.0,
                           {2: {"quantidade": 1, "preco_unitario": 15.0}})
        mock_intervencao_dao.consultar_por_os.return_value = [inv1, inv2]

        gestor = _make_gestor(os_dao=mock_os_dao, intervencao_dao=mock_intervencao_dao)
        dados = gestor.preparar_dados_finalizacao(1, "Aguarda Faturação")

        # mao_de_obra = taxa_diagnostico + (2 + 1) * 20 = 20 + 60 = 80
        assert dados["mao_de_obra"] == pytest.approx(80.0)
        assert 1 in dados["pecas"]
        assert 2 in dados["pecas"]
        assert dados["pecas"][1] == {"quantidade": 2, "preco_unitario": 10.0}
        assert dados["pecas"][2] == {"quantidade": 1, "preco_unitario": 15.0}

    def test_os_inexistente_retorna_none(self, mock_os_dao):
        mock_os_dao.consultar_por_id.return_value = None

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.preparar_dados_finalizacao(99, "Concluído") is None


# ─────────────────────────────────────────────────────────────────────────────
# PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────

class TestObterDadosPerformance:
    def test_sem_ordens_nao_divide_por_zero(self, mock_os_dao, mock_intervencao_dao):
        mock_os_dao.contar_ordens_por_mes.return_value = 0
        mock_os_dao.contar_ordens_paradas_por_mes.return_value = 0
        mock_intervencao_dao.tempo_medio_por_mes.return_value = 0.0

        gestor = _make_gestor(os_dao=mock_os_dao, intervencao_dao=mock_intervencao_dao)
        dados = gestor.obter_dados_performance(3, 2024)

        assert dados["pct_nao_avancadas"] == pytest.approx(0.0)

    def test_janeiro_usa_dezembro_do_ano_anterior(self, mock_os_dao, mock_intervencao_dao):
        mock_os_dao.contar_ordens_por_mes.return_value = 5
        mock_os_dao.contar_ordens_paradas_por_mes.return_value = 0
        mock_intervencao_dao.tempo_medio_por_mes.return_value = 2.0

        gestor = _make_gestor(os_dao=mock_os_dao, intervencao_dao=mock_intervencao_dao)
        gestor.obter_dados_performance(1, 2024)

        # Mês anterior de Janeiro 2024 deve ser Dezembro 2023
        calls = mock_os_dao.contar_ordens_por_mes.call_args_list
        meses_consultados = [(c[0][0], c[0][1]) for c in calls]
        assert (12, 2023) in meses_consultados

    def test_diff_zero_quando_mes_anterior_sem_ordens(self, mock_os_dao, mock_intervencao_dao):
        def contar(mes, ano):
            return 5 if mes == 3 else 0  # só tem dados no mês atual

        mock_os_dao.contar_ordens_por_mes.side_effect = contar
        mock_os_dao.contar_ordens_paradas_por_mes.return_value = 0
        mock_intervencao_dao.tempo_medio_por_mes.return_value = 0.0

        gestor = _make_gestor(os_dao=mock_os_dao, intervencao_dao=mock_intervencao_dao)
        dados = gestor.obter_dados_performance(3, 2024)

        assert dados["diff_ordens"] == pytest.approx(0.0)


# ─────────────────────────────────────────────────────────────────────────────
# ATUALIZAR OS
# ─────────────────────────────────────────────────────────────────────────────

class TestAtualizarOS:
    def test_os_inexistente_retorna_false(self, mock_os_dao):
        mock_os_dao.consultar_por_id.return_value = None

        gestor = _make_gestor(os_dao=mock_os_dao)
        assert gestor.atualizar_ordem_de_servico(99, None, "nova desc") is False

    def test_os_existente_atualiza_e_retorna_resultado_dao(self, mock_os_dao):
        ordem = _ordem("Em Reparação")
        mock_os_dao.consultar_por_id.return_value = ordem
        mock_os_dao.atualizar.return_value = True

        gestor = _make_gestor(os_dao=mock_os_dao)
        resultado = gestor.atualizar_ordem_de_servico(1, None, "Descrição actualizada")

        assert resultado is True
        assert ordem.descricao == "Descrição actualizada"
        mock_os_dao.atualizar.assert_called_once_with(ordem)
