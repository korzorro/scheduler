from copy import deepcopy
from datetime import MAXYEAR
from models import DatetimeRange


def is_solved(tasks):
    for task in tasks:
        if not task.meets_constraints():
            return False
    return True


def update_dt_ranges(datetime_ranges, event):
    updated = []
    for dt_range in datetime_ranges:
        if dt_range.overlaps(event.datetime_range):
            # begin [ ...
            if dt_range.starts_before(event.datetime_range):
                # begin [ end ) ...
                if event.end < dt_range[1]:
                    updated.append((event.end, dt_range[1]))
                # begin [ ) end
            # [ begin ...
            else:
                updated.append((dt_range[0], event.begin))
                # [ begin end )
                if event.end < dt_range[1]:
                    updated.append((event.end, dt_range[1]))
        else:
            updated.append(dt_range)
        datetime_ranges = updated


def solve(tasks, events, start):
    datetime_ranges = [datetimeRange(start, MAXYEAR)]
    for event in events:
        update_dt_ranges(datetime_ranges, event)

    stack = [deepcopy((tasks, available_dt_ranges))]
    priority_task = min(tasks, key=lambda t: t.priority)
    priority_task.available_dt_ranges = available_dt_ranges

    while len(tasks) > 0:
        event = priority_task.next_candidate()
        if event:
            priority_task.insert(event)
            update_dt_ranges(available_dt_ranges, event)
            if priority_task.meets_constraints():
                tasks.remove(priority_task)
                priority_task = min(tasks, key=lambda t: t.priority)
                priority_task.available_dt_ranges = available_dt_ranges
            stack.append(deepcopy((tasks, available_dt_ranges)))
        else:
            tasks, available_dt_ranges = stack.pop()

    for task in tasks:
        events += task.events

    return events
