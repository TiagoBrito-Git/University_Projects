Feature: Criar ordem de serviço (US06)
  Como secretaria
  Quero criar uma nova ordem de serviço associada a uma trotinete existente
  Para que o processo de reparação fique formalmente registado

  Scenario: OS criada com estado inicial correto
    Given estou autenticado como administrador
    When crio uma OS para um cliente e trotinete existentes
    Then a resposta tem código 201
    And a OS é criada com estado "Aguarda Diagnóstico"

  Scenario: Trotinete inexistente impede criação com código 404
    Given estou autenticado como administrador
    When crio uma OS com número de série inexistente
    Then a resposta tem código 404

  Scenario: Cliente inexistente impede criação com código 404
    Given estou autenticado como administrador
    When crio uma OS com NIF de cliente inexistente
    Then a resposta tem código 404
