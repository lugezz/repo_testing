class Padre:
    nombre = "Juan"
    apellido = "Perez"

    def print_nombre(self):
        print(self.apellido, self.nombre)

class Hijo(Padre):
    nombre = "Ricardo"

hijito = Hijo()
hijito.print_nombre()
