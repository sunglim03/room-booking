# 강의실 예약 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

ROOMS = ("A101", "A102", "B201")
DAYS = ("월", "화", "수", "목", "금")
OPEN_HOUR = 9
CLOSE_HOUR = 21
MAX_HOURS = 3
MAX_PER_PERSON_PER_DAY = 2


def _is_hour(value):
    """정수인지 확인 (True/False는 정수로 보지 않음)."""
    return isinstance(value, int) and not isinstance(value, bool)


def _valid_place(room, day):
    """있는 강의실·요일인지 확인 (문자열이 아니어도 에러 없이 False)."""
    return isinstance(room, str) and isinstance(day, str) and room in ROOMS and day in DAYS


class RoomBooking:
    def __init__(self):
        # (강의실, 요일) -> [(start, end, name), ...]
        self._bookings = {}

    def book(self, room, day, start, end, name):
        # 1. 없는 강의실·요일
        if not _valid_place(room, day):
            return False
        # 2. 정수가 아닌 시각
        if not _is_hour(start) or not _is_hour(end):
            return False
        # 3. 운영 시간 밖
        if start < OPEN_HOUR or end > CLOSE_HOUR:
            return False
        # 4. 시작이 끝보다 같거나 늦음
        if start >= end:
            return False
        # 5. 3시간 초과
        if end - start > MAX_HOURS:
            return False
        # 6. 같은 강의실·요일 예약과 겹침 (끝나는 시각에 시작은 허용)
        for s, e, _ in self._bookings.get((room, day), []):
            if start < e and s < end:
                return False
        # 7. 같은 사람은 같은 요일 최대 2건 (강의실 합산)
        count = 0
        for (r, d), items in self._bookings.items():
            if d == day:
                count += sum(1 for _, _, n in items if n == name)
        if count >= MAX_PER_PERSON_PER_DAY:
            return False

        self._bookings.setdefault((room, day), []).append((start, end, name))
        return True

    def cancel(self, room, day, start, name):
        if not _valid_place(room, day) or not _is_hour(start):
            return False
        items = self._bookings.get((room, day), [])
        for i, (s, e, n) in enumerate(items):
            if s == start:
                if n != name:
                    return False
                del items[i]
                return True
        return False

    def get_schedule(self, room, day):
        if not _valid_place(room, day):
            return []
        return sorted(self._bookings.get((room, day), []), key=lambda b: b[0])
