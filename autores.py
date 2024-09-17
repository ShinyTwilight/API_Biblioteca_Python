
class Autor:
    id_autor = 1
    def __init__(self, nome, idade, nacionalidade):
      self.nome = nome
      self.idade = idade
      self.nacionalidade = nacionalidade
      self.id = Autor.id_autor
      self.livros_publicados = ""

      Autor.id_autor += 1