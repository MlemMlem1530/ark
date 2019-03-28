import os

from redis import Redis

from chain.crypto.objects.block import Block


class Queue(object):

    list_name = 'process_queue'
    restored_database_integrity = False
    forging_delegates = []

    def __init__(self):
        super().__init__()

        self.db = Redis(
            host=os.environ.get('REDIS_HOST', 'localhost'),
            port=os.environ.get('REDIS_PORT', 6379),
            db=os.environ.get('REDIS_DB', 0),
        )

    def push_block(self, block):
        serialized_block = block.serialize_full()
        self.db.rpush(self.list_name, serialized_block)

    def pop_block(self):
        return self.db.lpop(self.list_name)

    def fetch_last_block(self):
        serialized_block = self.db.lindex(-1)
        if serialized_block:
            return Block.from_serialized(serialized_block)
        return None



    def clear(self):
        print('Clearing process queue')
        self.db.delete(self.list_name)
