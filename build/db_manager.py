# database loader using sqlite3

import sqlite3
from inspect import signature
from local_data import Tree

class Database:
    def __init__(self, database_file: str):
        self.db_exists = self.check_db_exists()
        self.con = sqlite3.connect(f'{database_file}.db')
        self.cursor = self.con.cursor()

    def check_db_exists(self):
        """
        Check whether TicketRequests table exists in database.
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TicketRequests';")
        return bool(self.cursor.fetchone())

    def db_setup(self, requests_class, tree_instance: Tree):
        """
        Create table in database if it does not already exist.
        Load data into table from local datastructure source.

        Table shape:
        -------------------------------------------------------------
        Club | Buy/Sell | TimeID | UserID | Status | Quantity | Price
        -------------------------------------------------------------
        """
        if not self.db_exists:
            init_sig = signature(requests_class.__init__)
            columns = [param for param in init_sig.parameters if param != 'self']
            column_titles = []
            for column in columns:
                if column == 'ticket_quantity':
                    column_titles.append(f'{column} INTEGER')
                elif column == 'status':
                    column_titles.append(f'{column} BOOLEAN')
                elif column == 'price':
                    column_titles.append(f'{column} REAL')
                else:
                    column_titles.append(f'{column} TEXT')
            create_table_query = f'CREATE TABLE IF NOT EXISTS TicketRequests ({', '.join(column_titles)})'
            self.cursor.execute(create_table_query)
            self.con.commit()
            self.db_exists = True

        for club, data in tree_instance.hash_map.items():
            # insert buy nodes
            for buy_node in data['buy']:
                self.cursor.execute(
                    "INSERT INTO TicketRequests (club, buy_or_sell, timeID, userID, status, ticket_quantity, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (club, 'buy', buy_node.timeID, buy_node.userID, buy_node.status, buy_node.ticket_quantity, buy_node.price)
                )
            # insert sell nodes
            for sell_node in data['sell']:
                self.cursor.execute(
                    "INSERT INTO TicketRequests (club, buy_or_sell, timeID, userID, status, ticket_quantity, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (club, 'sell', sell_node.timeID, sell_node.userID, sell_node.status, sell_node.ticket_quantity, sell_node.price)
                )
        self.con.commit()
        
    def db_close(self):
        self.con.close()
        
    # def db_queries(self):



