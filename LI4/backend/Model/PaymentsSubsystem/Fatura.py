from datetime import date


class Fatura:
    """
    Representa uma fatura emitida para uma Ordem de Serviço.

    Atributo 'pecas':
        dict[int, dict] onde a chave é o id_peca (int) e o valor é um dicionário:
        {
            "nome":           str,   -- nome da peça (para apresentação/PDF)
            "quantidade":     int,
            "preco_unitario": float,
            "subtotal":       float  -- quantidade * preco_unitario
        }

        Padrão consistente com intervencao_peca e diagnostico_peca na base de dados.
        Exemplo:
            {
                3: {"nome": "Roda 8.5\"", "quantidade": 2, "preco_unitario": 35.0, "subtotal": 70.0},
                5: {"nome": "Display LCD", "quantidade": 1, "preco_unitario": 28.0, "subtotal": 28.0},
            }
    """

    ESTADOS_VALIDOS = {"pendente", "paga", "cancelada"}
    TIPOS_PAGAMENTO_VALIDOS = {"dinheiro", "cartão", "transferência"}

    def __init__(
        self,
        id: int,
        numero: str,
        data: date,
        sub_total_pecas: float,
        sub_total_mao_obra: float,
        total: float,
        estado: str,
        tipo_pagamento: str,
        id_os: int,
        pecas: dict = None,
        nome_cliente: str = None,
        nif_cliente: str = None,
        email_cliente: str = None,
        morada_cliente: str = None,
    ):
        self.id = id
        self.numero = numero
        self.data = data
        self.sub_total_pecas = sub_total_pecas
        self.sub_total_mao_obra = sub_total_mao_obra
        self.total = total
        self.estado = estado
        self.tipo_pagamento = tipo_pagamento
        self.id_os = id_os
        self.pecas = pecas if pecas is not None else {}
        self.nome_cliente = nome_cliente
        self.nif_cliente = nif_cliente
        self.email_cliente = email_cliente
        self.morada_cliente = morada_cliente

    # --------- ID ---------
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    # --------- NUMERO ---------
    @property
    def numero(self) -> str:
        return self._numero

    @numero.setter
    def numero(self, value: str):
        if not value or not value.strip():
            raise ValueError("Número não pode estar vazio")
        self._numero = value.strip()

    # --------- DATA ---------
    @property
    def data(self) -> date:
        return self._data

    @data.setter
    def data(self, value: date):
        if not isinstance(value, date):
            raise ValueError("Data deve ser um objeto do tipo date")
        self._data = value

    # --------- SUB TOTAL PEÇAS ---------
    @property
    def sub_total_pecas(self) -> float:
        return self._sub_total_pecas

    @sub_total_pecas.setter
    def sub_total_pecas(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Subtotal de peças não pode ser negativo")
        self._sub_total_pecas = float(value)

    # --------- SUB TOTAL MÃO DE OBRA ---------
    @property
    def sub_total_mao_obra(self) -> float:
        return self._sub_total_mao_obra

    @sub_total_mao_obra.setter
    def sub_total_mao_obra(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Subtotal de mão de obra não pode ser negativo")
        self._sub_total_mao_obra = float(value)

    # --------- TOTAL ---------
    @property
    def total(self) -> float:
        return self._total

    @total.setter
    def total(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Total não pode ser negativo")
        self._total = float(value)

    # --------- ESTADO ---------
    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, value: str):
        # Normaliza para minúsculas — robusto ao valor vindo da BD ("Pendente" → "pendente")
        normalizado = value.lower() if isinstance(value, str) else value
        if normalizado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Valores aceites: {self.ESTADOS_VALIDOS}")
        self._estado = normalizado

    # --------- TIPO PAGAMENTO ---------
    @property
    def tipo_pagamento(self) -> str:
        return self._tipo_pagamento

    @tipo_pagamento.setter
    def tipo_pagamento(self, value: str):
        if value not in self.TIPOS_PAGAMENTO_VALIDOS:
            raise ValueError(f"Tipo de pagamento inválido. Valores aceites: {self.TIPOS_PAGAMENTO_VALIDOS}")
        self._tipo_pagamento = value

    # --------- ID_OS ---------
    @property
    def id_os(self) -> int:
        return self._id_os

    @id_os.setter
    def id_os(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("ID da ordem de serviço deve ser um inteiro positivo")
        self._id_os = value

    # --------- PEÇAS ---------
    @property
    def pecas(self) -> dict:
        return self._pecas

    @pecas.setter
    def pecas(self, value: dict):
        if not isinstance(value, dict):
            raise ValueError("Peças deve ser um dicionário")
        self._pecas = value

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "numero": self._numero,
            "data": self._data.isoformat(),
            "sub_total_pecas": self._sub_total_pecas,
            "sub_total_mao_obra": self._sub_total_mao_obra,
            "total": self._total,
            "estado": self._estado,
            "tipo_pagamento": self._tipo_pagamento,
            "id_os": self._id_os,
            "nome_cliente": self.nome_cliente,
            "nif_cliente": self.nif_cliente,
            "email_cliente": self.email_cliente,
            "morada_cliente": self.morada_cliente,
            "pecas": [
                {
                    "id_peca": id_peca,
                    "nome": dados.get("nome", ""),
                    "quantidade": dados["quantidade"],
                    "preco_unitario": dados["preco_unitario"],
                    "subtotal": dados["quantidade"] * dados["preco_unitario"],
                }
                for id_peca, dados in self._pecas.items()
            ],
        }
