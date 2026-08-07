Feature: Decisão do cliente sobre orçamento (US10)
  Como secretaria
  Quero registar a decisão do cliente sobre o orçamento
  Para prosseguir ou cancelar a reparação

  Scenario: Cliente aprova orçamento e OS avança para "Em Reparação"
    Given existe uma OS em "Aguarda Resposta"
    When o cliente aprova o orçamento
    Then a resposta tem código 200

  Scenario: Cliente recusa orçamento e OS é cancelada
    Given existe uma OS em "Aguarda Resposta"
    When o cliente recusa o orçamento
    Then a resposta tem código 200

  Scenario: Decisão inválida é rejeitada com código 400
    Given existe uma OS em "Aguarda Resposta"
    When registo uma decisão inválida do cliente
    Then a resposta tem código 400
