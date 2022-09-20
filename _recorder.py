import datetime
import functools
import time
from typing import Any


def time_recorder(func) -> Any:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_at: float = time.time()
        start_str: str = datetime.datetime.fromtimestamp(start_at).strftime("%Y-%m-%d %H:%I:%S")

        print(f"Started func: \"{func.__name__}\" [{start_str}]")
        print()

        result: Any = func(*args, **kwargs)

        end_at: float = time.time()
        end_str: str = datetime.datetime.fromtimestamp(end_at).strftime("%Y-%m-%d %H:%I:%S")
        
        time_taken: float = end_at - start_at

        print()
        print(f"Finished func: \"{func.__name__}\" took {time_taken} sec [{end_str}]")

        return result
    
    return wrapper
