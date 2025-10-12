# Initialize a rate limiter using SlowAPI.

# `Limiter` manages request rate limits to prevent abuse or overuse of API endpoints.
from slowapi import Limiter

# `key_func=get_remote_address` means each client's rate limit is tracked based on their IP address.
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)