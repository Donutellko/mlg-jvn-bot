
class Activity:
    def __init__(self, description: str, date: str, free_places: int, paid: bool):
        self.description = description
        self.date = date
        self.free_places = free_places
        self.paid = paid

    def __str__(self):
        plazas = f"Hay {self.free_places} plazas. " if self.free_places > 0 else "No hay plazas. "
        pago = "Hay que pagar. " if self.paid else ""
        return f"{self.date}: {self.description}\n{plazas}{pago}"