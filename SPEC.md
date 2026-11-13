# Specification (as requested)

Client: a bodybuilding trainer who currently sends students workout plans on paper or as WhatsApp
messages. Goal: a compact app that produces nice workout plans as PDF files sized for a phone, with an
illustration for every exercise, ready to send to students. Version 1 is English; Persian is planned later.

## Global rules

* Web app, single HTML file. Developed as a Claude-hosted page; also meant to run from a local copy.
* Top bar identical on every page: app name left, page tabs centered, icon buttons on the right
  (dataset folder, export backup, import backup), all the same fixed height.
* Every input, select and button is 44 px high everywhere. Number fields use large -/+ buttons
  (touch-friendly), not the browser's tiny spinners. Widths are proportional to content.
* Every search box has an x button that clears all the text at once.
* Exercise data comes from the hasaneyldrm dataset (illustrated images and GIFs, 1324 exercises).
  The user picks the folder; nothing is uploaded.

## Page 1 - Exercises

* Library of exercises; each has image, name, target muscle area, plus body part, equipment, secondary
  muscles and instructions. Every field is editable. New exercises can be added with an uploaded picture.
* Layout: selected exercise large on the left (animated GIF), library list on the right with small round
  thumbnails and filters for equipment, muscle and body part.

## Page 2 - Students

* The trainer sees his students and can add new ones.
* Fields: name, sex (male default; the two avatar images as the selector, also used as the student's
  round picture), age, blood type, body type (ectomorph, mesomorph, endomorph, overweight, obese),
  height, weight, BMI computed automatically, notes.
* Follow-up timer: choose 1 week to 3 months and the date the program was given. The student's ring
  turns amber two days before the due date and red when due or overdue; overdue students are listed first.

## Page 3 - Plans

* Plans are independent templates; they are not assigned to students on this page.
* Many plans with different purposes (for example a 1-day plan for an overweight person, a 4-day plan for
  a competitor). Each has name, level (beginner, intermediate, advanced, elite), goal (muscle building,
  fat loss, strength, endurance, general fitness, competition prep), 1 to 7 training days per week,
  and a male/female body model.
* List on the right: one card per plan. Collapsed: thumbnail (whole-plan muscle effect) and summary.
  Selected means maximized: only one plan open at a time, highlighted, loaded on the left.
  With none selected the left side shows an empty state.
* Filters in a single row under the top bar: name, number of days, muscle, body part, level, goal.
* Editor (left): name with duplicate and delete icons, days per week, level, goal, body model,
  then one tab per day (with exercise count). Each day shows a small blue muscle map on top.
  A multi-day plan also shows the whole-plan map in red (in the list card).
* Day content: exercises added through a picker with filters. The picker highlights exercises already in
  the day, shows how many times each is present, and adds or removes copies from the same dialog.
  Each exercise has three controls on two lines: picture and name; sets, reps, move up/down, delete.

## Not built yet

* PDF export (phone-sized, one page per day or continuous: undecided; GIFs cannot play in PDF, so key
  frames of the animation are the idea).
* Assigning a plan to a student.
* Persian translation.

## Data model (stored in IndexedDB database `trainer-app`, key `state`)

```
state = {
  over:     { [exerciseId]: edited exercise },
  custom:   { [id]: custom exercise },
  students: { [id]: { id, name, sex: 'Male'|'Female', age, blood, height, weight, bodyType,
                      dur: days|'' , start: 'YYYY-MM-DD', notes } },
  planLib:  { [id]: { id, name, days: 1..7, level, goal, sex: 'MALE'|'FEMALE', titles: [7],
                      routines: [7 x [ { id, n, t, s, b, sets, reps } ]] } },
  plans: {}   // legacy, migrated into planLib on load
}
```
`n` name, `t` target muscle, `s` secondary muscles, `b` body part (snapshots stored in each plan row).
Export/import writes and merges the same structure as a JSON file.

## Technical notes

* Hosted pages cannot make network requests to other sites, so the page cannot call GitHub or any API.
* Muscle drawing: MuscleMap photos and path data are embedded. Dataset targets map to MuscleMap groups
  through `KEYGROUPS`; unmapped names (for example hip flexors) are listed under the figure instead.
* All four body figures are scaled by their head-to-toe bounding box (`BODY_BOX`) so heights match.
* Colors: day maps blue (`#1f7aff` primary, `#8cc4ff` secondary), whole-plan maps red (`#e5484d`, `#f5a3a6`).
