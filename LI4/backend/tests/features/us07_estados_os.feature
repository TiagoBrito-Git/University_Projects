Feature: Estados da ordem de serviço (US07)
  Como secretaria
  Quero atualizar o estado de uma OS respeitando o fluxo definido
  Para que o sistema impeça transições inválidas

  Scenario: Transição de estado inválida é rejeitada com código 400
    Given existe uma OS no estado "Aguarda Diagnóstico"
    When avanço o estado para "Em Reparação" directamente
    Then a resposta tem código 400

  Scenario: Avançar estado de OS inexistente retorna código 400
    Given estou autenticado como administrador
    When avanço o estado de uma OS inexistente
    Then a resposta tem código 400
