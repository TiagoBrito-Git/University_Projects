from datetime import date


class Trotinete:
    def __init__(self, id: int, marca: str, modelo: str, numero_serie: str, data_registo: date, id_cliente: int):
        self._id = id
        self.set_marca(marca)
        self.set_modelo(modelo)
        self.set_numero_serie(numero_serie)
        self._data_registo = data_registo
        self._id_cliente = id_cliente

    # Getters
    def get_id(self) -> int:
        return self._id

    def get_marca(self) -> str:
        return self._marca

    def get_modelo(self) -> str:
        return self._modelo

    def get_numero_serie(self) -> str:
        return self._numero_serie

    def get_data_registo(self) -> date:
        return self._data_registo

    def get_id_cliente(self) -> int:
        return self._id_cliente

    def set_marca(self, marca: str):
        if not marca or not marca.strip():
            raise ValueError("Marca da trotinete não pode estar vazia.")
        self._marca = marca.strip()

    def set_modelo(self, modelo: str):
        if not modelo or not modelo.strip():
            raise ValueError("Modelo da trotinete não pode estar vazio.")
        self._modelo = modelo.strip()

    def set_numero_serie(self, numero_serie: str):
        if not numero_serie or not numero_serie.strip():
            raise ValueError("Número de série da trotinete não pode estar vazio.")
        self._numero_serie = numero_serie.strip()

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "marca": self._marca,
            "modelo": self._modelo,
            "numero_serie": self._numero_serie,
            "data_registo": self._data_registo.isoformat(),
            "id_cliente": self._id_cliente
        }
