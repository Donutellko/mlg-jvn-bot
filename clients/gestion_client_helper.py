
class Activity:
    def __init__(self, descripcion: str,
                 fecha: str,
                 fechas_inscripcion: str,
                 plazas_libres: int,
                 pago, # bool or None
                 edades: str,
                 programa: str = "Alterna en tu Ocio",
                 ):
        self.descripcion = descripcion
        self.programa = programa
        self.fecha = fecha
        self.fechas_inscripcion = fechas_inscripcion
        self.plazas_libres = plazas_libres
        self.pago = pago
        self.edades = edades

    def __str__(self):
        str_plazas = f"Hay {self.plazas_libres} plazas. " if self.plazas_libres > 0 else "No hay plazas. "
        str_pago = "Hay que pagar. " if self.pago else ""
        return f"{self.fecha}: {self.descripcion}\n{str_plazas}{str_pago}"

    def str_oncoming(self):
        str_inscripcion = f"Inicio Inscripción: {self.fechas_inscripcion}"
        return f"{self.fecha}: {self.descripcion}\n{str_inscripcion}\n"

