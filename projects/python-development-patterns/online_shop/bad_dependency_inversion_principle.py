class EmailSender:
    def send(self, message):
        print(f"Sending Email: {message}")


class OrderProcessor:
    def __init__(self):
        # жесткая зависимость: класс сам создает экземпляр EmailSender
        self.notifier = EmailSender()

    def process_order(self, order_id):
        print(f"Processing Order: {order_id}")
        self.notifier.send(f"Order {order_id} is confirmed")


if __name__ == "__main__":
    processor = OrderProcessor()
    processor.process_order(order_id=1)
