from datetime import timedelta, MINYEAR, MAXYEAR


class Constrained:

    def __init__(self, constraints=[]):
        self.constraints = constraints

    def meets_constraints(self):
        for meets_constraint in self.constraints:
            if not meets_constraint(self):
                return False

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def remove_constraint(self, constraint):
        self.constraints.remove(constraint)


class DatetimeRange:

    def __init__(self, begin, end=None, length=None):
        if not end:
            if length:
                end = begin + length
            else:
                raise ValueError(('DatetimeRange must have either an end ',
                                  'datetime or a length'))
        if end < begin:
            raise ValueError('end must come after begin')

        self.begin = begin
        self.end = end

    def __eq__(self, dt_range):
        return self.begin == dt_range.begin and self.end == dt_range.end
        
    @property
    def length(self):
        return self.end - self.begin

    def in_range(self, dt):
        return dt >= self.begin and dt < self.end

    def overlaps(self, dt_range):
        return self.in_range(dt_range.begin) or dt_range.in_range(self.begin)

    def connects(self, dt_range):
        return dt_range.end == self.begin or self.end == dt_range.begin

    def divides(self, dt_range):
        return self.begin > dt_range.begin and self.end < dt_range.end

    def intersect(self, dt_range):
        if self.overlaps(dt_range):
            return DatetimeRange(max(self.begin, dt_range.begin),
                                 min(self.end, dt_range.end))
        return None

    def union(self, dt_range):
        if self.overlaps(dt_range) or self.connects(dt_range):
            return [DatetimeRange(min(self.begin, dt_range.begin),
                                  max(self.end, dt_range.end))]
        return [self, dt_range]

    def subtract(self, dt_range):
        if dt_range.begin == dt_range.end:
            return [self]
        if self.overlaps(dt_range):
            if self.divides(dt_range):
                return []
            if dt_range.divides(self):
                return [DatetimeRange(self.begin, dt_range.begin),
                        DatetimeRange(dt_range.end, self.end)]
            if dt_range.begin <= self.begin:
                return [DatetimeRange(dt_range.end, self.end)]
            return [DatetimeRange(self.begin, dt_range.begin)]
        return [self]
            


class Task(Constrained):

    def __init__(
            self, name,
            priority=1,
            available_dt_ranges=[(MINYEAR, MAXYEAR)],
            deadline=MAXYEAR,
            length=timedelta(0),
            chunk_size=timedelta(hours=1),
            min_chunk_size=timedelta(minutes=15),
            max_chunk_size=timedelta(hours=4),
            cooldown=timedelta(hours=2),
            maximum_rate_daily=timedelta(hours=10),
            minimum_rate_daily=timedelta(hours=2)):

        self.set_ranges(datetime_ranges)
        self.name = name
        self.priority = priority
        self.deadline = deadline
        self.length = length
        self.chunk_size = chunk_size
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.cooldown = cooldown
        self.maximum_rate_daily = maximum_rate_daily
        self.minimum_rate_daily = minimum_rate_daily

        self.events = []

    def insert(self, event):
        self.events.append(event)

    def remove(self, event):
        self.events.remove(event)

    def set_ranges(self, dt_ranges):
        dt_ranges = filter()

    def range_before_deadline(self, dt_range):
        dt_range


class Event(DatetimeRange):

    # name: string
    # begin: datetime
    # end: datetime
    # location: location
    # description: string
    # participants: users list

    def __init__(self, name, begin, end=None, length=None, location=None,
                 description=None, participants=[]):
        super().__init__(begin, end, length)
        self.location = location
        self.description = description
        self.participants = participants

    def __repr__(self):
        return ('{0.name} - begin {0.begin:%m/%d/%Y %H:%M}, '
                'end {0.end::%m/%d/%Y %H:%M}').format(self)
