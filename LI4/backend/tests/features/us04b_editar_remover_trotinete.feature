Feature: Editar e remover trotinete (US04b)
  Como secretaria
  Quero editar e remover trotinetes registadas
  Para manter o inventário de equipamentos atualizado

  Scenario: Editar dados de uma trotinete existente retorna código 200
    Given existe uma trotinete registada com uma série
    When edito os dados dessa trotinete
    Then a resposta tem código 200

  Scenario: Editar trotinete inexistente retorna código 404
    Given estou autenticado como administrador
    When edito uma trotinete inexistente
    Then a resposta tem código 404

  Scenario: Remover trotinete sem ordens de serviço retorna código 200
    Given existe uma trotinete sem OS associadas
    When o administrador remove essa trotinete pelo id
    Then a resposta tem código 200

  Scenario: Remover trotinete inexistente retorna código 404
    Given estou autenticado como administrador
    When o administrador remove uma trotinete inexistente
    Then a resposta tem código 404
