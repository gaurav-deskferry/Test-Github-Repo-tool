# 02 — Screens

Every screen, its buttons and a rough sketch. The clickable [prototype](../prototype/index.html) shows the main ones with fake data.

## Screen list
| # | Screen | Who |
|---|---|---|
| S1 | Sign in | all |
| S2 | Register | patient |
| S3 | Patient home / My appointments | patient |
| S4 | Book: pick doctor, date, time | patient, receptionist |
| S5 | Confirm booking | patient, receptionist |
| S6 | Booking done | patient, receptionist |
| S7 | Reschedule | patient, receptionist |
| S8 | Receptionist day board | receptionist |
| S9 | Add walk-in | receptionist |
| S10 | Appointment details | receptionist, doctor |
| S11 | Doctor day view | doctor |
| S12 | Doctor leave & clinic hours | receptionist |
| S13 | Patients list / patient record | receptionist |

---

## S1 Sign in
```
+------------------------------+
|        Clinic Name           |
|  Email    [______________]   |
|  Password [______________]   |
|          [ Sign in ]         |
|   New patient? Register      |
+------------------------------+
```
- **Sign in**: checks details; sends patient to S3, receptionist to S8, doctor to S11. Wrong details → inline error.
- **Register** link: goes to S2.

## S2 Register
```
| Name [____]  Phone [____]    |
| Email [____] Password [____] |
| [ Create account ]  [Back]   |
```
- **Create account**: creates a patient, signs in, goes to S3. Errors shown under each field (e.g., email already used).
- **Back**: returns to S1.

## S3 Patient home / My appointments
```
+------------------------------------------+
| Hello, Anna            [Book appointment]|
| UPCOMING                                 |
| Tue 3 Dec 10:20  Dr Rao   [Reschedule][Cancel]
| PAST                                     |
| 12 Nov 09:00 Dr Lee  Done               |
+------------------------------------------+
```
- **Book appointment**: S4.
- **Reschedule**: S7 for that booking (disabled with tooltip inside cancel window).
- **Cancel**: confirm dialog, then status Cancelled.
- **Sign out**: back to S1.
- Empty state: "You have no upcoming appointments" + Book button.

## S4 Book: doctor, date, time
```
+------------------------------------------+
| 1 Doctor [ Dr Rao v ]                    |
| 2 Date   [ < Dec 2026 > calendar ]       |
| 3 Time   [09:00][09:20][09:40][10:00]... |
|          (taken times greyed)            |
| [Back]                    [Continue]     |
+------------------------------------------+
```
- **Doctor dropdown**: reloads times.
- **Calendar**: past/closed/leave days disabled; arrows change month.
- **Time buttons**: select one (highlighted); taken ones disabled.
- **Continue**: S5 (disabled until a time is chosen).
- **Back**: S3.
- Empty state: "No free times this day" + "Next free day" button.

## S5 Confirm booking
```
| Dr Rao · Tue 3 Dec · 10:20–10:40         |
| Reason (optional) [__________]           |
| [Change]                    [Confirm]    |
```
- **Confirm**: saves; on success S6; if taken, error and back to S4 with fresh times.
- **Change**: back to S4.

## S6 Booking done
```
|  ✔ Booked!  Tue 3 Dec 10:20 with Dr Rao  |
|  Reminder: 24h before.                   |
|  [My appointments]  [Book another]       |
```
- **My appointments**: S3. **Book another**: S4.

## S7 Reschedule
Same as S4 with header "Moving: Tue 3 Dec 10:20" and button **Confirm move** instead of Continue. **Keep original** goes back without changes.

## S8 Receptionist day board
```
+--------------------------------------------------------+
| < Tue 3 Dec >  [Today]  [Add walk-in] [Book for patient]|
|  Time | Dr Rao        | Dr Lee        | Dr Kim(Leave)  |
| 09:00 | Anna  Booked  | (free)        |  ///////       |
| 09:20 | Ben  Arrived  | Cara Booked   |  ///////       |
| 09:40 | (free)        | Dan No-show   |  ///////       |
+--------------------------------------------------------+
```
- **< / > / Today**: change day.
- **Add walk-in**: S9.
- **Book for patient**: S4 with patient search first.
- **Click a free cell**: starts booking for that doctor/time.
- **Click a booked cell**: S10.
- Colours: Booked = blue, Arrived = green, Done = grey, No-show = red, Leave = hatched.

## S9 Add walk-in
```
| Patient [search name/phone____] [New patient]|
| Doctor  [Dr Rao v]  Next free: 10:40         |
| Reason  [____]                               |
| [Cancel]  [Add as extra]  [Add walk-in]      |
```
- **Search**: lists matches; click selects.
- **New patient**: inline name + phone fields.
- **Add walk-in**: creates appointment, status Arrived, returns to S8.
- **Add as extra**: only when no slot is free; overbooks with a visible "Extra" tag.
- **Cancel**: back to S8.

## S10 Appointment details
```
| Anna Lopez · 0412 345 678                |
| Dr Rao · Tue 3 Dec 10:20 · Booked        |
| Reason: cough  Note: [__________]        |
| [Arrived][Done][No-show][Reschedule][Cancel]|
```
- **Arrived / Done / No-show**: change status (Done and note are available to doctor; Arrived to receptionist; No-show both).
- **Reschedule / Cancel**: S7 / confirm dialog (override of cancel window for receptionist).
- **Save note**: stores note (doctor only, guessed).
- **Back**.

## S11 Doctor day view
```
+------------------------------------------+
| Dr Rao   < Tue 3 Dec >   [Today]         |
| 09:00 Anna Lopez  cough       Booked  > |
| 09:20 Ben Ito     checkup     Arrived > |
| 09:40 —free—                             |
| Next: Ben Ito (Arrived)                  |
+------------------------------------------+
```
- **Arrows / Today**: change day.
- **Row**: S10.
- **Mark done / Mark no-show** quick buttons on each row.
- Empty and leave states as in flows.

## S12 Leave & clinic hours (receptionist)
```
| Doctor leave                             |
| Doctor [Dr Kim v] From [date] To [date]  |
| [Add leave]                              |
| Affected bookings: 3  [Review & cancel]  |
| Clinic hours: Mon–Fri 09:00–17:00 [Edit] |
```
- **Add leave**: saves; lists affected bookings.
- **Review & cancel**: cancels them as "by clinic" after confirm.
- **Edit hours**: change open/close per weekday and closed dates.

## S13 Patients
```
| Search [______]  [New patient]           |
| Anna Lopez  0412…  No-shows: 0           |
```
- **Search**, **New patient**, **row click** → patient record with their appointment history and **Book for patient**.

## Shared parts
- **Top bar**: clinic name, user name and role, **Sign out**.
- **Dialogs**: confirm cancel, error messages ("just taken", "time passed").
- **Messages** use plain words, never codes.
