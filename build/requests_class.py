class TicketRequest:
    def __init__(self, club, timeID, userID, buy_or_sell,requestID, ticket_quantity= 1,price="market",status=True):
        """
        Initialize a transaction object representing a user's ticket transaction.

        Args:
            timeID (datetime): The timestamp of the transaction. 
            userID (str): The unique identifier for the user performing the transaction.
            club (str): The name of the club associated with the ticket transaction.
            buy_or_sell (str): Indicates whether the transaction is a 'buy' or 'sell'.
            ticket_quantity (int): The number of tickets involved in the transaction.
            price (str or float) : The asking/selling price of the ticket, if none, will get the market price from the resolve_price method
        """
        self.club = club
        self.buy_or_sell = buy_or_sell
        self.timeID = timeID
        self.userID = userID
        self.ticket_quantity = ticket_quantity
        self.price = self.resolve_price(price)
        self.requestID = requestID # unique identifier for each request object, concatenated string of 
    
    def __repr__(self):
        return (self.club,self.buy_or_sell,self.timeID,self.userID,self.ticket_quantity,self.price,self.requestID)
    
    def resolve_price(self,price):
        if price == "market":
            if self.buy_or_sell == "buy":
                return "Placeholder Value"
                NotImplementedError # implement logic for calculating the market price
            elif self.buy_or_sell == "sell":
                return "Placeholder Value"
                NotImplementedError # implement logic for calculating the market price
        return price
    
    def __eq__(self,other):
        # Check if the other object is of the same class and compare attributes
        if isinstance(other,TicketRequest):
            return (self.club == other.club and 
                    self.buy_or_sell == other.buy_or_sell and
                    self.timeID == other.timeID and
                    self.ticket_quantity == other.ticket_quantity and
                    self.price == other.price)
        return False
    
    

