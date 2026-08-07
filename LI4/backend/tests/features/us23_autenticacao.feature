Feature: Autenticação no sistema (US23)
  Como utilizador do sistema
  Quero aceder com as minhas credenciais pessoais
  Para que apenas eu possa realizar operações associadas ao meu perfil

  Scenario: Credenciais inválidas retornam código 401
    When autentico com username "inexistente@test.pt" e password "errada"
    Then a resposta tem código 401

  Scenario: Conta desativada retorna código 403
    Given existe uma conta desativada no sistema
    When autentico com as credenciais dessa conta
    Then a resposta tem código 403

  Scenario: Acesso sem token retorna código 401
    When acedo a um recurso protegido sem token
    Then a resposta tem código 401
