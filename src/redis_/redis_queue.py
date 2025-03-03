"""
Реализовать класс очереди, который использует redis "под капотом"
"""

import json
from typing import Optional

import redis


class RedisQueue:
    """
    Класс очереди, который использует redis
    """

    def __init__(self, host="localhost", port=6379, db=0, queue_name="redis_queue"):
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.queue_name = queue_name

    def publish(self, msg: dict) -> None:
        """
        Отправляет сообщение в очередь

        :param msg: Сообщение в виде словаря
        """

        self.redis.rpush(self.queue_name, json.dumps(msg))

    def consume(self) -> Optional[dict]:
        """
        Получает и возвращает первое сообщение из очереди
        """

        msg = self.redis.lpop(self.queue_name)

        if msg:
            return json.loads(msg)
        return None


if __name__ == "__main__":
    q = RedisQueue()
    q.publish({"a": 1})
    q.publish({"b": 2})
    q.publish({"c": 3})

    assert q.consume() == {"a": 1}
    assert q.consume() == {"b": 2}
    assert q.consume() == {"c": 3}
