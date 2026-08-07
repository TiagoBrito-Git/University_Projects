Feature: Consultar faturas (US12)
  Como gestor
  Quero consultar as faturas emitidas
  Para controlar a faturação do negócio

  Scenario: Listar faturas retorna código 200
    Given estou autenticado como administrador
    When consulto a listagem de faturas
    Then a resposta tem código 200

  Scenario: Download de fatura inexistente retorna código 404
    Given estou autenticado como administrador
    When faço download de uma fatura inexistente
    Then a resposta tem código 404
