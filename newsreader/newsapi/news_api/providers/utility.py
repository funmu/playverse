#
#  utility.py 
#
#  Helper classes for implementing the provider
#

import datetime

class DateTimeManager:

    def get_datetime_string( self, dt_object=None, format:str="%Y-%m-%d %H:%M:%S %Z", 
        timezone=datetime.timezone.utc):
        """
        Generates a string representation of a datetime object, including 
         the time and timezone.

        Args:
            dt_object: The datetime.datetime object to format. If None, uses the 
                        current datetime.
            format: The desired format string (default includes date, time, and timezone).
            timezone: The timezone to use (default is UTC).

        Returns:
            str: The formatted datetime string.
        """
        if dt_object is None:
            dt_object = datetime.datetime.now(timezone)
        elif isinstance(dt_object, datetime.datetime) and not isinstance(dt_object, datetime.date):
            # If it's already a datetime object, just replace the timezone
            dt_object = dt_object.replace(tzinfo=timezone)  
        else:
            # If it's a date object, convert it to a datetime object
            dt_object = datetime.datetime.combine(dt_object, datetime.time(0, 0))
            dt_object = dt_object.replace(tzinfo=timezone)

        return dt_object.strftime(format)

    def test_datetime_string(self):
        # Example usage:
        datetime_str = self.get_datetime_string()  # Uses current datetime and UTC
        print(datetime_str)  # Output: 2024-11-24 04:57:30 UTC

        # With a specific datetime object and PST timezone:
        dt_obj = datetime.datetime(2023, 5, 17, 10, 30, 0)
        pst_timezone = datetime.timezone(datetime.timedelta(hours=-8))  # PST
        datetime_str = self.get_datetime_string(dt_obj, timezone=pst_timezone)
        print(datetime_str)  # Output: 2023-05-17 10:30:00 PST

        # With a custom format:
        datetime_str = self.get_datetime_string(format="%A, %B %d, %Y %I:%M %p %Z")
        print(datetime_str)  # Output: Sunday, November 24, 2024 04:57 AM UTC

# for quick test runs
# dm = DateTimeManager()
# dm.get_datetime_string()
# dm.test_datetime_string()
