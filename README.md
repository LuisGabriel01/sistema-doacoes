# Projeto Integrador 1, DRP05, Grupo 3N9

## Especificações

aqui podemos anotar os detalhes e requisitos do projeto.
Por enquanto fica aqui o mockup que a Emilia montou no AppLab.
A imagem representa uma ficha de cadastro de uma família assistida pelo projeto:

![Mockup da ficha de cadastro de uma familia](./doc-imagens/mockup-ficha-familia.jpeg)

## Como clonar e rodar o projeto

> ATENÇÃO: Se estiver usando Windows, confira as instruções de como instalar o
[Python e Git](./README-WINDOWS.md)

### Clonar o projeto

Escolha uma pasta onde vai deixar seus projetos, por exemplo Documentos\projetos
e rode o git clone dentro dela (pra mudar de pasta veja as [instruções pro Windows](/README-WINDOWS.md#abrindo-o-git-bash-e-mudando-de-pasta)):

```console
git clone https://github.com/LuisGabriel01/sistema-doacoes
```

Depois disso mudar para a pasta do projeto com:

```console
cd sistema-doacoes
```

### a primeira vez, criar o `venv`

```shell
python -m venv .venv
```

### rodando o projeto

#### sempre que for mexer

tem que fazer a ativação do ambiente virtual do Python (`venv`)

##### no Linux

```shell
source .venv/bin/activate
```

##### no Windows (Git Bash)

```shell
source .venv\Scripts\activate
```

#### instalar as dependências

apenas uma vez, ou quando alterarmos as dependências

```shell
pip install .
```

as dependências ficam anotadas no arquivo `pyproject.toml`

#### rodar o projeto

com o `venv` ativado (por enquanto ainda não tem nada)

```shell
flask run
```

#### pra gerar o gráfico do ERM abaixo

usamos a biblioteca `paracelsus`. as configurações estão no arquivo
`pyproject.toml` também.

```shell
paracelsus graph
```

o resultado é um código que gera um gráfico `mermaid`, da pra ver abrindo
o código-fonte deste arquivo `README.md`

### esboço do ERM (Modelo Relacional de Entidades) do Banco de Dados

> **pessoal, ignorem a tabela `user` ela tem todos esses campos pq é gerada
> automaticamente pela biblioteca**

```mermaid
erDiagram
  assistido {
    INTEGER id PK
    VARCHAR email
    VARCHAR endereco
    VARCHAR nome UK
    INTEGER quant_familia
    VARCHAR telefone
  }

  categoria_item {
    INTEGER id PK
    VARCHAR nome UK
  }

  coleta {
    INTEGER id PK
    INTEGER doador_id FK "nullable"
    INTEGER instituicao_id FK
    DATETIME data_hora
  }

  doador {
    INTEGER id PK
    VARCHAR email
    VARCHAR endereco
    VARCHAR nome UK
    VARCHAR telefone
  }

  entrega {
    INTEGER id PK
    INTEGER assistido_id FK "nullable"
    INTEGER instituicao_id FK
    DATETIME data_hora
  }

  instituicao {
    INTEGER id PK
    VARCHAR email
    VARCHAR endereco
    VARCHAR nome UK
    VARCHAR telefone
  }

  item {
    INTEGER id PK
    INTEGER assistido_id FK "nullable"
    INTEGER coleta_id FK "nullable"
    INTEGER doador_id FK "nullable"
    INTEGER entrega_id FK "nullable"
    INTEGER instituicao_id FK "nullable"
    INTEGER nome_id FK
    ENUM status
  }

  nome_item {
    INTEGER id PK
    INTEGER categoria_id FK
    VARCHAR nome UK
  }

  role {
    INTEGER id PK
    VARCHAR(255) description "nullable"
    VARCHAR(80) name UK
    TEXT permissions "nullable"
    DATETIME update_datetime
  }

  roles_users {
    INTEGER role_id PK,FK
    INTEGER user_id PK,FK
  }

  user {
    INTEGER id PK
    BOOLEAN active
    DATETIME confirmed_at "nullable"
    DATETIME create_datetime
    DATETIME current_login_at "nullable"
    VARCHAR(64) current_login_ip "nullable"
    VARCHAR(255) email UK
    VARCHAR(64) fs_uniquifier UK
    VARCHAR(64) fs_webauthn_user_handle UK "nullable"
    DATETIME last_login_at "nullable"
    VARCHAR(64) last_login_ip "nullable"
    INTEGER login_count "nullable"
    TEXT mf_recovery_codes "nullable"
    VARCHAR(255) password "nullable"
    VARCHAR(128) tf_phone_number "nullable"
    VARCHAR(64) tf_primary_method "nullable"
    VARCHAR(255) tf_totp_secret "nullable"
    DATETIME update_datetime
    VARCHAR(128) us_phone_number UK "nullable"
    TEXT us_totp_secrets "nullable"
    VARCHAR(255) username UK "nullable"
  }

  instituicao ||--o{ coleta : instituicao_id
  doador ||--o{ coleta : doador_id
  instituicao ||--o{ entrega : instituicao_id
  assistido ||--o{ entrega : assistido_id
  nome_item ||--o{ item : nome_id
  coleta ||--o{ item : coleta_id
  entrega ||--o{ item : entrega_id
  doador ||--o{ item : doador_id
  instituicao ||--o{ item : instituicao_id
  assistido ||--o{ item : assistido_id
  categoria_item ||--o{ nome_item : categoria_id
  user ||--o| roles_users : user_id
  role ||--o| roles_users : role_id
```

.
