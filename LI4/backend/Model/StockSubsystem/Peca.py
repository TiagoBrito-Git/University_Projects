class Peca:
    def __init__(self, id, nome, descricao, fornecedor, categoria, preco, stock, quantidade_minima):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._fornecedor = fornecedor
        self._categoria = categoria
        self._preco = preco
        self._stock = stock
        self._quantidade_minima = quantidade_minima

    # --------- ID ---------
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    # --------- NOME ---------
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        if not value:
            raise ValueError("Nome não pode ser vazio")
        self._nome = value

    # --------- DESCRIÇÃO ---------
    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, value):
        self._descricao = value


    # --------- Fornecedor ---------
    @property
    def fornecedor(self):
        return self._fornecedor

    @fornecedor.setter
    def fornecedor(self, value):
        self._fornecedor = value


    # --------- Categoria ---------
    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, value):
        self._categoria = value

    # --------- PREÇO ---------
    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, value):
        if value < 0:
            raise ValueError("Preço não pode ser negativo")
        self._preco = value

    # --------- STOCK ---------
    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        if value < 0:
            raise ValueError("Stock não pode ser negativo")
        self._stock = value

    # --------- STOCK MÍNIMO ---------
    @property
    def quantidade_minima(self):
        return self._quantidade_minima

    @quantidade_minima.setter
    def quantidade_minima(self, value):
        if value < 0:
            raise ValueError("Minimum level não pode ser negativo")
        self._quantidade_minima = value

    def to_dict(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "descricao": self._descricao,
            "fornecedor": self._fornecedor,
            "categoria": self._categoria,
            "preco": self._preco,
            "stock": self._stock,
            "quantidade_minima": self._quantidade_minima
        }