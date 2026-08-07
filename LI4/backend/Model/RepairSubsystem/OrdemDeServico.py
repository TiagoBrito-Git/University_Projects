from datetime import date

ESTADOS_VALIDOS = [
    "Aguarda Diagnóstico", "Aguarda Resposta", "Em Reparação",
    "Concluído", "Aguarda Faturação", "Faturada", "Encerrada", "Cancelada",
]


class OrdemDeServico:
    def __init__(
        self,
        id: int,
        data_abertura: date,
        data_conclusao: date,
        estado: str,
        descricao: str,
        id_trotinete: int,
        id_tecnico: int,
        id_cliente: int
    ):
        self._id = id
        self._data_abertura = data_abertura
        self._data_conclusao = data_conclusao
        self._estado = estado
        self._descricao = descricao
        self._id_trotinete = id_trotinete
        self._id_tecnico = id_tecnico
        self._id_cliente = id_cliente

    # ID
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    # Data abertura
    @property
    def data_abertura(self):
        return self._data_abertura

    @data_abertura.setter
    def data_abertura(self, value):
        self._data_abertura = value

    # Data conclusão
    @property
    def data_conclusao(self):
        return self._data_conclusao

    @data_conclusao.setter
    def data_conclusao(self, value):
        self._data_conclusao = value

    # Estado
    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self.set_estado(value)

    def set_estado(self, estado: str):
        if estado not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: '{estado}'. Válidos: {', '.join(ESTADOS_VALIDOS)}")
        self._estado = estado

    # Descrição
    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, value):
        self.set_descricao(value)

    def set_descricao(self, descricao: str):
        if not descricao or not descricao.strip():
            raise ValueError("Descrição da OS não pode estar vazia.")
        self._descricao = descricao

    # ID Trotinete
    @property
    def id_trotinete(self):
        return self._id_trotinete

    @id_trotinete.setter
    def id_trotinete(self, value):
        self.set_id_trotinete(value)

    def set_id_trotinete(self, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError("ID da trotinete inválido.")
        self._id_trotinete = value

    # ID Técnico
    @property
    def id_tecnico(self):
        return self._id_tecnico

    @id_tecnico.setter
    def id_tecnico(self, value):
        self.set_id_tecnico(value)

    def set_id_tecnico(self, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError("ID do técnico inválido.")
        self._id_tecnico = value

    # ID Cliente
    @property
    def id_cliente(self):
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, value):
        self._id_cliente = value


    def to_dict(self):
        return {
            "id": self._id,
            "data_abertura": self._data_abertura.isoformat() if hasattr(self._data_abertura, 'isoformat') else str(self._data_abertura),
            "data_conclusao": self._data_conclusao.isoformat() if self._data_conclusao else None,
            "estado": self._estado,
            "descricao": self._descricao,
            "id_trotinete": self._id_trotinete,
            "id_tecnico": self._id_tecnico,
            "id_cliente": self._id_cliente
        }
