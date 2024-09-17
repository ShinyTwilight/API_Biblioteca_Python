class Livro:
    id_livro = 1

    def __init__(self, titulo, genero, ano):
      self.titulo = titulo
      self.genero = genero
      self.ano = ano
      self.id = Livro.id_livro
      self.autor_id = None

      Livro.id_livro += 1