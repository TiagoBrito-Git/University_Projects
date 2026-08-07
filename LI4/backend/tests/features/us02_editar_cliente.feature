Feature: Editar cliente (US02)
  Como secretaria
  Quero editar os dados de um cliente registado
  Para manter as informações sempre atualizadas

  Scenario: Editar dados de um cliente existente retorna código 200
    Given existe um cliente registado com um NIF
    When o administrador edita os dados desse cliente
    Then a resposta tem código 200

  Scenario: Editar cliente inexistente retorna código 404
    Given estou autenticado como administrador
    When o administrador tenta editar um cliente inexistente
    Then a resposta tem código 404
