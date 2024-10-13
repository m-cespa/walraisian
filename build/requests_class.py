import datetime
class TicketRequest:
    def __init__(self, timeID, userID, club, buy_or_sell, status, ticket_quantity):
        """
        Initialize a transaction object representing a user's ticket transaction.

        Args:
            timeID (datetime): The timestamp of the transaction. 
            userID (str): The unique identifier for the user performing the transaction.
            club (str): The name of the club associated with the ticket transaction.
            buy_or_sell (str): Indicates whether the transaction is a 'buy' or 'sell'.
            status (bool): The current status of the transaction (True for completed, False for pending/cancelled).
            ticket_quantity (int): The number of tickets involved in the transaction.
        """
        self.timeID = timeID
        self.userID = userID
        self.club = club
        self.buy_or_sell = buy_or_sell
        self.status = status
        self.ticket_quantity = ticket_quantity


