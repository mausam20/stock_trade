import random
import threading
import time

class OrderNode:
    """ A node representing an order in the linked list """
    def __init__(self, order_type, ticker, quantity, price):
        # buy or sell
        self.order_type = order_type  
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.next = None

class OrderBook:
    """ OrderBook using linked lists without dictionaries/maps """
    def __init__(self):
        self.buy_head = None  
        self.sell_head = None  
        self.buy_tail = None
        self.sell_tail = None

    def add_order(self, order_type, ticker, quantity, price):
        """ Adds an order into the linked list """
        new_order = OrderNode(order_type, ticker, quantity, price)

        if order_type == "Buy":
            self._insert_buy_order(new_order)
        else:
            self._insert_sell_order(new_order)

    def _insert_buy_order(self, order):
        """ Inserts buy order in descending order of price """
        if not self.buy_head or order.price > self.buy_head.price:
            order.next = self.buy_head
            self.buy_head = order
            return
        
        prev, curr = None, self.buy_head
        while curr and curr.price >= order.price:
            prev, curr = curr, curr.next
        prev.next = order
        order.next = curr

    def _insert_sell_order(self, order):
        """ Inserts sell order in ascending order of price """
        if not self.sell_head or order.price < self.sell_head.price:
            order.next = self.sell_head
            self.sell_head = order
            return

        prev, curr = None, self.sell_head
        while curr and curr.price <= order.price:
            prev, curr = curr, curr.next
        prev.next = order
        order.next = curr

    def match_orders(self):
        """ Matches buy and sell orders """
        while self.buy_head and self.sell_head and self.buy_head.price >= self.sell_head.price:
            buy_order = self.buy_head
            sell_order = self.sell_head

            traded_quantity = min(buy_order.quantity, sell_order.quantity)
            print(f"Trade Executed: {buy_order.ticker} | Price: {sell_order.price} | Quantity: {traded_quantity}")

            buy_order.quantity -= traded_quantity
            sell_order.quantity -= traded_quantity

            if buy_order.quantity == 0:
                self.buy_head = self.buy_head.next
            if sell_order.quantity == 0:
                self.sell_head = self.sell_head.next


class StockExchange:
    """ Real-time Stock Exchange to handle multiple tickers """
    def __init__(self, num_tickers=1024):
        self.order_books = [OrderBook() for _ in range(num_tickers)]
        self.lock = threading.Lock()  # Ensures thread safety
    
    def add_order(self, order_type, ticker, quantity, price):
        """ Adds an order to the corresponding order book """
        index = ticker % len(self.order_books)
        self.lock.acquire()
        try:
            self.order_books[index].add_order(order_type, ticker, quantity, price)
        finally:
            self.lock.release()

    def match_orders(self):
        """ Matches orders for all tickers """
        for book in self.order_books:
            self.lock.acquire()
            try:
                book.match_orders()
            finally:
                self.lock.release()

# Simulating real-time transactions
def simulate_orders(stock_exchange):
    """ Randomly executes addOrder with different parameters """
    tickers = 1024
    while True:
        order_type = random.choice(["Buy", "Sell"])
        ticker = random.randint(0, tickers - 1)
        quantity = random.randint(1, 100)
        price = round(random.uniform(10, 500), 2)

        stock_exchange.add_order(order_type, ticker, quantity, price)
        time.sleep(random.uniform(0.01, 0.1))  # Simulate random order timings

# Start real-time stock exchange simulation
stock_exchange = StockExchange()
order_thread = threading.Thread(target=simulate_orders, args=(stock_exchange,))
match_thread = threading.Thread(target=stock_exchange.match_orders)

order_thread.start()
match_thread.start()
