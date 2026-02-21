# End-to-End Data Engineering Pipeline: Yelp Lakehouse Architecture

## 1. Sobre o Projeto
Este projeto demonstra a implementação de uma arquitetura de dados moderna (Modern Data Stack) para processar grandes volumes de dados estruturados e semiestruturados do ecossistema Yelp. O objetivo principal é construir um ambiente de **Data Lakehouse** que automatiza a jornada do dado desde o armazenamento bruto (Data Lake) até a camada analítica final (Data Warehouse) seguindo a metodologia de **Kimball**.

### Cenário de Negócio
Imagine uma consultoria que precisa analisar o comportamento de usuários e a evolução de estabelecimentos comerciais. O desafio é que esses dados chegam em formatos distintos (JSONs complexos e tabelas CSV) e precisam ser consolidados para permitir análises históricas precisas, como mudanças em categorias de negócios e evolução de notas (SCD Tipo 2).

## 2. Objetivos Técnicos
* **Ingestão Automatizada:** Desenvolver scripts em Python para orquestrar o upload de dados para a nuvem.
* **Arquitetura Medalhão:** Organizar os dados em camadas (Bronze/Staging, Silver/Cleaned, Gold/Star Schema).
* **Processamento de Semi-estruturados:** Utilizar o tipo `VARIANT` do Snowflake para tratar dados aninhados sem perda de performance.
* **Processamento de 7 Milhões de Registros:** Demonstração de capacidade técnica para lidar com Big Data (5.3 GB de reviews).
* **Modelagem Dimensional:** Implementar um **Star Schema** (Fatos e Dimensões) otimizado para consultas analíticas.
* **Histórico de Dados:** Gerenciar mudanças de estado utilizando **Slowly Changing Dimensions (SCD)**.
* **Idempotência e Automação:** Garantir que o pipeline possa ser reexecutado sem duplicidade e que novos dados sejam processados automaticamente.

## 3. Stack Tecnológica
* **Linguagem:** Python 3
* **Cloud Storage (Data Lake):** Azure Blob Storage (Camada Bronze)
* **Data Warehouse:** Snowflake (Edição Enterprise)
* **Transformação de Dados:** SQL & Snowflake Tasks/Streams
* **Modelagem:** Metodologia Kimball (Star Schema)
* **Ferramenta de Desenvolvimento:** VSCode no macOS

## 4. Ingestão e Performance (Bronze Layer)
A carga dos dados brutos foi realizada utilizando o comando `COPY INTO` do Snowflake, integrando o Azure Blob Storage como External Stage para uma ingestão de alto desempenho.

| Dataset | Volume de Dados | Registros Carregados | Tempo de Processamento |
| :--- | :--- | :--- | :--- |
| **Business** | 118 MB | 150.346 | 11 segundos |
| **Review** | 5.3 GB | 6.990.280 | 9 minutos   |

*Os dados foram validados via consultas de agregação, confirmando uma média de 3.74 estrelas e registros datados de 2005 a 2022.*

## 5. Metodologia de Desenvolvimento e Custos
Para este projeto, optou-se por uma estratégia de **Sampling (Amostragem)** dos dados originais do Yelp:
* **Dados Semiestruturados:** Carga integral dos arquivos Business, Review e User para permitir análise de Star Schema completa.
* **Dados Não Estruturados:** Seleção manual de uma amostra representativa de imagens para demonstrar a capacidade de gerenciamento de binários via Snowflake Directory Tables, mantendo o projeto dentro da camada gratuita da Azure (Free Tier).

## 6. Estrutura do Repositório
```text
.
├── data/               # Arquivos locais (não versionados no Git)
├── docs/               # Documentação técnica e diagramas
├── scripts/            # Scripts Python para ingestão (Azure Upload)
├── sql/                # Scripts Snowflake (Bronze, Silver, Gold)
├── requirements.txt    # Dependências do projeto (pip install)
└── README.md           # Documentação principal
```

## 7. Decisões de Engenharia
### Camada Bronze no Cloud Storage

A escolha de utilizar o **Azure Blob Storage** como camada inicial (Bronze) justifica-se pela necessidade de um **Data Lake** imutável. Isso garante a preservação dos dados originais e permite que o Snowflake utilize **External Stages** para uma ingestão escalável.

### Uso da Edição Enterprise

A utilização da edição Enterprise do Snowflake é estratégica, permitindo o uso de Time Travel estendido (até 90 dias) e Materialized Views, fundamentais para auditoria e performance em ambientes produtivos.

## 8. Desafios de Dados Semiestruturados
O dataset do Yelp apresenta campos complexos e aninhados (ex: attributes e hours), que não seguem um esquema rígido.

* **Estratégia:** Utilizaremos o tipo de dado `VARIANT` do Snowflake na camada **Bronze** (Schema-on-Read).

* **Transformação:** A extração para colunas relacionais ocorrerá na camada **Silver** via funções `FLATTEN` e notação de ponto.