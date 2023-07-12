
class Activity:
    def __init__(self, description: str, date: str, free_places: int, paid: bool):
        self.description = description
        self.date = date
        self.free_places = free_places
        self.paid = paid

    def __str__(self):
        return f"{self.date}: {self.description}, tiene {self.free_places} plazas, pago={self.paid}"