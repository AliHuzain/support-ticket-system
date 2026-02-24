class Ticket:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.status = "Open"

    def close_ticket(self):
        self.status = "Closed"