Feature: Validação de estado para intervenções (US16)
  Como técnico
  Quero registar intervenções apenas em ordens em reparação
  Para que o sistema impeça registos com estado inválido

  Scenario: Registar intervenção em OS fora de "Em Reparação" é rejeitado com código 400
    Given existe uma OS no estado "Aguarda Diagnóstico"
    When o técnico tenta registar uma intervenção nessa OS
    Then a resposta tem código 400

  Scenario: Registar intervenção em OS no estado "Em Reparação" retorna código 200
    Given existe uma OS em "Em Reparação"
    When o técnico regista uma intervenção nessa OS
    Then a resposta tem código 200
