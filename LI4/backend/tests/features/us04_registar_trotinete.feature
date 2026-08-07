Feature: Registar trotinete (US04)
  Como secretaria
  Quero registar uma trotinete associada a um cliente
  Para que possa ser associada a ordens de serviço

  Scenario: Trotinete criada com dados válidos retorna código 201
    Given existe um cliente registado com um NIF
    When registo uma trotinete para esse cliente
    Then a resposta tem código 201
    And a trotinete aparece na listagem

  Scenario: Número de série duplicado é rejeitado com código 400
    Given existe uma trotinete registada com uma série
    When registo outra trotinete com a mesma série
    Then a resposta tem código 400
