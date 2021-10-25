import threading
from threading import RLock
from typing import Type
import uuid
from dataclasses import dataclass


class PooledObject:
    def __init__(
        self
    ) -> None:
        self._id = uuid.uuid4()

    def dispose(self) -> bool:
        return True


class PooledObjectFactory:
    def __init__(self) -> None:
        pass

    def create(self) -> PooledObject:
        print(f"Creating object from {self.__class__.__name__}")
        return None


# TODO: Implement max_object_count
class ObjectPool:
    def __init__(
        self,
        object_factory,
        max_object_count: int,
    ) -> None:
        self._lock = threading.RLock()
        self._object_factory = object_factory
        self._max_object_count = max_object_count
        self._available = list()
        self._reserved = list()

    def get_object(self) -> PooledObject:
        self._lock.acquire()

        if(len(self._available) > 0):
            ob = self._available.pop()
            self._reserved.append(ob)
            print(f"Reserved {ob.__class__.__name__} [{ob._id}]")
            return ob
        else:
            ob = self._object_factory.create()
            self._reserved.append(ob)
            return ob

        self._lock.release()

    def release_object(self, pooled_object: PooledObject):
        if pooled_object in self._reserved:
            self._reserved.remove(pooled_object)
            self._available.append(pooled_object)
            print(f"Released {pooled_object.__class__.__name__} [{pooled_object._id}]")


class FtPConnection(PooledObject):
    def __init__(
        self,
        url: str,
        username: str,
        password: str,
    ) -> None:
        super().__init__()
        self.url=url
        self.username=username
        self.password=password


class FtpConnectionFactory(PooledObjectFactory):
    def __init__(
        self,
        url: str,
        username: str,
        password: str,
    ) -> None:
        self.url=url
        self.username=username
        self.password=password


    def create(self) -> PooledObject:
        super().create()
        return FtPConnection(
            self.url,
            self.username,
            self.password,
        )

def main():
    # TODO: Load connection details from file
    url="at.at.com",
    username="user",
    password="123",

    # Create connection factory
    factory = FtpConnectionFactory(
        url=url,
        username=username,
        password=password,
    )

    # Create object pool
    pool = ObjectPool(
        factory=factory,
        max_object_count=5
    )

    # Get connection from pool
    ob = pool.get_object()

    # Do something with pooled object
    # ob.somefunction()

    # Release pooled object back to pool
    pool.release_object(ob)


if __name__ == "__main__":
    main()
