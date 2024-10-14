# N tree for storing buy, sell requests
import heapq
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

    def add_node(self, request_instance):
        # create write and read node instances for sorting purposes
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

