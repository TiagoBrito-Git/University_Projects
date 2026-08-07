Feature: Remover cliente (US03)
  Como secretaria
  Quero remover o registo de um cliente que já não utiliza os serviços
  Para que a base de dados não contenha registos desnecessários

  Scenario: Cliente sem histórico é apagado da base de dados
    Given existe um cliente sem ordens de serviço associadas
    When o administrador remove esse cliente
    Then a resposta tem código 200
    And o cliente deixa de existir na listagem

  Scenario: Remover cliente inexistente retorna código 404
    Given estou autenticado como administrador
    When o administrador tenta remover um cliente inexistente
    Then a resposta tem código 404
