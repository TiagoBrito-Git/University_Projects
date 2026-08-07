Feature: Gestão de stock (US11)
  Como gestor
  Quero gerir o inventário de peças
  Para garantir a disponibilidade de materiais nas reparações

  Scenario: Criar peça com nível mínimo de stock retorna código 201
    Given estou autenticado como administrador
    When crio uma peça com stock e nível mínimo definidos
    Then a resposta tem código 201
    And a peça aparece na listagem com o nível mínimo correto

  Scenario: Atualizar manualmente o stock de uma peça retorna código 200
    Given existe uma peça de stock no sistema
    When o administrador atualiza o stock dessa peça
    Then a resposta tem código 200
