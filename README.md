# Desafio Dev - Importação de CNAB

Este é um projeto full-stack para upload e processamento de dados transacionais a partir de arquivos CNAB (Padrão Bycoders 😆). O sistema é capaz de realizar a leitura, conversão de tipagem e normalização de dados antes de salvá-los no banco de dados.

## 1. Setup de Ambiente e Execução Local

O projeto foi inteiramente "dockerizado" para facilitar a execução e garantir um ambiente padronizado.

### Pré-requisitos

- Docker
- Docker Compose

### Passos para rodar

1. Clone o repositório na sua máquina ou acesse o diretório raiz.
2. Copie os arquivos de exemplo para criar seus próprios arquivos de variáveis de ambiente (`.env`):

   ```bash
   cp apps/web/.env.example apps/web/.env
   ```
3. Na raiz do projeto (onde está localizado o arquivo `docker-compose.yml`), execute o comando abaixo no terminal:

```bash
docker compose up --build
```

O comando irá construir e iniciar três containers:

- `db`: Banco de dados PostgreSQL (na porta `5432`).
- `api`: Backend da aplicação (disponibilizado na porta `8000`).
- `web`: Frontend da aplicação (disponibilizado na porta `3000`).

Aguarde até que o log sinalize que os servidores estão rodando.

- O Frontend pode ser acessado em: `http://localhost:3000`
- A documentação interativa (Swagger UI) do Backend pode ser acessada em: `http://localhost:8000/docs`

## 2. Tecnologias Utilizadas (Stack)

### Backend (`apps/api`)

- **Python 3**
- **FastAPI**: Framework web de alta performance para a criação de APIs reativas.
- **Uvicorn**: Servidor ASGI leve e otimizado.
- **PostgreSQL**: Banco de dados relacional.
- **SQLAlchemy**: ORM (Object Relational Mapper) e construtor de SQL para interação com o banco.
- **Pytest**: Framework para implementação e execução de testes automatizados.
- **Pydantic**: Biblioteca para validação de dados garantindo segurança (Type hints).

### Frontend (`apps/web`)

- **React**: Biblioteca Javascript para a construção da interface do usuário.
- **React Router (v7)**: Controle de roteamento na aplicação web.
- **Vite**: Ferramenta de build de extrema velocidade, focada em entregar boa experiência de uso.
- **Tailwind CSS**: Framework CSS para estilização rápida por utility classes.
- **TypeScript**: Superset de tipagem estática que previne erros no desenvolvimento.
- **Axios**: Cliente HTTP para requisições com o backend.

## 3. Documentação da API (Backend)

O backend possui o formato padronizado de envolope (`ResponseEnvelope`) em todas as respostas (em caso de sucesso ou de erro), cuja estrutura é:

- `success`: booleano (`true` ou `false`).
- `data`: os dados de resposta do servidor, caso existam.
- `message`: mensagem explicativa da resposta.
- `error`: descrição ou string do erro, preenchida quando acontece falha na regra de negócio ou erro 500.

### Endpoints

#### Verificação de Funcionamento

- **`GET /health`**
  - **Função**: Checar se a aplicação encontra-se saudável.
  - **Reposta de sucesso (`200`)**: `{"message": "ok"}`

#### Operações com Transações

- **`POST /api/v1/transactions/import`**

  - **Função**: Recebe o arquivo CNAB por um form-data multipart, faz processamento, extrai as transações contidas e insere no banco de dados.
  - **Corpo da requisição (MIME: `multipart/form-data`)**:
    - `file`: O arquivo `.txt` contendo as transações CNAB.
  - **Resposta de sucesso (`201 Created`)**:
    - Retorna a listagem serializada com as transações normalizadas na chave `data`.
- **`GET /api/v1/transactions/`**

  - **Função**: Recupera a listagem plana (array) paginada das transações financeiras.
  - **Parâmetros de Consulta (Query)**:
    - `page` _(integer, default 1)_: A página desejada de resultados.
    - `page_size` _(integer, default 50)_: O número máximo de resultados.
  - **Resposta de sucesso (`200 OK`)**:
    - Traz o `data` fixado como um Array contendo os objetos `OutputTransactionDTO`.
- **`GET /api/v1/transactions/summary`**

  - **Função**: Retorna um sumário completo contendo transações agrupadas explicitamente por Loja (Store), simplificando a confecção de painéis / dashboards focados em saldo.
  - **Parâmetros de Consulta (Query)**:
    - `page` _(integer, default 1)_: A página desejada de resultados.
    - `page_size` _(integer, default 50)_: O número máximo de transações por loja.
  - **Resposta de sucesso (`200 OK`)**:
    - Traz o `data` em formato de Dicionário, onde cada chave é o *Nome da Loja*, contendo as transações que pertencem a ela.

## 4. Como Consumir os Endpoints

Aqui estão exemplos práticos usando `curl` e JavaScript nativo (`fetch`) que demonstram como é feita a interação com a camada de serviços da API.

### A) Consumindo com cURL (Testes via Terminal de Comando)

**Fazer o upload do arquivo CNAB:**
*(Considere que você tem acesso a um arquivo chamado `CNAB.txt` no mesmo diretório do seu terminal)*

```bash
curl -X POST http://localhost:8000/api/v1/transactions/import \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@CNAB.txt"
```

**Listar Transações Paginas:**

```bash
curl -X GET "http://localhost:8000/api/v1/transactions/?page=1&page_size=20" \
  -H "accept: application/json"
```

**Listar Transações Agrupadas por Loja (Dashboard Summary):**
Este endpoint é bastante útil para exibição de dashboard financeiro em uma única visualização.

```bash
curl -X GET "http://localhost:8000/api/v1/transactions/summary?page=1&page_size=50" \
  -H "accept: application/json"
```

### B) Consumindo com JavaScript Nativo (`fetch`)

**Upload do arquivo em requisições de Front-end:**

```javascript
const uploadArquivo = async (fileInputValue) => {
  const formData = new FormData();
  formData.append('file', fileInputValue); // fileInputValue é o objeto literal de tipo File

  try {
    const response = await fetch('http://localhost:8000/api/v1/transactions/import', {
      method: 'POST',
      body: formData,
    });
  
    const result = await response.json();
    console.log(result.data); // transações processadas com envelope desempacotado
  } catch (error) {
    console.error('Erro de envio ou parse', error);
  }
};
```

**Listando saldos agrupados:**

```javascript
const carregarFinanceiro = async () => {
  try {
    const url = new URL('http://localhost:8000/api/v1/transactions/summary');
    url.searchParams.append('page', '1');
    url.searchParams.append('page_size', '50');

    const response = await fetch(url);
    const result = await response.json();
  
    // Validando o envelope e imprimindo no caso de sucesso.
    if(result.success) {
      console.log('Listagem das lojas e seus totais:', result.data);
    }
  } catch (error) {
    console.error('Falha de requisição', error);
  }
}

carregarFinanceiro();
```
