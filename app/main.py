from tickets import Ticket

ticket1 = Ticket("Login Issue", "User cannot login")
print(ticket1.title, ticket1.status)

ticket1.close_ticket()
print(ticket1.status)