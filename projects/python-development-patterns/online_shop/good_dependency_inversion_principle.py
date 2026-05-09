from abc import ABC, abstractmethod


# Абстракция (интерфейс)
class Notifier(ABC):
    @abstractmethod
    def send(self, message):
        pass


# Низкоуровневый модуль (реализует абстракцию)
class EmailSender(Notifier):
    def send(self, message):
        print(f"Sending email: {message}")


# Еще один низкоуровневый модуль
class SMSSender(Notifier):
    def send(self, message):
        print(f"Sending SMS message: {message}")


# Высокоуровневый модуль зависит только от абстракции
class OrderProcessor:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def process_order(self, order_id):
        print(f"Processing order: {order_id}")
        self.notifier.send(f"Order {order_id} is confirmed.")


# Использование
if __name__ == "__main__":
    email_notifier = EmailSender()
    sms_notifier = SMSSender()

    # Можно легко переключаться между способами управления
    processor_email = OrderProcessor(email_notifier)
    processor_email.process_order(order_id=1)

    processor_sms = OrderProcessor(sms_notifier)
    processor_sms.process_order(order_id=2)
