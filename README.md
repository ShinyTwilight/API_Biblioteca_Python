# Biblioteca HTTP API - Gerenciamento de Livros e Autores

Este projeto é uma API básica que simula o gerenciamento de uma **biblioteca**. Ele permite criar, atualizar, listar e deletar **livros** e **autores**, além de associar livros a autores. A API é construída com o módulo `http.server` do Python e usa requisições HTTP (GET, POST, PUT, DELETE) para manipular os dados.

## Estrutura do Projeto

O projeto contém os seguintes arquivos:

- **main.py**: Contém a lógica principal da API, incluindo o servidor HTTP e o roteamento de requisições.
- **autores.py**: Define a classe `Autor`, que representa os autores da biblioteca.
- **livros.py**: Define a classe `Livro`, que representa os livros da biblioteca.

## Funcionalidades da API

### Requisições GET

- **Listar todos os livros**:
  - **Rota**: `/books`
  - **Resposta**: Retorna uma lista de todos os livros armazenados.
  
- **Obter detalhes de um livro específico**:
  - **Rota**: `/books/{id}`
  - **Resposta**: Retorna os detalhes do livro com o ID especificado.

- **Listar todos os autores**:
  - **Rota**: `/authors`
  - **Resposta**: Retorna uma lista de todos os autores armazenados.

- **Obter detalhes de um autor específico**:
  - **Rota**: `/authors/{id}`
  - **Resposta**: Retorna os detalhes do autor com o ID especificado.

- **Listar livros de um autor específico**:
  - **Rota**: `/authors/{id}/books`
  - **Resposta**: Retorna uma lista de livros associados ao autor.

### Requisições POST

- **Criar um novo livro**:
  - **Rota**: `/books`
  - **Corpo da Requisição**: 
    ```json
    {
      "titulo": "Título do Livro",
      "genero": "Gênero",
      "ano": "Ano"
    }
    ```
  - **Resposta**: Retorna o livro criado.

- **Criar um novo autor**:
  - **Rota**: `/authors`
  - **Corpo da Requisição**: 
    ```json
    {
      "nome": "Nome do Autor",
      "idade": "Idade",
      "nacionalidade": "Nacionalidade"
    }
    ```
  - **Resposta**: Retorna o autor criado.

- **Associar um livro a um autor**:
  - **Rota**: `/authors/{id}/books/{book_id}`
  - **Resposta**: Associa o livro ao autor e retorna uma mensagem de sucesso.

### Requisições PUT

- **Atualizar um livro existente**:
  - **Rota**: `/books/{id}`
  - **Corpo da Requisição**: 
    ```json
    {
      "titulo": "Novo Título",
      "genero": "Novo Gênero",
      "ano": "Novo Ano"
    }
    ```
  - **Resposta**: Retorna o livro atualizado.

- **Atualizar um autor existente**:
  - **Rota**: `/authors/{id}`
  - **Corpo da Requisição**: 
    ```json
    {
      "nome": "Novo Nome",
      "idade": "Nova Idade",
      "nacionalidade": "Nova Nacionalidade"
    }
    ```
  - **Resposta**: Retorna o autor atualizado.

### Requisições DELETE

- **Deletar um livro**:
  - **Rota**: `/books/{id}`
  - **Resposta**: Remove o livro e retorna uma mensagem de sucesso.

- **Deletar a associação de um livro a um autor**:
  - **Rota**: `/authors/{id}/books/{book_id}`
  - **Resposta**: Remove a associação do livro ao autor e retorna uma mensagem de sucesso.

- **Deletar um autor**:
  - **Rota**: `/authors/{id}`
  - **Resposta**: Remove o autor e retorna uma mensagem de sucesso.

## Como Rodar o Projeto

1. **Clone o repositório** ou copie os arquivos fornecidos.
   
2. **Instale o Python 3.x** (se ainda não tiver).
   
3. **Execute o servidor** rodando o comando abaixo no terminal na pasta onde está o arquivo `main.py`:

   ```bash
   python main.py
