# Plataforma SaaS para Validação Regulatória

Esta solução fornece uma base completa para um SaaS de validação de arquivos regulatórios 
dirigido a empresas do ecossistema de meios de pagamento (adquirentes, subadquirentes e 
emissores). A plataforma contempla layouts exigidos pelo **BACEN**, **DIMP (TED/TEF)** e **DIRF**, 
permitindo que as instituições validem seus arquivos antes do envio oficial.

## Visão Geral da Arquitetura

- **FastAPI** expõe endpoints REST para cadastro de instituições e submissão de arquivos.
- **Armazenamento em memória** (substituível por banco relacional) controla organizações, uploads e resultados.
- **Camada de serviços** orquestra a validação usando uma coleção de validadores plugáveis.
- **Validadores declarativos** implementam layouts pré-configurados para BACEN, DIMP e DIRF.

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

A API ficará disponível em `http://localhost:8000`. Utilize ferramentas como `curl` ou `HTTPie`
para interagir com as rotas.

### Rotas principais

- `POST /organizations` – cadastra uma instituição (adquirente, subadquirente ou emissor).
- `GET /organizations` – lista instituições cadastradas.
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
2. **Dashboard web** para visualização de resultados de validação e trilhas de auditoria.
3. **Suporte a filas** (ex.: RabbitMQ) para processar arquivos volumosos de forma assíncrona.
4. **Catálogo de layouts configurável** permitindo atualização sem deploys.

Com estes elementos, a plataforma oferece uma base robusta para atender às exigências
regulatórias dos participantes do mercado de meios de pagamento.
