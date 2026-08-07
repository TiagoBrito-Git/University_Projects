CREATE DATABASE IF NOT EXISTS scooterfix
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE scooterfix;
CREATE TABLE IF NOT EXISTS utilizadores (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome varchar (255) NOT NULL,
    username varchar (255) NOT NULL UNIQUE,
    password_hash varchar (255) NOT NULL,
    password_salt varchar (255) NOT NULL,
    perfil ENUM(
        'administrador',
        'tecnico',
        'secretaria',
        'gestor'
    ) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_registo DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome varchar (255) NOT NULL,
    nif varchar (20) NOT NULL UNIQUE,
    contacto varchar (20),
    email varchar (255),
    morada varchar (255)
);

CREATE TABLE IF NOT EXISTS trotinetes (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    marca varchar (255) NOT NULL,
    modelo varchar (255) NOT NULL,
    numero_serie varchar (255) NOT NULL UNIQUE,
    data_registo DATE NOT NULL,
    id_cliente INT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS ordem_de_servico (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    data_abertura DATE NOT NULL,
    data_conclusao DATE,
    estado varchar (50) NOT NULL DEFAULT 'Aguarda Diagnóstico',
    descricao TEXT NOT NULL,
    id_trotinete INT NOT NULL,
    id_tecnico INT NOT NULL,
    id_cliente INT NOT NULL,
    FOREIGN KEY (id_trotinete) REFERENCES trotinetes(id),
    FOREIGN KEY (id_tecnico) REFERENCES utilizadores(id),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS diagnostico (
    id INT PRIMARY KEY AUTO_INCREMENT,
    descricao TEXT,
    orcamentoEstimado DECIMAL(10,2),
    horasMaoDeObra DECIMAL(6,2),
    data DATE,
    decisaoCliente VARCHAR(255),
    dataDecisao DATE,
    idOS INT,
    idTecnico INT,
    
    CONSTRAINT fk_diagnostico_os
        FOREIGN KEY (idOS) 
        REFERENCES ordem_de_servico(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_diagnostico_tecnico
        FOREIGN KEY (idTecnico) 
        REFERENCES utilizadores(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);




CREATE TABLE IF NOT EXISTS intervencoes (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    descricao TEXT NOT NULL,
    horas_trabalho DECIMAL(6,2) NOT NULL DEFAULT 0.00,
    data_ DATE NOT NULL,
    custo_total DECIMAL(6,2),
    id_os INT NOT NULL,
    id_tecnico INT NOT NULL,
    FOREIGN KEY (id_os) REFERENCES ordem_de_servico(id),
    FOREIGN KEY (id_tecnico) REFERENCES utilizadores(id)
);


CREATE TABLE IF NOT EXISTS pecas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    fornecedor VARCHAR(255) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    quantidade_minima INT NOT NULL
);


CREATE TABLE IF NOT EXISTS intervencao_peca (
    idIntervencaoPeca INT AUTO_INCREMENT PRIMARY KEY,
    idIntervencao INT NOT NULL,
    idPeca INT NOT NULL,
    quantidade INT NOT NULL,
    precoUnitario DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_intervencao_peca_intervencao
        FOREIGN KEY (idIntervencao)
        REFERENCES intervencoes(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_intervencao_peca_peca
        FOREIGN KEY (idPeca)
        REFERENCES pecas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS diagnostico_peca (
    idDiagnosticoPeca INT AUTO_INCREMENT PRIMARY KEY,
    idDiagnostico INT NOT NULL,
    idPeca INT NOT NULL,
    quantidade INT NOT NULL,
    precoUnitario DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_diagnostico_peca_diagnostico
        FOREIGN KEY (idDiagnostico)
        REFERENCES diagnostico(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_diagnostico_peca_peca
        FOREIGN KEY (idPeca)
        REFERENCES pecas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS fatura (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    numero varchar (50) NOT NULL UNIQUE,
    data_emissao DATE NOT NULL, 
    subtotal_pecas DECIMAL(10,2) NOT NULL,
    subtotal_mao_obra DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    estado varchar (20) NOT NULL DEFAULT 'Pendente',
    tipo_pagamento varchar (20) NOT NULL,
    id_os INT NOT NULL,
    FOREIGN KEY (id_os) REFERENCES ordem_de_servico(id)
);

-- Substituir a fatura_peca existente por:
CREATE TABLE IF NOT EXISTS fatura_peca (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    id_fatura     INT NOT NULL,
    id_peca       INT NOT NULL,
    quantidade    INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_fatura_peca_fatura
        FOREIGN KEY (id_fatura) REFERENCES fatura(id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_fatura_peca_peca
        FOREIGN KEY (id_peca) REFERENCES pecas(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS perfis_permissoes (
    perfil VARCHAR(50) NOT NULL,
    permissao VARCHAR(100) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (perfil, permissao)
);

CREATE TABLE IF NOT EXISTS relatorios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    caminho VARCHAR(500) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
