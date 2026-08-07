from datetime import date


class Diagnostico:
    def __init__(
        self,
        id: int,
        descricao: str,
        orcamento_estimado: float,
        horas_mao_de_obra: float,
        data: date,
        id_os: int,
        id_tecnico: int,
        decisao_cliente: str = "Indefinido",
        data_decisao: date = None,
        # pecas: dict {id_peca: {"quantidade": int, "preco_unitario": float}}
        pecas: dict = None
    ):
        self._id = id
        self._descricao = descricao
        self._orcamento_estimado = orcamento_estimado
        self._horas_mao_de_obra = horas_mao_de_obra
        self._data = data
        self._id_os = id_os
        self._id_tecnico = id_tecnico
        self._decisao_cliente = decisao_cliente
        self._data_decisao = data_decisao
        self._pecas = pecas if pecas is not None else {}

    # --------- ID ---------
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    # --------- DESCRIÇÃO ---------
    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, value):
        self._descricao = value

    # --------- ORÇAMENTO ---------
    @property
    def orcamento_estimado(self):
        return self._orcamento_estimado

    @orcamento_estimado.setter
    def orcamento_estimado(self, value):
        self._orcamento_estimado = value

    # --------- HORAS MÃO DE OBRA ---------
    @property
    def horas_mao_de_obra(self):
        return self._horas_mao_de_obra

    @horas_mao_de_obra.setter
    def horas_mao_de_obra(self, value):
        self._horas_mao_de_obra = value

    # --------- DATA ---------
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    # --------- DECISÃO CLIENTE ---------
    @property
    def decisao_cliente(self):
        return self._decisao_cliente

    @decisao_cliente.setter
    def decisao_cliente(self, value):
        self._decisao_cliente = value

    # --------- DATA DECISÃO ---------
    @property
    def data_decisao(self):
        return self._data_decisao

    @data_decisao.setter
    def data_decisao(self, value):
        self._data_decisao = value

    # --------- ID ORDEM DE SERVIÇO ---------
    @property
    def id_os(self):
        return self._id_os

    @id_os.setter
    def id_os(self, value):
        self._id_os = value

    # --------- ID TÉCNICO ---------
    @property
    def id_tecnico(self):
        return self._id_tecnico

    @id_tecnico.setter
    def id_tecnico(self, value):
        self._id_tecnico = value

    # --------- PEÇAS ---------
    @property
    def pecas(self):
        return self._pecas

    @pecas.setter
    def pecas(self, value):
        self._pecas = value

    # --------- UTILIDADE ---------
    def to_dict(self):
        return {
            "id": self._id,
            "descricao": self._descricao,
            "orcamento_estimado": float(self._orcamento_estimado),
            "horas_mao_de_obra": float(self._horas_mao_de_obra) if self._horas_mao_de_obra is not None else 0.0,
            # Formata a data para string (ISO format) para evitar erro de serialização JSON
            "data": self._data.isoformat() if hasattr(self._data, 'isoformat') else str(self._data),
            "decisao_cliente": self._decisao_cliente,
            "data_decisao": self._data_decisao.isoformat() if self._data_decisao else None,
            "id_os": self._id_os,
            "id_tecnico": self._id_tecnico,
            # Se 'pecas' for um dict {id: {info}}, transformamos numa lista para facilitar o v-for no Vue
            "pecas": [
                {
                    "id_peca": id_p,
                    "quantidade": dados["quantidade"],
                    "preco_unitario": float(dados["preco_unitario"])
                }
                for id_p, dados in self._pecas.items()
            ] if self._pecas else []
        }