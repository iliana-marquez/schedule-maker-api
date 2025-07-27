"""
The Calendar Service is the google calendar connection
between the tool and the caller, where working shifts of
active employees are fetched and published.
"""

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, date, time
from typing import List, Dict
from dateutil.parser import parse
import calendar
from models.employee import Employee

SCOPE = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events"
]

CREDS = Credentials.from_service_account_file('./creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
CALENDAR_SERVICE = build('calendar', 'v3', credentials=SCOPE_CREDS)


class ShiftCalendar:
    def __init__(self, employees: List[Employee]):
        self.service = CALENDAR_SERVICE
        self.employees = employees

    def fetch_current_shifts(self) -> Dict[str, List[dict]]:
        """
        Fetches current month shifts for
        all employees by calendar ID.
        Returns:
            {employee_id: [shift_dict, shift_dict, ...]}

        """
        # Auto-calculate current month boundaries
        today = date.today()
        start_date = date(today.year, today.month, 1)
        end_date = date(today.year, today.month,
                        calendar.monthrange(today.year, today.month)[1])

        current_shifts_by_employee = {}

        for employee in self.employees:
            events = self._fetch_events(
                employee.work_calendar_id,
                start_date,
                end_date)
            parsed_events = [self._parse_shift_event(e) for e in events]
            current_shifts_by_employee[employee.employee_id] = parsed_events

        return current_shifts_by_employee

    def publish_upcoming_shifts(self, schedule: Dict[str, List[dict]]):
        """
        Publishes the generated shifts to Google Calendar.
        Args:
        schedule: Dict of employee_id -> List[shift_dict]
        """
        for employee in self.employees:
            employee_schedule = schedule.get(employee.employee_id, [])
            for shift in employee_schedule:
                self._create_event(employee.work_calendar_id, shift)

    # --------------------------
    # Internal helper methods
    # --------------------------

    def _fetch_events(
            self,
            calendar_id: str,
            start: date,
            end: date) -> List[dict]:
        start_iso = datetime.combine(start, time.min).isoformat() + 'Z'
        end_iso = datetime.combine(end, time.max).isoformat() + 'Z'

        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=start_iso,
            timeMax=end_iso,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])

    def _parse_shift_event(self, event: dict) -> dict:
        start_str = event['start'].get('dateTime') or event['start'].get('date')
        end_str = event['end'].get('dateTime') or event['end'].get('date')
        return {
            'title': event.get('summary'),
            'start': parse(start_str),
            'end': parse(end_str),
        }

    def _create_event(self, calendar_id: str, shift: dict):
        event = {
            'summary': shift['summary'],
            'start': {'dateTime': shift['start'].isoformat(),
                      'timeZone': 'Europe/Amsterdam'},
            'end': {'dateTime': shift['end'].isoformat(),
                    'timeZone': 'Europe/Amsterdam'},
        }
        self.service.events().insert(
            calendarId=calendar_id, body=event
            ).execute()


# if __name__ == "__main__":
#     from models.employee import Employee
#     # Example employee with dummy calendar id
#     employees = [
#         Employee(
#             employee_id="123",
#             first_name="Alice",
#             contract_hours_per_week=40,
#             work_calendar_id="vcrk5gevoffaskkl57rbl3q1n8@group.calendar.google.com",
#             unavailability=[],
#             businessunit="BU1"
#         ),
#         Employee(
#             employee_id="124",
#             first_name="Alico",
#             contract_hours_per_week=40,
#             work_calendar_id="vcrk5gevoffaskkl57rbl3q1n8@group.calendar.google.com",
#             unavailability=[],
#             businessunit="BU1"
#         )
#     ]

#     cal = ShiftCalendar(employees)
#     shifts = cal.fetch_current_shifts()
#     print(shifts)

#     # To test publish, create a dummy schedule with the same keys as
#       _parse_shift_event returns
#     test_schedule = {
#         "123": [
#             {
#                 "summary": "Test Shift",
#                 "start": datetime.now(),
#                 "end": datetime.now() + timedelta(hours=8)
#             }
#         ],
#         "124": [
#             {
#                 "summary": "Test Shift 2",
#                 "start": datetime.now(),
#                 "end": datetime.now() + timedelta(hours=4)
#             }
#         ],
#     }
#     cal.publish_upcoming_shifts(test_schedule)