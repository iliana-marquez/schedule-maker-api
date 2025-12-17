#  Schedule Maker API       

Stateless Shift Scheduling System for Multi-Location Retail Operations

### Problem:
Manual shift scheduling is time-consuming, error-prone, and difficult to optimize across multiple employees with varying availabilities, contract hours, and regulatory requirements. The existing process requires hours of manual work and is prone to human error at any given step: missed unavailability and assigned shift, official version with shifts, error when publishing manually on google calendar.'

Existing solutions force data migration and vendor lock-in.

### Solution:
An intelligent API that generates and assigns monthly work schedules across multiple business units, handling complex constraints including employee availability, contract hours, public holidays, and labor regulations.

## Business Context

### Target Users:
Store managers: Need efficient monthly schedule with minimal manual effort
Employees: Require fair shift distribution respecting ther availability
Business Owners: Want compliance with labor laws and optimised labour costs.

### Real-World Constraints:
Multi-day absences (vacations spanning multiple days)
Part-time contracts (varying weekly hours: 10h, 20h, 30h, 40h)
Austrian labor regulations (max 8 hours/day, mandatory rest periods)
Public holiday handling (mandatory closures with adjacent day shift adjustments)
Employee preferences (morning/afternoon/full-day unavailability)

### Data Flow
Input → Processing → Output