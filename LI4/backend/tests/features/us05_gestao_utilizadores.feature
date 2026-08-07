Feature: Gestão de utilizadores (US05)
  Como administrador
  Quero gerir contas de utilizador
  Para controlar o acesso ao sistema

  Scenario: Administrador edita o nome de um utilizador existente
    Given existe um utilizador técnico no sistema
    When o administrador edita o nome desse utilizador
    Then a resposta tem código 200

  Scenario: Administrador desativa conta de utilizador
    Given existe um utilizador técnico no sistema
    When o administrador desativa esse utilizador
    Then a resposta tem código 200

  Scenario: Não é possível desativar a própria conta de administrador
    Given estou autenticado como administrador
    When o administrador tenta desativar a própria conta
    Then a resposta tem código 400
