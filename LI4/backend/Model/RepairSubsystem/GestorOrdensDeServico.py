from datetime import datetime

from Model.RepairSubsystem.I_GestorOrdensDeServico import I_GestorOrdensDeServico
from Model.RepairSubsystem.DiagnosticoDAO import DiagnosticoDAO, Diagnostico
from Model.RepairSubsystem.IntervencaoDAO import IntervencaoDAO, Intervencao
from Model.RepairSubsystem.OrdemDeServicoDAO import OrdemDeServicoDAO
from Model.RepairSubsystem.OrdemDeServico import OrdemDeServico




class GestorOrdensDeServico(I_GestorOrdensDeServico):
    TAXA_DIAGNOSTICO = 20.0
    TAXA_MAO_OBRA = 20.0

    _AVANCAR_MAPA = {
        "Aguarda Diagnóstico": "Aguarda Resposta",
        "Em Reparação": "Aguarda Faturação",
        "Aguarda Faturação": "Faturada",
        "Faturada": "Encerrada",
    }


    def __init__(self, os_dao:OrdemDeServicoDAO, intervencao_dao:IntervencaoDAO, diagnostico_dao:DiagnosticoDAO):
        self.os_dao = os_dao
        self.intervencao_dao = intervencao_dao
        self.diagnostico_dao = diagnostico_dao

    def criar_ordem_de_servico(self, data_conclusao, descricao, id_trotinete, id_tecnico, id_cliente) -> int:
        os = OrdemDeServico(-1, datetime.now(),data_conclusao, "Aguarda Diagnóstico", descricao, id_trotinete, id_tecnico, id_cliente)
        return self.os_dao.inserir(os)
    

    def _validar_transicao_estado(self, ordem: OrdemDeServico, estado_destino: str) -> str | None:
        """Valida a transição de estado. Devolve o novo estado se válido, None se inválido."""
        match ordem.estado:
            case "Aguarda Diagnóstico":
                if estado_destino == "Aguarda Resposta" and self.diagnostico_dao.consultar_por_os(ordem.id) is not None:
                    return estado_destino
            case "Aguarda Resposta":
                if estado_destino in ("Em Reparação", "Cancelada"):
                    return estado_destino
            case "Em Reparação":
                if estado_destino in ("Cancelada", "Aguarda Faturação"):
                    return estado_destino
            case "Aguarda Faturação":
                if estado_destino == "Faturada":
                    return estado_destino
            case "Faturada":
                if estado_destino == "Encerrada":
                    return estado_destino
        return None

    def avancar_estado_ordem_de_servico(self, id: int) -> bool:
        os = self.os_dao.consultar_por_id(id)
        if not os:
            return False
        proximo = self._AVANCAR_MAPA.get(os.estado)
        if not proximo:
            return False
        return self.alterar_estado_ordem_de_servico(id, proximo)

    def alterar_estado_ordem_de_servico(self, id, estado) -> bool:
        return self.os_dao.alterar_estado(
            id,
            lambda ordem: self._validar_transicao_estado(ordem, estado)
        )

    def alterar_estado_em_transacao(self, id: int, estado: str) -> bool:
        """Altera o estado sem commit — para uso numa transação gerida externamente."""
        return self.os_dao.alterar_estado_sem_commit(
            id,
            lambda ordem: self._validar_transicao_estado(ordem, estado)
        )
    
    def atualizar_ordem_de_servico(self, id, data_conclusao, descricao) -> bool:
        ordem = self.os_dao.consultar_por_id(id)
        if not ordem:
            return False
        ordem.data_conclusao = data_conclusao
        ordem.descricao = descricao
        return self.os_dao.atualizar(ordem)

    def consultar_os(self, id) -> OrdemDeServico:
        return self.os_dao.consultar_por_id(id)
    
    def listar_ordens_de_servico(self) -> list[OrdemDeServico]:
        return self.os_dao.listar()
    
    def remover_ordem_de_servico(self, id) -> bool:
        return self.os_dao.remover(id)
    

    def criar_intervencao(self,id_os,id_tecnico,descricao,tempo: float,custo_pecas,pecas):
        os = self.os_dao.consultar_por_id(id_os)

        if not os:
            return -1

        if os.estado != "Em Reparação":
            return -3

        try:
            custo_total = custo_pecas + tempo*self.TAXA_MAO_OBRA

            i = Intervencao(-1, descricao, tempo, datetime.now(), id_os, id_tecnico,custo_total,pecas)
            return self.intervencao_dao.inserir(i)

        except Exception:
            return -2
    


    def criar_diagnostico(self,id_os,id_tecnico,descricao,orcamento_pecas,pecas,tempo_estimado: float):
        os = self.os_dao.consultar_por_id(id_os)

        if not os:
            return -1

        if os.estado != "Aguarda Diagnóstico":
            return -3

        try:
            custo_estimado = orcamento_pecas + tempo_estimado*self.TAXA_MAO_OBRA + self.TAXA_DIAGNOSTICO

            existente = self.diagnostico_dao.consultar_por_os(id_os)
            if existente:
                d = Diagnostico(existente.id, descricao, custo_estimado, tempo_estimado, datetime.now(), id_os, id_tecnico, pecas=pecas)
                return self.diagnostico_dao.atualizar(d)

            d = Diagnostico(-1,descricao,custo_estimado,tempo_estimado,datetime.now(),id_os,id_tecnico,pecas=pecas)
            return self.diagnostico_dao.inserir(d)

        except Exception:
            return -2
        

    def alterar_diagnostico(self,id,id_os,id_tecnico,descricao,orcamento_pecas,pecas,tempo_estimado: float):
        os = self.os_dao.consultar_por_id(id_os)

        if not os:
            return -1

        try:
            custo_estimado = orcamento_pecas + tempo_estimado*self.TAXA_MAO_OBRA + self.TAXA_DIAGNOSTICO
            d = Diagnostico(id, descricao, custo_estimado, tempo_estimado, datetime.now(), id_os, id_tecnico, pecas=pecas)
            return self.diagnostico_dao.atualizar(d)

        except Exception:
            return -2



    def obter_resumo_pecas_intervencoes(self, id_os: int):

        intervencoes = self.intervencao_dao.consultar_por_os(id_os) 
        
        resumo_pecas = {} 

        for intervencao in intervencoes:
            for id_peca, dados in intervencao.pecas_usadas.items():
                quantidade = dados.get('quantidade', 0)
                preco_unitario = dados.get('preco_unitario', 0.0)
                valor_total_peca = quantidade * preco_unitario
                
                if id_peca in resumo_pecas:
                    resumo_pecas[id_peca] += valor_total_peca
                else:
                    resumo_pecas[id_peca] = valor_total_peca
                    
        return resumo_pecas
    

    # No GestorOrdensDeServico.py

    def preparar_dados_finalizacao(self, id_os: int, estado_final: str):

        os = self.os_dao.consultar_por_id(id_os)
        if not os:
            return None

        if estado_final == "Cancelada":
            return {
                "pecas": {},
                "mao_de_obra": self.TAXA_DIAGNOSTICO,
                "id_os": id_os
            }

        # Se for concluída, calcula o real (inclui sempre o custo de diagnóstico)
        intervencoes = self.intervencao_dao.consultar_por_os(id_os)
        total_mao_obra = self.TAXA_DIAGNOSTICO
        pecas_resumo = {}

        for i in intervencoes:
            total_mao_obra += float(i.horas_trabalhadas or 0) * self.TAXA_MAO_OBRA
            for id_p, dados in i.pecas_usadas.items():
                if id_p not in pecas_resumo:
                    pecas_resumo[id_p] = {
                        "quantidade": 0,
                        "preco_unitario": dados["preco_unitario"],
                    }
                pecas_resumo[id_p]["quantidade"] += dados["quantidade"]

        return {
            "pecas": pecas_resumo,
            "mao_de_obra": total_mao_obra,
            "id_os": id_os
        }



    def obter_detalhes_completos_os(self, id_os: int):
        os_base:OrdemDeServico = self.os_dao.consultar_por_id(id_os)
        if not os_base:
            return None

        diagnostico_obj = self.diagnostico_dao.consultar_por_os(id_os)
        
        intervencoes_objs = self.intervencao_dao.consultar_por_os(id_os)

        dados_finais = os_base.to_dict() 
        
        dados_finais["diagnostico"] = diagnostico_obj.to_dict() if diagnostico_obj else None
        dados_finais["intervencoes"] = [i.to_dict() for i in intervencoes_objs]
        
        return dados_finais


    def obter_contagem_ordens_mes_atual(self,mes,ano) -> int:
        
        return self.os_dao.contar_ordens_por_mes(mes, ano)
    
    def obter_pecas_usadas(self, mes: int, ano: int) -> dict:
        intervencoes = self.intervencao_dao.consultar_por_mes(mes, ano)
        resumo = {}
        for intervencao in intervencoes:
            for id_peca, dados in intervencao.pecas_usadas.items():
                quantidade = dados.get("quantidade", 0)
                resumo[id_peca] = resumo.get(id_peca, 0) + quantidade
        return resumo



    def obter_dados_performance(self, mes: int, ano: int) -> dict:
        # Mês anterior
        if mes == 1:
            mes_ant, ano_ant = 12, ano - 1
        else:
            mes_ant, ano_ant = mes - 1, ano

        # Valores do mês atual
        num_ordens      = self.os_dao.contar_ordens_por_mes(mes, ano)
        num_ordens_ant  = self.os_dao.contar_ordens_por_mes(mes_ant, ano_ant)

        paradas         = self.os_dao.contar_ordens_paradas_por_mes(mes, ano)
        paradas_ant     = self.os_dao.contar_ordens_paradas_por_mes(mes_ant, ano_ant)

        tempo_medio     = self.intervencao_dao.tempo_medio_por_mes(mes, ano)
        tempo_medio_ant = self.intervencao_dao.tempo_medio_por_mes(mes_ant, ano_ant)

        # % de OS paradas em relação ao total
        pct_nao_avancadas     = (paradas / num_ordens * 100)         if num_ordens     else 0.0
        pct_nao_avancadas_ant = (paradas_ant / num_ordens_ant * 100) if num_ordens_ant else 0.0

        # Variações percentuais vs mês anterior
        def variacao(atual, anterior):
            if anterior == 0:
                return 0.0
            return ((atual - anterior) / anterior) * 100

        return {
            "tempo_medio":          tempo_medio,
            "diff_tempo":           variacao(tempo_medio, tempo_medio_ant),
            "pct_nao_avancadas":    pct_nao_avancadas,
            "diff_nao_avancadas":   variacao(pct_nao_avancadas, pct_nao_avancadas_ant),
            "num_ordens":           num_ordens,
            "diff_ordens":          variacao(num_ordens, num_ordens_ant),
        }