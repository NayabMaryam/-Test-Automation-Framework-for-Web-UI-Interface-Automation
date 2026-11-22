
import redis
import json


class RedisReader:

    def __init__(self, host, port, db):

        self.host = host
        self.port = port
        self.db = db

        self.client = None

        self.key_prefix = "test_data:"

    def get_connection(self):

        if self.client is None:

            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True
            )

        return self.client

    def close_connection(self):

        if self.client is not None:

            self.client.close()

            self.client = None

    def store_test_data(self, key, test_data):

        client = self.get_connection()

        redis_key = f"{self.key_prefix}{key}"

        serialized_data = json.dumps(test_data)

        return client.set(redis_key, serialized_data)

    def get_test_data(self, key):

        client = self.get_connection()

        redis_key = f"{self.key_prefix}{key}"

        data = client.get(redis_key)

        if data is None:
            return None

        return json.loads(data)

    def get_all_test_data(self):

        client = self.get_connection()

        all_data = {}

        for redis_key in client.scan_iter(
            match=f"{self.key_prefix}*"
        ):

            key = redis_key[len(self.key_prefix):]

            all_data[key] = self.get_test_data(key)

        return all_data

    def delete_test_data(self, key):

        client = self.get_connection()

        redis_key = f"{self.key_prefix}{key}"

        return client.delete(redis_key)
