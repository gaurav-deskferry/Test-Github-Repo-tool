# 06 — Test Plan

Two kinds of checks: **automatic** (the computer runs them every change) and **hands-on** (you or a tester click through). Tick boxes are for the hands-on pass at the end of each phase.

## Automatic checks (all phases)
- Rules tests: slot calculation, hours, lunch, leave, past times, 60-day window.
- Clash test: two bookings for the same doctor and time at once → exactly one succeeds.
- Cancel-window tests at 1h59m, 2h00m, 2h01m.
- Reschedule swap: if the new slot fails, the old one is kept.
- Role tests: patient cannot open reception or doctor pages or other people's bookings.
- End-to-end browser tests for each flow below.

## Phase 1 checklist
**S1 Sign in** ☐ right details work ☐ wrong password shows message ☐ each role lands on its own home
**S2 Register** ☐ creates account ☐ duplicate email refused ☐ empty fields flagged
**S3 My appointments** ☐ upcoming/past split ☐ empty message ☐ Cancel asks to confirm
**S4 Book** ☐ past/closed days disabled ☐ taken slots disabled ☐ lunch has no slots ☐ no-slots message and "next free day"
**S5–S6 Confirm/done** ☐ details correct ☐ "just taken" error when second window books first ☐ failed save books nothing
**S7 Reschedule** ☐ old kept if new fails ☐ blocked inside 2 hours
**Flows** ☐ Book ☐ Reschedule ☐ Cancel ☐ Double booking ☐ Past date ☐ Sign out then protected pages redirect to sign in

## Phase 2 checklist
**S8 Day board** ☐ all doctors shown ☐ colours match status ☐ day arrows work ☐ free cell starts a booking
**S9 Walk-in** ☐ finds existing patient ☐ new patient created ☐ next free slot offered ☐ "Add as extra" only when full, tagged
**S13 Patients** ☐ search by name and phone ☐ no duplicate on same phone
**Flows** ☐ Phone booking ☐ Walk-in ☐ Receptionist override cancel with reason ☐ Receptionist cannot see doctor notes

## Phase 3 checklist
**S11 Doctor day** ☐ only own patients ☐ time order ☐ empty day message ☐ leave banner
**S10 Details** ☐ Done / No-show change status ☐ note saved, visible to doctor only ☐ Undo no-show same day
**S12 Leave/hours** ☐ leave removes slots ☐ affected bookings listed ☐ clinic-cancel notifies patient ☐ closed date has no slots
**Flows** ☐ No-show after grace ☐ "Late?" tag ☐ 3 no-shows warning ☐ Doctor on leave cannot be booked

## Phase 4 checklist
☐ 24h and 2h reminders arrive once each ☐ none sent for cancelled bookings ☐ moved booking gets new reminders ☐ password reset works ☐ phone-size layouts usable on all screens ☐ keyboard-only booking possible ☐ backup can be restored ☐ pilot week with real staff: list of problems closed

## Edge cases to try by hand (every phase)
- Two browsers, same slot, click at the same moment.
- Leave the confirm page open until the slot time passes.
- Book at 23:59 / around clock changes (daylight saving).
- Very long reason text; names with accents.
- Slow or dropped network on Confirm.

## Done means
All automatic checks green, the phase checklist fully ticked, and you have approved what you opened.
