Feature: Diagnóstico de ordem de serviço (US09)
  Como técnico
  Quero registar o diagnóstico de uma trotinete em reparação
  Para avaliar e orçamentar o trabalho necessário

  Scenario: Diagnóstico registado em OS válida retorna código 200
    Given existe uma OS no estado "Aguarda Diagnóstico"
    When o técnico regista um diagnóstico nessa OS
    Then a resposta tem código 200

  Scenario: OS sem diagnóstico não pode avançar para "Aguarda Resposta"
    Given existe uma OS no estado "Aguarda Diagnóstico"
    When tento avançar a OS para "Aguarda Resposta" sem diagnóstico
    Then a resposta tem código 400
