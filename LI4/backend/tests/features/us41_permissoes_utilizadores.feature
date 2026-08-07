Feature: Permissões de criação de utilizadores (US41)
  Como administrador do sistema
  Quero que apenas perfis autorizados possam criar utilizadores
  Para controlar o acesso ao sistema

  Scenario: Técnico não pode criar utilizadores e recebe código 403
    Given estou autenticado como técnico
    When tento criar um utilizador com perfil técnico
    Then a resposta tem código 403

  Scenario: Secretaria não pode criar utilizadores e recebe código 403
    Given estou autenticado como secretaria
    When tento criar um utilizador com perfil técnico
    Then a resposta tem código 403
