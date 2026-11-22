
import redis


class RedisReader:

    def __init__(self, host, port, db):

        self.host = host
        self.port = port
        self.db = db

        self.client = None

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
