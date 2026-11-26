# 01 — Users and Flows

Items marked **(guessed)** are assumptions to confirm in [07_decisions.md](07_decisions.md).

## Roles

### Patient
Can: register and sign in; book; see own upcoming and past appointments; reschedule; cancel (within the cancel window); see reminders.
Cannot: see other patients, doctors' notes, or other people's bookings (they only see that a time is "taken").

### Receptionist
Can: everything a patient can do *on behalf of any patient*; see all doctors' calendars; create walk-ins; create new patient records; mark arrived / no-show; cancel or move any appointment even inside the cancel window; mark a doctor on leave; edit clinic hours (guessed).
Cannot: see doctor notes (guessed).

### Doctor
Can: see own day and week; open a patient's visit details; mark done / no-show; write a short note (guessed); request leave (receptionist enters it in v1, guessed).
Cannot: see other doctors' calendars (guessed), change clinic hours.

---

## Flow 1 — Book (patient)
1. Patient signs in and taps **Book appointment**.
2. Picks a doctor (or "any doctor", guessed).
3. Picks a date. Past dates and days the clinic is closed are greyed out.
4. Sees free time slots for that day; taps one.
5. Enters a short reason (optional) and taps **Confirm**.
6. Sees a confirmation with date, time, doctor. A reminder is scheduled.

Problems:
- **No free slots that day**: message "No free times on this day. Next free day: <date>" with a button to jump there.
- **Doctor on leave**: that date is shown as "Doctor unavailable"; no slots are offered.
- **Past date/time**: cannot be chosen. If a patient keeps the page open and the time passes, Confirm is refused: "That time has passed."
- **Double booking**: if someone else took the slot while the patient was deciding, Confirm fails with "Sorry, this time was just taken," and the list of slots refreshes.
- **Patient already has a visit at that time** (even another doctor): refused (guessed).
- **Too many open bookings**: more than 3 upcoming bookings is refused (guessed).
- **Connection error**: "Could not save. Nothing was booked. Try again." The booking is only real after the confirmation screen.

## Flow 2 — Reschedule (patient or receptionist)
1. Open **My appointments** → pick a booking → **Reschedule**.
2. Same date/slot picker as booking, same doctor pre-selected.
3. Confirm. The old slot becomes free **only when** the new one is saved (so the patient never ends up with nothing).
4. Reminder is re-scheduled.

Problems:
- **Inside the cancel window** (less than 2 hours before, guessed): patient sees "Please call the clinic." Receptionist can still do it.
- **New slot taken meanwhile**: same "just taken" message; old booking stays.
- **Appointment already past / done / cancelled**: Reschedule button not shown.

## Flow 3 — Cancel (patient or receptionist)
1. **My appointments** → booking → **Cancel** → confirm dialog "Cancel this appointment?"
2. Status becomes *Cancelled*; slot becomes free immediately.

Problems:
- **Inside the cancel window**: patient blocked, told to phone; receptionist may cancel with a reason.
- **Already cancelled** (e.g., receptionist did it): friendly message, no error.
- **Doctor goes on leave**: receptionist's leave screen lists affected bookings; each is marked *Cancelled by clinic* and patients are notified (mock in v1).

## Flow 4 — Walk-in (receptionist)
1. Patient arrives without booking. Receptionist taps **Add walk-in**.
2. Searches patient by name/phone; if none, taps **New patient** and fills name + phone.
3. Picks a doctor. App shows the **next free slot** for that doctor today; receptionist accepts or picks another.
4. Confirm → appointment is created with type *Walk-in* and status *Arrived*.

Problems:
- **No free slot today for anyone**: "No free times today." Options: pick a later day, or **Add as extra** (overbook, receptionist only; marked clearly) (guessed).
- **Doctor on leave / clinic closed**: that doctor is not offered.
- **Duplicate patient**: if the phone number already exists, app offers the existing patient.

## Flow 5 — Doctor day view
1. Doctor signs in and lands on **Today**.
2. Sees list in time order: time, patient name, reason, status (Booked / Arrived / Done / No-show).
3. Taps a row to open details; taps **Mark done** after the visit; may add a note.
4. Can switch to another day with arrows.

Problems:
- **Empty day**: "No appointments today. Enjoy the quiet."
- **On leave**: banner "You are on leave today."
- **Walk-in appears mid-day**: list refreshes on reload / every minute (guessed).

## Flow 6 — No-show
1. Appointment time passes + 15 minutes grace (guessed) with status still *Booked*: it shows an amber "Late?" tag to receptionist and doctor.
2. Receptionist or doctor taps **Mark no-show**.
3. Status becomes *No-show*; slot is not reopened (it has passed).
4. The patient's no-show count goes up. At 3 no-shows in 6 months the receptionist sees a warning on the patient (guessed). No automatic blocking.

Problems:
- **Marked by mistake**: **Undo** available for the same day (guessed).
- **Patient arrives late but within the day**: receptionist sets *Arrived* instead.

## Flow 7 — Sign in / register (supporting)
- Patient registers with name, phone, email, password. Receptionist and doctor accounts are created by the clinic (guessed).
- Wrong password: "Email or password is wrong." Forgotten password: reset link (later phase).

## Conflict summary
| Situation | What the app does |
|---|---|
| Two people click the same slot | First to confirm wins; second sees "just taken" |
| Doctor on leave | No slots; existing bookings flagged for the receptionist |
| Past date/time | Cannot be picked or confirmed |
| Clinic closed (weekend/holiday) | Day shown as closed |
| Cancel too late | Patient told to call; receptionist can override |
| Network drops during booking | Nothing saved until confirmation shown |
