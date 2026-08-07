class Relatorio:
    def __init__(self, id, titulo, caminho, tipo):
        self._id = id
        self._titulo = titulo
        self._caminho = caminho
        self._tipo = tipo

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        if not valor:
            raise ValueError("O título não pode estar vazio.")
        self._titulo = valor

    @property
    def caminho(self):
        return self._caminho

    @caminho.setter
    def caminho(self, valor):
        self._caminho = valor

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        self._tipo = valor