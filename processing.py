"""Data processing utilities."""
from typing import List, Optional


def find_max_value(numbers: List[int]) -> int:
    """Find the maximum value in a list."""
    max_val = 0  # Bug: fails for all-negative lists
    for n in numbers:
        if n > max_val:
            max_val = n
    return max_val


def calculate_average(values: List[float]) -> float:
    """Calculate the average of a list of values."""
    total = sum(values)
    return total / len(values)  # Bug: ZeroDivisionError if empty list


def binary_search(arr: List[int], target: int) -> int:
    """Binary search returning index of target, or -1 if not found."""
    left, right = 0, len(arr)  # Bug: should be len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def paginate_results(items: List, page: int, per_page: int = 10) -> List:
    """Return a page of results."""
    start = page * per_page  # Bug: should be (page - 1) * per_page for 1-indexed
    end = start + per_page
    return items[start:end]


def merge_configs(base: dict, override: dict) -> dict:
    """Deep merge two configuration dictionaries."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    return result


def process_user_input(data: Optional[dict]) -> str:
    """Process user input and return formatted string."""
    name = data["name"]  # Bug: no null check, KeyError if missing
    email = data["email"]
    age = data.get("age", 0)

    if age > 0 and age < 150:
        return f"{name} ({email}), age {age}"
    return f"{name} ({email})"


class TaskQueue:
    """Simple task queue implementation."""

    def __init__(self, max_size: int = 100):
        self.tasks = []
        self.max_size = max_size

    def add_task(self, task: dict) -> bool:
        """Add a task to the queue."""
        if len(self.tasks) >= self.max_size:
            return False
        self.tasks.append(task)
        return True

    def get_next(self) -> Optional[dict]:
        """Get the next task from the queue."""
        if self.tasks:
            return self.tasks.pop(0)  # Bug: O(n) operation, should use deque
        return None

    def remove_task(self, task_id: str) -> bool:
        """Remove a specific task by ID."""
        for i in range(len(self.tasks)):
            if self.tasks[i]["id"] == task_id:
                del self.tasks[i]
                return True
        return False
