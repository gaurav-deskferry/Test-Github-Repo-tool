# Clinic Appointment Booking App — Overview

> Status: **PLANNING ONLY.** No real app code exists yet. Everything marked "guessed" is listed in [07_decisions.md](07_decisions.md) for you to confirm.

## What it is
A small website where a clinic's patients book visits with a doctor, the receptionist manages the day's schedule, and doctors see who is coming next.

## Who it is for
- **Patients**: want to book, move or cancel a visit without phoning.
- **Receptionists**: want one place to see the whole day, add walk-ins and handle changes.
- **Doctors**: want a clean list of today's patients and a way to mark who came.

The clinic is assumed to be **one clinic, a few doctors (about 2–5), a few hundred patients** (guessed).

## In scope (version 1)
- Sign in for the three roles.
- Patients: find a free time, book, reschedule, cancel, see their visits.
- Receptionist: see all doctors' calendars, book for a patient by phone, add walk-ins, reschedule/cancel for anyone, mark no-shows, block a doctor's leave.
- Doctor: day view, mark visit as done / no-show, add a short note (guessed).
- Clinic opening hours and fixed-length time slots.
- Reminders (first as on-screen / mock, later real email).

## Out of scope (version 1)
- Payments and invoices.
- Medical records, prescriptions, test results.
- Insurance handling.
- Video consultations.
- Several clinic branches.
- Mobile apps (the website will work on phones, but no app-store app).
- Waiting lists and recurring appointments.

## 2-minute summary
1. A patient signs in, picks a doctor and a day, sees free times, taps one, confirms. Done.
2. They can move or cancel it later, as long as it is not too close to the start time.
3. The receptionist sees every doctor's day in one screen, can book on behalf of callers, add walk-ins, and handle no-shows.
4. The doctor sees only their own day, in order, and marks each patient as done or no-show.
5. The app never lets two people take the same time with the same doctor, never lets booking in the past or on a doctor's leave.
6. We build it in 4 phases. After each one you can open something and judge it (see [05_phases.md](05_phases.md)).

## Document map
| File | What you will find |
|---|---|
| [01_users_and_flows.md](01_users_and_flows.md) | Roles and step-by-step flows, including problems |
| [02_screens.md](02_screens.md) | Every screen, button and layout sketch |
| [03_data_and_rules.md](03_data_and_rules.md) | The information stored and the business rules |
| [04_architecture.md](04_architecture.md) | Technology and how parts connect |
| [05_phases.md](05_phases.md) | Build phases, effort, risks |
| [06_test_plan.md](06_test_plan.md) | How we check each phase |
| [07_decisions.md](07_decisions.md) | Questions for you, with safe defaults |
| [../prototype/index.html](../prototype/index.html) | Clickable look-and-feel prototype (fake data) |
