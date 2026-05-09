from abc import ABC, abstractmethod

from numpy.lib._datasource import Repository


# Абстракция для работы с пользователями
class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id):
        pass


# Низкоуровневый модуль для MySQL
class MySQLUserRepository(UserRepository):
    def get_user(self, user_id):
        print(f"MySQL: запрос пользователя {user_id}")
        return {"id": user_id, "name": "Alice"}


# Высокоуровневый модуль для PostgreSQL
class PostgresUserRepository(UserRepository):
    def get_user(self, user_id):
        print(f"PostgreSQL: запрос пользователя {user_id}")
        return {"id": user_id, "name": "Bob"}


# Высокоуровневый модуль знает только об интерфейсе
class UserReport:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def generate(self, user_id):
        user = self.repo.get_user(user_id)
        print(f"Отчет для пользователя: {user['name']}")


# Использование
if __name__ == "__main__":
    my_sql_repo = MySQLUserRepository()
    postgres_repo = PostgresUserRepository()

    user_report_my_sql = UserReport(my_sql_repo)
    user_report_my_sql.generate(1)

    user_report_postgres = UserReport(postgres_repo)
    user_report_postgres.generate(1)
