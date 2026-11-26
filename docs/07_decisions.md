# 07 — Decisions for You

Every item below is a **guess** I made so the docs could be written. Reply with changes, or accept the default. Nothing is built until you approve.

| # | Question | Safe default | Status |
|---|---|---|---|
| 1 | How many doctors and patients? | 2–5 doctors, a few hundred patients | guessed |
| 2 | One clinic or several branches? | One clinic | guessed |
| 3 | Visit length | 20 minutes for everyone | guessed |
| 4 | Opening hours | Mon–Fri 09:00–17:00, lunch 12:30–13:30, weekends closed | guessed |
| 5 | How far ahead can patients book? | 60 days | guessed |
| 6 | Minimum notice for a new booking | 1 hour | guessed |
| 7 | Cancel / reschedule window for patients | 2 hours before start | guessed |
| 8 | Can patients choose "any doctor"? | Yes | guessed |
| 9 | Max upcoming bookings per patient | 3 | guessed |
| 10 | Can one patient hold two overlapping bookings? | No | guessed |
| 11 | Who creates receptionist and doctor accounts? | The clinic admin (a receptionist) | guessed |
| 12 | Can patients register themselves? | Yes, with email + phone | guessed |
| 13 | Reminders: when and how? | 24h and 2h before, email only | guessed |
| 14 | Do you need SMS reminders? | No (extra cost, later) | guessed |
| 15 | No-show grace period | 15 minutes | guessed |
| 16 | No-show warning level | 3 in 6 months, warning only, no blocking | guessed |
| 17 | Can doctors write notes? Who sees them? | Yes; only that doctor | guessed |
| 18 | Can receptionist overbook ("extra")? | Yes, tagged | guessed |
| 19 | Who enters doctor leave? | Receptionist | guessed |
| 20 | Can a doctor see other doctors' calendars? | No | guessed |
| 21 | Languages | English only | guessed |
| 22 | Time zone | Single clinic time zone (please tell me which) | guessed |
| 23 | Privacy rules (e.g., HIPAA / GDPR / local law) | Keep data minimal, no medical history, HTTPS, backups; **you must confirm legal needs** | guessed |
| 24 | Technology (see doc 04) | TypeScript + Next.js + SQLite→Postgres | guessed |
| 25 | Hosting and monthly budget | One small host, low monthly cost | guessed |
| 26 | Clinic name, logo, colours | Placeholder "Riverside Clinic", calm blue/teal | guessed |
| 27 | Phase order | As in doc 05; receptionist before doctor | guessed |
| 28 | Effort estimate | 25–33 working days | guessed |

## What I need from you most
Items **1, 4, 7, 13, 22 and 23** change the most work if wrong. Please look at those first.

## Not guessed (stated by you)
- Three roles: patient, receptionist, doctor.
- Flows: book, reschedule, cancel, walk-in, doctor day view, no-show.
- Plan and docs first; no real app code until you approve.
