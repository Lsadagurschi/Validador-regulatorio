# Plataforma SaaS para Validação Regulatória

Esta solução fornece uma base completa para um SaaS de validação de arquivos regulatórios
dirigido a empresas do ecossistema de meios de pagamento (adquirentes, subadquirentes e
emissores). A plataforma contempla layouts exigidos pelo **BACEN**, **DIMP (TED/TEF)**,
**DIRF** e **CADOC (3040, 3050, 6334)**, permitindo que as instituições validem seus
arquivos antes do envio oficial.

## Visão Geral da Arquitetura

- **Frontend responsivo** em HTML/CSS/JavaScript consome a API e oferece dashboard operacional.
- **FastAPI** expõe endpoints REST para cadastro de instituições e submissão de arquivos.
- **Armazenamento em memória** (substituível por banco relacional) controla organizações, uploads e resultados.
- **Camada de serviços** orquestra a validação usando uma coleção de validadores plugáveis.
- **Validadores declarativos** implementam layouts pré-configurados para BACEN, DIMP, DIRF e CADOC.

```
+--------------------+        +-------------------+        +---------------------+
| Cliente (SaaS)     | -----> | FastAPI (API REST)| -----> | Serviço de Validação|
+--------------------+        +-------------------+        +----------+----------+
                                                                | Registros       
                                                                v                
                                                     +-----------------------+
                                                     | Banco/Storage (adaptável)|
                                                     +-----------------------+
```

## Como executar localmente

```bash
uvicorn validator_saas.api.main:app --reload
```

A API ficará disponível em `http://localhost:8000` e a interface web em
`http://localhost:8000/app/`. Utilize o frontend para realizar cadastros e submeter
arquivos ou ferramentas como `curl`/`HTTPie` para testes manuais das rotas.

### Rotas principais

- `POST /organizations` – cadastra uma instituição (adquirente, subadquirente ou emissor).
- `GET /organizations` – lista instituições cadastradas.
- `GET /validators` – lista o catálogo de validadores com metadados do layout.
- `POST /validations` – recebe um arquivo CSV (upload multipart/form-data) e dispara a validação.

### Exemplo de requisição de validação

```bash
http --form POST :8000/validations \
  organization_id==1 \
  regulator=bacen \
  layout_version=1.0 \
  file@dados_bacen.csv
```

## Estrutura dos Layouts

Os validadores utilizam uma camada declarativa para garantir que cada linha do arquivo
respeite os campos, formatos e comprimentos exigidos. A tabela a seguir destaca os campos
principais de cada regulatório implementado:

| Regulatório | Campos principais |
|-------------|-------------------|
| BACEN       | `codigo_registro`, `cnpj_instituicao`, `tipo_produto`, `valor_transacao`, `data_transacao`, `quantidade_transacoes` |
| DIMP (TED/TEF) | `codigo_registro`, `cnpj_participante`, `modalidade`, `valor_total`, `quantidade_operacoes`, `data_referencia` |
| DIRF        | `tipo_registro`, `cnpj_fonte_pagadora`, `cpf_beneficiario`, `cnpj_beneficiario`, `valor_rendimento`, `imposto_retido`, `ano_calendario` |
| CADOC 3040  | `tipo_registro`, `cnpj_instituicao`, `codigo_produto`, `saldo_ativo`, `saldo_passivo`, `data_base` |
| CADOC 3050  | `tipo_registro`, `cnpj_instituicao`, `codigo_modalidade`, `valor_exposicao`, `prazo_medio_dias`, `indice_cobertura` |
| CADOC 6334  | `tipo_registro`, `cnpj_participante`, `codigo_servico`, `quantidade_operacoes`, `valor_total`, `canal_atendimento`, `data_referencia` |

## Interface Web

O frontend está disponível em `/app/` e oferece as seguintes funcionalidades:

- Cadastro de instituições com feedback instantâneo.
- Listagem dinâmica de instituições registradas na API.
- Catálogo visual dos validadores disponíveis, com descrição dos campos exigidos.
- Upload de arquivos CSV para validação com exibição tabular das inconsistências.

Os assets estáticos residem em `frontend/` e são servidos diretamente pelo FastAPI via
`StaticFiles`, permitindo deploy simples sem build steps adicionais.

## Testes automatizados

Instale as dependências de desenvolvimento e execute os testes:

```bash
pip install -e .[dev]
pytest
```

Os testes cobrem cenários de sucesso e de falha, garantindo que o motor de validação identifique
inconsistências e registre relatórios adequadamente.

## Próximos passos sugeridos

1. **Autenticação multi-tenant** com OAuth2 e segmentação de dados por cliente.
2. **Persistência** em banco relacional para manter histórico de runs e issues.
3. **Processamento assíncrono** com filas (ex.: RabbitMQ) para grandes volumes.
4. **Layout Builder** para permitir ajustes via painel administrativo.

Com estes elementos, a plataforma oferece uma base robusta para atender às exigências
regulatórias dos participantes do mercado de meios de pagamento.
