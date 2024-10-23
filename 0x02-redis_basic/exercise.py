#!/usr/bin/env python3
"""
Main file
"""


import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f"{method.__qualname__}"  # Use method's qualified name as the key
        self._redis.incr(key)  # Increment the call count in Redis
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"  # Input list key
        output_key = f"{method.__qualname__}:outputs"  # Output list key

        # Store the input arguments as strings
        self._redis.rpush(input_key, str(args))

        # Execute the original method and store the output
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper

class Cache:
    """Cache class to interact with Redis."""

    def __init__(self):
        """Initialize the Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return a generated key."""
        key = str(uuid.uuid4())  # Generate a random UUID
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """Retrieve data from Redis and optionally convert it."""
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string value from Redis."""
        return self.get(key, lambda d: d.decode("utf-8") if d else None)

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer value from Redis."""
        return self.get(key, lambda d: int(d) if d else None)

def replay(method: Callable):
    """Display the history of calls of a particular function."""
    redis_instance = redis.Redis()
    method_name = method.__qualname__

    # Retrieve inputs and outputs from Redis
    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for input_, output in zip(inputs, outputs):
        print(f"{method_name}(*{input_.decode('utf-8')}) -> {output.decode('utf-8')}")
