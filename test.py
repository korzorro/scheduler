from unittest import TestCase
from models import DatetimeRange
from datetime import datetime, timedelta

one_hour = timedelta(hours=1)
thirty_minutes = timedelta(minutes=30)

begin = datetime.now()
end = begin + one_hour
before = begin - thirty_minutes
before1 = before
before2 = before1 + timedelta(minutes=15)
after = end + timedelta(minutes=15)
after1 = after
after2 = after1 + timedelta(minutes=15)
during = begin + thirty_minutes
during1 = during
during2 = during + timedelta(minutes=15)
# [ )
dt_range = DatetimeRange(begin, end)
# b e [ )
begins_before_ends_before = DatetimeRange(before1, before2)
# b e[ )
connects_before = DatetimeRange(before, begin)
# b [ e )
begins_before_ends_during = DatetimeRange(before, during)
# b [ e)
begins_before_same_end = DatetimeRange(before, end)
# b [ ) e
begins_before_ends_after = DatetimeRange(before, after)
# be[
begin_begin = DatetimeRange(begin, begin)
# b[ e )
same_begin_ends_during = DatetimeRange(begin, during)
# b[ ) e
same_begin_ends_after = DatetimeRange(begin, after)
# [ b e )
begins_during_ends_during = DatetimeRange(during1, during2)
# [ b e)
begins_during_same_end = DatetimeRange(during, end)
# [ b ) e
begins_during_ends_after = DatetimeRange(during, after)
# [ be)
end_end = DatetimeRange(end, end)
# [ b) e
connects_after = DatetimeRange(end, after)
# [ ) b e
begins_after_ends_after = DatetimeRange(after1, after2)


class TestDatetimeRange(TestCase):

    def test_end_must_be_after_begin(self):
        try:
            DatetimeRange(begin, before)
        except ValueError:
            assert True
            return
        assert False

    def test_end_or_length_required(self):
        try:
            DatetimeRange(begin)
        except ValueError:
            assert True
            return
        assert False

    def test_equals(self):
        assert dt_range == dt_range
        assert dt_range != begins_before_ends_after

    def test_length(self):
        dt_range = DatetimeRange(begin, length=one_hour)
        assert dt_range.length == one_hour

    def test_in_range(self):
        assert dt_range.in_range(begin)
        assert dt_range.in_range(during)
        assert not dt_range.in_range(end)
        assert not dt_range.in_range(before)
        assert not dt_range.in_range(after)

    def test_overlaps(self):
        assert not dt_range.overlaps(begins_before_ends_before)
        assert not dt_range.overlaps(connects_before)
        assert dt_range.overlaps(begins_before_ends_during)
        assert dt_range.overlaps(begins_before_same_end)
        assert dt_range.overlaps(begins_before_ends_after)
        assert dt_range.overlaps(begin_begin)
        assert dt_range.overlaps(same_begin_ends_during)
        assert dt_range.overlaps(dt_range)
        assert dt_range.overlaps(same_begin_ends_after)
        assert dt_range.overlaps(begins_during_ends_during)
        assert dt_range.overlaps(begins_during_same_end)
        assert dt_range.overlaps(begins_during_ends_after)
        assert not dt_range.overlaps(end_end)
        assert not dt_range.overlaps(connects_after)
        assert not dt_range.overlaps(begins_after_ends_after)

    def test_intersect(self):
        assert not dt_range.intersect(begins_before_ends_before)
        assert not dt_range.intersect(connects_before)
        assert dt_range.intersect(
            begins_before_ends_during) == same_begin_ends_during
        assert dt_range.intersect(begins_before_same_end) == dt_range
        assert dt_range.intersect(begins_before_ends_after) == dt_range
        assert dt_range.intersect(begin_begin) == begin_begin
        assert dt_range.intersect(
            same_begin_ends_during) == same_begin_ends_during
        assert dt_range.intersect(dt_range) == dt_range
        assert dt_range.intersect(same_begin_ends_after) == dt_range
        assert dt_range.intersect(
            begins_during_ends_during) == begins_during_ends_during
        assert dt_range.intersect(
            begins_during_same_end) == begins_during_same_end
        assert dt_range.intersect(
            begins_during_ends_after) == begins_during_same_end
        assert not dt_range.intersect(end_end)
        assert not dt_range.intersect(connects_after)
        assert not dt_range.intersect(begins_after_ends_after)

    def test_union(self):
        assert dt_range.union(
            begins_before_ends_before) == [dt_range, begins_before_ends_before]
        assert dt_range.union(
            connects_before) == [begins_before_same_end]
        assert dt_range.union(
            begins_before_ends_during) == [begins_before_same_end]
        assert dt_range.union(
            begins_before_same_end) == [begins_before_same_end]
        assert dt_range.union(
            begins_before_ends_after) == [begins_before_ends_after]
        assert dt_range.union(
            begin_begin) == [dt_range]
        assert dt_range.union(
            same_begin_ends_during) == [dt_range]
        assert dt_range.union(
            dt_range) == [dt_range]
        assert dt_range.union(
            same_begin_ends_after) == [same_begin_ends_after]
        assert dt_range.union(
            begins_during_ends_during) == [dt_range]
        assert dt_range.union(
            begins_during_same_end) == [dt_range]
        assert dt_range.union(
            begins_during_ends_after) == [same_begin_ends_after]
        assert dt_range.union(
            end_end) == [dt_range]
        assert dt_range.union(
            connects_after) == [same_begin_ends_after]
        assert dt_range.union(
            begins_after_ends_after) == [dt_range, begins_after_ends_after]

    def test_subtract(self):
        assert dt_range.subtract(begins_before_ends_before) == [dt_range]
        assert dt_range.subtract(connects_before) == [dt_range]
        assert dt_range.subtract(
            begins_before_ends_during) == [begins_during_same_end]
        assert dt_range.subtract(
            begins_before_same_end) == []
        assert dt_range.subtract(
            begins_before_ends_after) == []
        assert dt_range.subtract(
            begin_begin) == [dt_range]
        print(dt_range.subtract(same_begin_ends_during))
        assert dt_range.subtract(
            same_begin_ends_during) == [begins_during_same_end]
