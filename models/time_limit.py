class TimeLimit:
    def __init__(self, weeks: int = None, days: int = None, hours: int = None, minutes: int = None):
        self.weeks = weeks
        self.days = days
        self.hours = hours
        self.minutes = minutes

    def get_seconds(self):
        total_seconds = 0
        if self.weeks is not None and self.weeks > 0:
            total_seconds += self.weeks * 7 * 24 * 60 * 60

        if self.days is not None and self.days > 0:
            total_seconds += self.days * 24 * 60 * 60

        if self.hours is not None and self.hours > 0:
            total_seconds += self.hours * 60 * 60

        if self.minutes is not None and self.minutes > 0:
            total_seconds += self.minutes * 60

        return total_seconds

    def to_string(self):
        return f'Weeks:{self.weeks} Days:{self.days} Hours:{self.hours} Minutes:{self.minutes}'
