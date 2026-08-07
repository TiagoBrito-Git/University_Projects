Feature: Perfis de acesso (US24)
  Como administrador
  Quero que cada perfil aceda apenas às funcionalidades que lhe competem
  Para que os dados sensíveis fiquem protegidos

  Scenario: Técnico não pode criar cliente e recebe código 403
    Given estou autenticado como técnico
    When registo um cliente com dados válidos
    Then a resposta tem código 403

  Scenario: Técnico pode consultar a lista de clientes
    Given estou autenticado como técnico
    When consulto a lista de clientes
    Then a resposta tem código 200

  Scenario: Secretaria não pode criar peças de stock e recebe código 403
    Given estou autenticado como secretaria
    When registo uma nova peça de stock
    Then a resposta tem código 403

  Scenario: Administrador pode criar peças de stock
    Given estou autenticado como administrador
    When registo uma nova peça de stock
    Then a resposta tem código 201
