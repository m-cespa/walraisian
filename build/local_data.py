from typing import List

class ReadNode:
    def __init__(self, request_instance):
        """
        Node class which parses all input data from the requests_class instance
        """
        self.club = request_instance.club
        self.timeID = request_instance.timeID
        self.userID = request_instance.userID
        self.buy_or_sell = request_instance.buy_or_sell
        self.status = request_instance.status
        self.ticket_quantity = request_instance.ticket_quantity
        self.price = request_instance.price

class WriteNode:
    def __init__(self, request_instance):
        """
        Node class which stores all but club & buy/sell parameters to reduce storage
        """
        self.timeID = request_instance.timeID
        self.userID = request_instance.userID
        self.status = request_instance.status
        self.ticket_quantity = request_instance.ticket_quantity
        self.price = request_instance.price

class Tree:
    def __init__(self):
        self.hash_map = {}

    def binary_insertion(self, lst: List[WriteNode], node: WriteNode, len: int) -> None:
        low, high = 0, len

        while low < high:
            mid = (low + high) // 2
            if lst[mid].price < node.price:
                low = mid + 1
            else:
                high = mid

        lst.insert(low, node)

    def add_node(self, request_instance) -> None:
        """
        Take a requests_class instance and load data into Tree object.
        Binary insertion to maintain entries in sorted price order. 
        """
        read_node = ReadNode(request_instance)
        write_node = WriteNode(request_instance)

        if read_node.club not in self.hash_map:
            # track the sizes of the buy/sell arrays to optimise the binary insertion
            self.hash_map[read_node.club] = {'buy': [], 'sell': [], 'buy_size': 0, 'sell_size': 0}

        if read_node.buy_or_sell == 'buy':
            n = self.hash_map[read_node.club]['buy_size']
            self.binary_insertion(lst=self.hash_map[read_node.club]['buy'], node=write_node, len=n)
            self.hash_map[read_node.club]['buy_size'] += 1
        else:
            n = self.hash_map[read_node.club]['sell_size']
            self.binary_insertion(lst=self.hash_map[read_node.club]['sell'], node=write_node, len=n)
            self.hash_map[read_node.club]['sell_size'] += 1

    def find_matches(self) -> List:
        """
        Condition for a match eg:
        (for a given club)

        buy = [7, 8, 10, 11]
        sell = [6.5, 7, 8, 15]

        For each element of sell, traverse the buy list until buy[j] >= sell[i]
        Store index j such that subsequent searches commence there
        Append matches to a list of tuples (sell_node, buy_node)
        For each buy/sell node, subtract 1 from quantity;
            if quantity == 0:
                add index to removed set
            if quantity of sell node != 0:
                keep pointer at i
        """
        matches = []
        
        for club in self.hash_map:
            n = self.hash_map[club]['sell_size']
            m = self.hash_map[club]['buy_size']

            sellers_remove = set()
            buyers_remove = set()

            i = 0
            j = 0

            # check that buy and sell lists are populated
            if n and m:
                while i < n:
                    if i in sellers_remove:
                        i += 1
                        continue
                    current_seller = self.hash_map[club]['sell'][i]

                    while j < m:
                        if j in buyers_remove:
                            j += 1
                            continue
                        current_buyer = self.hash_map[club]['buy'][j]

                        if current_buyer.price >= current_seller.price:
                            trade_quantity = min(current_seller.ticket_quantity, current_buyer.ticket_quantity)
                            # subtract from each of buyer and seller nodes the min trade quantity
                            current_buyer.ticket_quantity -= trade_quantity
                            current_seller.ticket_quantity -= trade_quantity

                            matches.append((current_seller, current_buyer))

                            if current_buyer.ticket_quantity == 0:
                                buyers_remove.add(j)
                                j += 1  # advance buyer pointer if exhausted
                            if current_seller.ticket_quantity == 0:
                                sellers_remove.add(i)
                                i += 1  # advance seller pointer if exhausted
                                break
                        else:
                            j += 1

                    # check seller is exhausted before moving to next
                    if current_seller.ticket_quantity == 0:
                        sellers_remove.add(i)
                        i += 1

            for seller_to_remove in sellers_remove:
                self.hash_map[club]['sell_size'] -= 1
                self.hash_map[club]['sell'].pop(seller_to_remove)

            for buyer_to_remove in buyers_remove:
                self.hash_map[club]['buy_size'] -= 1
                self.hash_map[club]['buy'].pop(buyer_to_remove)

        return matches
                            

                        


            


