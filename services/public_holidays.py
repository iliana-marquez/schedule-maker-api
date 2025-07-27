"""
Returns the public holidays of the
upcoming month for the schedule_maker
"""
import holidays
from datetime import date
from typing import List, Dict, Any


def get_holidays_in_range(
        country_code: str,
        start_date: date,
        end_date: date) -> List[Dict[str, Any]]:
    """
    Get holidays between start and end date
    """
    all_holidays = holidays.country_holidays(
        country_code,
        years=start_date.year)

    return [{"date": holiday_date, "title": all_holidays[holiday_date]}
            for holiday_date in all_holidays
            if start_date <= holiday_date <= end_date]


# # testing
# if __name__ == "__main__":
#     # Test with Austrian holidays for August 2025
#     august_holidays = get_holidays_in_range(
#         'AT', date(2025, 8, 1), date(2025, 8, 31)
#         )

#     print(f"Found {len(august_holidays)} holidays in August 2025:")
#     for holiday in august_holidays:
#         print(f"  {holiday['date']}: {holiday['title']}")
