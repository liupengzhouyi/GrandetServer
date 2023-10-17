import hashlib
import bisect


class ConsistentHash:
    def __init__(self, nodes=None, replicas=100):
        self.replicas = replicas
        self.ring = dict()
        self.sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        for i in range(self.replicas):
            key = self.hash(f"{node}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node):
        for i in range(self.replicas):
            key = self.hash(f"{node}:{i}")
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key):
        hash_key = self.hash(key)
        index = bisect.bisect(self.sorted_keys, hash_key)
        return self.ring[self.sorted_keys[index % len(self.sorted_keys)]]

    @staticmethod
    def hash(key):
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        return int(m.hexdigest(), 16)
