from typing import List, Tuple

from celery.result import AsyncResult


def check_all_tasks_complete(task_list: List[str]) -> Tuple[bool, bool]:
    """
    Checks a list of task IDs to see if they are marked as successful
    :param task_list: A list of string task IDs to check
    :return: (complete, fatal) as a tuple. Complete is true/false of all tasks being complete, and if any task is
    marked as failed, then the fatal is true
    """
    for task in task_list:
        status = AsyncResult(task).state
        if status == "FAILURE":
            return False, True
        elif status == "SUCCESS":
            continue
        return False, False
    # If all tasks are successful
    return True, False
