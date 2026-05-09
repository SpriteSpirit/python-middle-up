# Плохо: прямая зависимость от MySQL
# Низкоуровневый модуль
class MySQLDatabase:
    def get_user(self, user_id):
        print(f"SELECT * FROM users WHERE id = {user_id}")  # Имитация SQL
        return {"id": user_id, "name": "Alice"}


# Высокоуровневый модуль
class UserReport:
    def __init__(self):
        self.db = MySQLDatabase()  # Жесткая привязка к MySQL

    def generate(self, user_id):
        user = self.db.get_user(user_id)
        print(f"Отчет для пользователя: {user['name']}")


# Использование
if __name__ == "__main__":
    user_report = UserReport()
    user_report.generate(1)
