from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from livros import Livro
from autores import Autor


# Instâncias globais para armazenar autores e livros
autores = {}
livros = {}

# Classe para tratar as requisições HTTP
class BibliotecaHandler(BaseHTTPRequestHandler):

    # Método auxiliar para simplificar o envio de respostas HTTP
    def _responder(self, status, data=None):
        self.send_response(status)
        self.send_header("Content-type", "application/json") # Tipo de conteúdo da resposta
        self.end_headers() # Finaliza o cabeçalho da resposta
        if data:
            self.wfile.write(json.dumps(data).encode()) # Converte o dicionário em JSON e envia como resposta    
    
    
    # Função para lidar com a requisição GET
    def do_GET(self):
    
        # Listar todos os livros
        if self.path == '/books':
            self._responder(200, [livro.__dict__ for livro in livros.values()]) # Converte os livros em dicionários e envia como resposta
    
        # Obter detalhes de um livro específico
        elif self.path.startswith('/books/'):
            livro_id = int(self.path.split('/')[2]) # Obtém o ID do livro a partir do path da requisição
            livro = livros.get(livro_id) # Obtém o livro com o ID especificado
            if livro:
                self._responder(200, livro.__dict__) # Converte o livro em dicionário e envia como resposta
            else:
                self._responder(404, {'message': 'Livro não encontrado!'})
    
        # Listar todos os autores
        elif self.path == '/authors':
            self._responder(200, [autor.__dict__ for autor in autores.values()]) # Converte os autores em dicionários e envia como resposta
    
        # Listar os livros de um autor
        elif self.path.startswith('/authors/') and 'books' in self.path:
            path_parts = self.path.split('/') # Separa o path em partes
            autor_id = int(path_parts[2])
            autor = autores.get(autor_id)
            if autor:
                if autor.livros_publicados != "": # Verifica se o autor tem livros publicados
                    self._responder(200, autor.livros_publicados) # Envia a lista de livros publicados como resposta
                else:
                    self._responder(404, {'message': 'Esse autor não possui nenhum livro associado!'})
            else:
                self._responder(404, {'message': 'Autor não encontrado!'})
    
        # Obter detalhes de um autor específico
        elif self.path.startswith('/authors/'):
            autor_id = int(self.path.split('/')[2]) # Obtém o ID do autor a partir do path da requisição
            autor = autores.get(autor_id) # Obtém o autor com o ID especificado
            if autor:
                self._responder(200, autor.__dict__) # Converte o autor em dicionário e envia como resposta
            else:
                self._responder(404, {'message': 'Autor não encontrado!'})
    
    
    
    # Função para lidar com a requisição POST
    def do_POST(self):
        global livros
        global autores
    
        # Criar um livro
        if self.path == '/books':
            conteudo = self.rfile.read(int(self.headers['Content-Length'])).decode() # Lê o corpo da requisição
            dados = json.loads(conteudo) # Converte o corpo da requisição em um dicionário
            livro = Livro(**dados) # Cria um objeto Livro com os dados do corpo da requisição
            livros[livro.id] = livro # Adiciona o livro ao dicionário de livros
            self._responder(201, livro.__dict__) # Envia uma resposta de criação com o livro criado
    
        # Criar um autor    
        elif self.path == '/authors':
            conteudo = self.rfile.read(int(self.headers['Content-Length'])).decode() # Lê o corpo da requisição
            dados = json.loads(conteudo) # Converte o corpo da requisição em um dicionário
            autor = Autor(**dados) # Cria um objeto Autor com os dados do corpo da requisição
            autores[autor.id] = autor # Adiciona o autor ao dicionário de autores
            self._responder(201, autor.__dict__) # Envia uma resposta de criação com o autor criado
    
        # Associar um livro a um autor
        elif self.path.startswith('/authors/') and 'books' in self.path:
            path_parts = self.path.split('/') # Separa o path da requisição em partes
            autor_id = int(path_parts[2])
            livro_id = int(path_parts[4])
            autor = autores.get(autor_id)
            livro = livros.get(livro_id)
    
            if autor.livros_publicados != "": # Verifica se o autor já possui livros associados
                autor.livros_publicados += ";" # Adiciona um ponto e vírgula para separar os livros já exisitentes
            autor.livros_publicados += livro.titulo # Adiciona o título do livro ao autor
            
            if not autor:
                self._responder(404, {'message': 'Autor não encontrado'}) # Envia uma resposta de erro se o autor não for encontrado
            if not livro:
                self._responder(404, {'message': 'Livro não encontrado'}) # Envia uma resposta de erro se o livro não for encontrado
    
            livro.autor_id = autor_id
            self._responder(200, {'message': f'Livro {livro.titulo} associado ao autor {autor.nome} com sucesso'}) # Envia uma resposta de sucesso se a associação for bem sucedida
    
        else:
            self.send_error(405, 'Method Not Allowed') # Responder com um erro 405 caso o caminho não seja /books ou /authors
    
    
    # Função para lidar com a requisição PUT
    def do_PUT(self):
        global livros
        global autores
    
        # Atualizar um livro
        if self.path.startswith('/books/'):
            livro_id = int(self.path.split('/')[2]) # Obtém o ID do livro a partir do path da requisição
            conteudo = self.rfile.read(int(self.headers['Content-Length'])).decode() # Lê o corpo da requisição
            dados = json.loads(conteudo) # Converte o corpo da requisição em um dicionário
            livro = livros.get(livro_id) # Obtém o livro com o ID especificado
            if livro:
                livro.titulo = dados.get('titulo', livro.titulo) # Atualiza o título do livro com o valor do corpo da requisiçao ou o valor padrão
                livro.genero = dados.get('genero', livro.genero) # Atualiza o gênero do livro com o valor do corpo da requisiçao ou o valor padrão
                livro.ano = dados.get('ano', livro.ano) # Atualiza o ano do livro com o valor do corpo da requisiçao ou o valor padrão
                self._responder(200, livro.__dict__) # Envia uma resposta de atualização com o livro atualizado
    
            else:
                self._responder(404, {'message': 'Livro não encontrado'})
    
        # Atualizar um autor
        elif self.path.startswith('/authors/'):
            autor_id = int(self.path.split('/')[2]) # Obtém o ID do autor a partir do path da requisição
            conteudo = self.rfile.read(int(self.headers['Content-Length'])).decode() # Lê o corpo da requisição
            dados = json.loads(conteudo) # Converte o corpo da requisição em um dicionário
            autor = autores.get(autor_id) # Obtém o autor com o ID especificado
            if autor:
                autor.nome = dados.get('nome', autor.nome) # Atualiza o nome do autor com o valor do corpo da requisiçao ou o valor padrão
                autor.idade = dados.get('idade', autor.idade) # Atualiza a idade do autor com o valor do corpo da requisiçao ou o valor padrão
                autor.nacionalidade = dados.get('nacionalidade', autor.nacionalidade) # Atualiza a nacionalidade do autor com o valor do corpo da requisiçao ou o valor padrão
                self._responder(200, autor.__dict__) # Envia uma resposta de atualização com o autor atualizado
    
            else:
                self._responder(404, {'message': 'Autor não encontrado'})
    
    
    # Função para lidar com a requisição DELETE
    def do_DELETE(self):
        global livros
        global autores
    
        # Deletar um livro
        if self.path.startswith('/books/'):
            livro_id = int(self.path.split('/')[2]) # obtém o ID do livro a ser deletado
            livro = livros.pop(livro_id, None) # remove o livro do dicionário de livros e recebe o objeto Livro
            self._responder(200, {'message':f'{livro.titulo} removido com sucesso!'}) 

        # Deletar uma assoiação entre um livro e um autor
        elif self.path.startswith('/authors/') and 'books' in self.path:
            path_parts = self.path.split('/') # obtém os partes do path da requisição
            autor_id = int(path_parts[2])
            livro_id = int(path_parts[4])
            autor = autores.get(autor_id) # obtém o autor com o ID especificado
            livro = livros.get(livro_id) # obtém o livro com o ID especificado
    
            if not autor:
                self._responder(404, {'message':'Autor não encontrado!'})
                return
            if not livro:
                self._responder(404, {'message':'Livro não encontrado!'})
    
            if livro.titulo in autor.livros_publicados: # verifica se o livro está associado ao autor
                livros_associados = autor.livros_publicados.split(';') # divide os livros associados pelo ponto e vírgula
                livros_associados.remove(livro.titulo) # remove o livro da lista de livros associados
                autor.livros_publicados = ';'.join(livros_associados) if livros_associados else "" # atualiza a lista de livros associados
    
                livro.autor_id = None # remove a associação entre o livro e o autor
                self._responder(200, {'message': f'A associação do livro {livro.titulo} com o autor {autor.nome} foi removida com sucesso!'})
            else:
                self._responder(404, {'message': 'Esse livro não está associado ao autor especificado!'})  
    
        # Deletar um autor
        elif self.path.startswith('/authors/'):
            autor_id = int(self.path.split('/')[2]) # obtém o ID do autor a ser deletado
            autor = autores.pop(autor_id, None) # remove o autor do dicionário de autores e recebe o objeto Autor
            self._responder(200, {'message':f'{autor.nome} removido com sucesso!'})
    
        else:
            self._responder(404, {'message':'Objeto não encontrado!'})  


# Função para rodar o servidor
def run(server_class=HTTPServer, handler_class=BibliotecaHandler, port=8080):
    server_address = ('', port) # Define o endereço do servidor
    httpd = server_class(server_address, handler_class) # Cria o servidor HTTP
    print(f'Servidor rodando na porta {port}...')
    httpd.serve_forever() # Inicia o servidor

# Verifica se o arquivo está sendo executado diretamente
if __name__ == '__main__':
    run()









