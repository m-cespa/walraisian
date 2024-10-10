# N tree for storing buy, sell requests
import heapq

class LeafNode:
    def __init__(self, name, buy=[], sell=[]):
        self.name = name
        self.buy = buy if buy is not None else []
        self.sell = sell if sell is not None else []
        # convert both to min heaps
        heapq.heapify(self.buy)
        heapq.heapify(self.sell)

    def push_to_buy(self, price: float) -> None:
        heapq.heappush(self.buy, price)

    def push_to_sell(self, price: float) -> None:
        heapq.heappush(self.sell, price)

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = set()
        self.children_names = set()

    def add_child(self, obj: LeafNode) -> None:
        self.children.add(obj)
        self.children_names.add(obj.name)

    def incoming_request(self, target_club: str, price: float, selling: bool):
        if target_club not in self.children_names:
            self.add_child(LeafNode(name=target_club))

        for club in self.children:
            if club.name == target_club:
                # if the incoming request is a sale
                if selling:
                    club.push_to_sell(price)
                # if the incoming request is a buy 
                else:
                    club.push_to_buy(price)
                break

    

        



root = TreeNode(name='root')
revs = LeafNode(name='revs')
mash = LeafNode(name='mash')

root.add_child(revs)
root.add_child(mash)

revs.push_to_buy(10)
mash.push_to_sell(10)
