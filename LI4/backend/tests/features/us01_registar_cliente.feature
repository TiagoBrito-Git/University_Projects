Feature: Registar novo cliente (US01)
  Como secretaria
  Quero registar um novo cliente no sistema
  Para que fique disponível para associação a trotinetes e ordens de serviço

  Scenario: Dados válidos são aceites com código 201
    Given estou autenticado como administrador
    When registo um cliente com NIF único e dados completos
    Then a resposta tem código 201
    And o cliente aparece na listagem

  Scenario: NIF duplicado é rejeitado com código 400
    Given existe um cliente registado com um NIF
    When registo outro cliente com o mesmo NIF
    Then a resposta tem código 400

  Scenario: Campos obrigatórios em falta retornam código 422
    Given estou autenticado como administrador
    When registo um cliente sem indicar o NIF
    Then a resposta tem código 422
