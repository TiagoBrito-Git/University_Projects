from datetime import date


class Intervencao():

    def __init__(self, id, descricao, horas_trabalhadas, data, id_os, id_tecnico, custo_total=0.0, pecas_usadas: dict = None):
        self._id: int = id
        self._descricao: str = descricao
        self._horas_trabalhadas: float = horas_trabalhadas
        self._custo_total: float = custo_total
        self._data: date = data
        self._pecas_usadas: dict[int, int] = pecas_usadas if pecas_usadas is not None else {}
        self._id_os: int = id_os
        self._id_tecnico: int = id_tecnico

    # --------- ID ---------
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    # --------- DESCRICAO ---------
    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, value: str):
        if not value or not value.strip():
            raise ValueError("Descrição não pode estar vazia")
        self._descricao = value.strip()

    # --------- HORAS TRABALHADAS ---------
    @property
    def horas_trabalhadas(self) -> float:
        return self._horas_trabalhadas

    @horas_trabalhadas.setter
    def horas_trabalhadas(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Horas trabalhadas devem ser um número positivo")
        self._horas_trabalhadas = float(value)

    # --------- CUSTO TOTAL ---------
    @property
    def custo_total(self) -> float:
        return self._custo_total

    @custo_total.setter
    def custo_total(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Custo total deve ser um número positivo")
        self._custo_total = float(value)

    # --------- PECAS USADAS ---------
    @property
    def pecas_usadas(self) -> dict:
        return self._pecas_usadas

    @pecas_usadas.setter
    def pecas_usadas(self, value: dict):
        if not isinstance(value, dict):
            raise ValueError("Peças usadas deve ser um dicionário")
        self._pecas_usadas = value

    # --------- DATA ---------
    @property
    def data(self) -> date:
        return self._data

    @data.setter
    def data(self, value: date):
        if not isinstance(value, date):
            raise ValueError("Data deve ser um objeto do tipo date")
        self._data = value

    # --------- ID_OS ---------
    @property
    def id_os(self) -> int:
        return self._id_os

    @id_os.setter
    def id_os(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("ID da ordem de serviço deve ser um inteiro positivo")
        self._id_os = value

    # --------- ID_TECNICO ---------
    @property
    def id_tecnico(self) -> int:
        return self._id_tecnico

    @id_tecnico.setter
    def id_tecnico(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("ID do técnico deve ser um inteiro positivo")
        self._id_tecnico = value


    # --------- UTILIDADE ---------
    def to_dict(self):
        return {
            "id": self._id,
            "descricao": self._descricao,
            "horas_trabalhadas": float(self._horas_trabalhadas),
            "custo_total": float(self._custo_total),
            # Converte a data (objeto date) para string ISO (YYYY-MM-DD)
            "data": self._data.isoformat() if hasattr(self._data, 'isoformat') else str(self._data),
            "id_os": self._id_os,
            "id_tecnico": self._id_tecnico,
            # Converte o dicionário de peças usadas numa lista de objetos para o frontend
            # Assume-se que pecas_usadas é {id_peca: quantidade} ou {id_peca: {dados}}
            "pecas_usadas": [
                {
                    "id_peca": id_p,
                    "quantidade": dados["quantidade"] if isinstance(dados, dict) else dados,
                    "preco_unitario": float(dados.get("preco_unitario", 0.0)) if isinstance(dados, dict) else 0.0
                }
                for id_p, dados in self._pecas_usadas.items()
            ] if self._pecas_usadas else []
        }