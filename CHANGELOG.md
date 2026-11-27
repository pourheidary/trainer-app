# Changelog

Every step of the Trainer App, from the first page to the current version. Each version is a file
(`trainer-app-vX.Y.html`) and a git commit/tag. Newest entries are at the bottom.

How to read this file: **v0.x and v1.0** were recorded exactly when they were saved. **v1.1 to v1.16** were
made quickly, one request after another; only v1.1, v1.7, v1.10 and v1.12 were kept as files, so those versions
are described together by feature, not one by one. **v1.17 onward** are recorded one by one.

## Not saved (cannot be recovered byte for byte)

Between v0.1b and v0.2 the single hosted file `trainer-app.html` was created and then edited in place many
times, and no copy was taken in between. Those intermediate states (folder picker and two-column layout,
then the Students page, then the first Plan page, the plan picker filters and the fixed header grid) exist
only inside v0.2, which already contains all of them. The script that embedded the MuscleMap figures
(between v0.2 and v0.3) was run inline and not saved either; the result is v0.3.

## v0.1a - Page 1, first version (`history/v0.1a-index.html`)
Exercise library page loaded from `data/exercises.json` through a local server. Cards with image, name,
target muscle; search; three filters; edit dialog; add exercise; edits kept in IndexedDB; export/import.
Reconstructed exactly by reversing the three small edits of v0.1b (round trip verified).

## v0.1b - GIF in the edit dialog (`history/v0.1b-index.html`)
The edit dialog shows the animated GIF; cards still use the static image.

## v0.2 - Hosted single-file app (`history/v0.2-pre-musclemap.html`)
Pages Exercises, Students, Plan. Dataset folder picker (no server needed). Library list on the right,
selected exercise large on the left. Students: name, age, height, weight, notes. Plan: student picker,
1 to 7 days, day tabs, exercise picker with equipment/muscle/body-part filters and a clear button,
sets and reps, hand-drawn SVG muscle figure. Fixed header grid.

## v0.3 - MuscleMap figures (`history/v0.3-musclemap.html`)
Hand-drawn figure replaced by the photoreal grey body with colored muscles (MuscleMap, MIT). Male and
female toggle. Primary muscles dark, secondary light.

## v0.4 - Plan library and student fields (`history/v0.4-plan-library.html`, `tools/patch2.py`)
Icon buttons in the header with fixed height. Plans became a library of independent templates (name,
level, goal, 1 to 7 days) with duplicate and delete. Plan filters. Clear button on every search box.
Students: sex, blood type, body type, automatic BMI, follow-up timer with color status.
Per-day map in blue and whole-plan map in red.

## v0.5 - Plan thumbnails and tabs (`history/v0.5-thumbnails.html`, `tools/patch3.py`)
Small whole-body thumbnail for every plan, enlarged when selected. Filters in one row at the top.
Training days under the plan name; duplicate and delete as icons. Day tabs with exercise counts.
All four bodies drawn at the same height (bounding boxes normalised).

## v0.6 - Per-plan body model and touch controls (`history/v0.6-touch-controls.html`, `tools/patch4.py`)
Male/female belongs to the plan. Front/Back captions removed. Large +/- steppers for age, height,
weight and sets. Student form layout: name beside sex; age, blood type and body type in one row.

## v0.7 - Accordion plans and picker with counts (`history/v0.7-accordion.html`, `tools/patch5.py`)
Selecting a plan means maximizing it; the chevron sits inside the highlighted card; nothing selected
shows an empty state. Exercise picker highlights selected rows, shows a count, allows adding the same
exercise several times and removing one from the same dialog. All inputs, selects and buttons 44 px high.
Exercise rows in the day list use three lines.

## v1.0 - Compact widths and avatars (`history/v1.0-current.html`, `tools/patch6.py`)
Sets and reps controls narrower and on one line with the move/delete buttons. Male and female symbols are
the supplied avatar images; student avatars use them with a colored follow-up ring. Vecteezy attribution.

## v1.1 to v1.16 - Programs, popups, charts and look (grouped; saved files: v1.1, v1.7, v1.10, v1.12)
The exact version of each item below was not recorded, but all of them were in place by v1.12, except the
face avatars, which are the current avatar images and were finished before v1.17.
* **Programs given to students:** a student keeps a history of programs. "Assign program" copies a library plan
  into the student's record, so editing the library plan later does not change what the student was given.
  "Edit program" opens the student's own copy in the Plan page with a bar that says so and a "Back to student" button.
  Each record has a date, follow-up reminder, notes and (at that time) the measurements.
* **Follow-up reminder:** green, amber and red status from the date a program was given plus the chosen follow-up time.
* **Exercise information popup:** clicking an exercise opens a popup with the animation, muscle map and instructions.
* **Supersets:** exercises in a day can be grouped as a superset; each group has its own color, number badge and left border.
* **Body-part chart** on each plan: bars per body part with dotted guide lines at 3, 10 and 20 sets and color tiers
  (v1.12: tiers end exactly at the guide lines; 1, 2 and 3 sets have different bar widths).
* **"Designed for" (men or women)** selector on the plan, shown with the male and female symbols.
* **Header GitHub button** (only inside Claude) that downloads the current version as a file for GitHub, with a red dot when
  the version has not been saved yet. Toast messages for confirmations.
* **One button style:** filled buttons everywhere, one common hover color; all controls 44 px high; plus/minus steppers for
  numbers; icons aligned in the supersets row.
* **New face avatars** for male and female (embedded as small images) replacing the earlier avatar pictures.
* **Plan list row:** thumbnail of the two body views, name and a small line with days, level and goal.
* Smaller layout fixes in the exercise page (image/popup size), widths of sets and reps boxes, and the filter bar.

## Hosting and data steps (not app versions, but part of the history)
1. Dataset hasaneyldrm/exercises-dataset (1324 exercises) is used with the creator's permission.
2. The data was slimmed to English only: `exercises.json` went from 16.59 MB to 0.96 MB (`make-slim-data.py`).
3. Private GitHub repo `trainer-app`; pushes with a fine-grained access token. Images (1324) pushed in one go after raising
   `http.postBuffer`; the 1324 animation files pushed in batches with `push-videos.command`.
4. Cloudflare Workers (static assets, `wrangler.jsonc`, no build command) deploys automatically on every push:
   https://trainer-app.darvagdarvag.workers.dev
5. `save-to-github.command`: copies the newest `trainer-app*.html` from Downloads to `app/`, keeps a copy in `history/`,
   commits, tags and pushes.
6. Student and plan data live in each browser's own storage, so the website starts empty; data was moved from the Claude
   page to the website with Export and Import.


## v1.17 - Data comes from folders next to the app
The exercise data, images and animations are read from the `data`, `images` and `videos` folders next to the page.
The folder picker was removed from the website version.

## v1.18 - Folder picker only inside Claude
Inside Claude the dataset folder picker is still offered (the page has no folders beside it there). On the website the
picker and the GitHub button are hidden and the data is read automatically.

## v1.19 - Export works inside Claude
The Export button uses the Claude save dialog when the page runs inside Claude (the normal browser download was blocked
silently there). On the website it still downloads a file.

## v1.20 - Export and Import icons
The two backup icons were swapped so that Export (data leaves the app) points out and Import (data comes in) points in.

## v1.21 - Student page like the plan page
Name box on top with the male/female buttons and a delete icon, no Save button (changes save by themselves), and birth
date, age and blood type in one row.

## v1.22 - Student profile and assign dialog
* The delete icon stays on the first row; the name box shrinks to make room.
* Height, weight, BMI and body type moved from the assign dialog into the student profile (they are saved automatically).
  Existing students get the values of their latest program. When a program is assigned, the current measurements are copied
  into that record, so the history still shows what they were at that date.
* The program chooser in the assign dialog looks like the plan list (thumbnail, name, details) instead of a plain select.
* A male student sees only men's plans; a female student only women's plans.

## v1.23 - Working delete buttons and cleaner student page
* Delete did nothing inside Claude because the browser's built-in confirmation box is blocked there. The app now has its own
  confirmation box ("Are you sure?" with Cancel and a red Delete button). Used for deleting a student, a plan, an assigned
  program and a custom exercise.
* New plans and new students are male by default; the trainer can change it.
* Student page spacing fixed (labels and fields were running together).
* The program chooser became a drop-down that opens and closes.
* Each program card in a student's history has a red Delete button (removes that whole record: program, measurements, notes).

## v1.24 - Dropdown height, three-line plan rows, student row
* The program drop-down opens as a floating list over the dialog, so the dialog keeps its height. It shows about three plans and
  scrolls for the rest; clicking outside closes it.
* Plan rows (Plan page list and the assign dialog) use three lines: name; days and level; goal in the accent color. Fonts and sizes unchanged.
* Student profile, second line: birth date, age, blood type (narrower), body type, all on one line. Age is a grey, dashed,
  read-only box labelled "Age (auto)", calculated from the birth date.
* This changelog is now kept up to date with every version.

## v1.25 - Program history cards
* "(auto)" removed from the Age label so it stays on one line (the box is still grey, dashed and read-only).
* Programs in a student's history are numbered; the newest is always 1 and at the top (`1- 2026-11-17`).
* Each card shows the plan like the plan list: picture, then name, "days · level" and the goal in the accent color.
* The follow-up length is written after the program name in orange, in brackets, e.g. `Aghaye2 (3 weeks)`.
  The old "Follow-up after 3 weeks" text was removed from the measurements line.
* Under the picture: the student's body measurements at that date (`180 cm · 80 kg · BMI 24.7 · Normal · Mesomorph (athletic)`).
* The last line of the newest card is the green/amber/red follow-up status with the days left.

## v1.26 - Number badges and follow-up length
* The orange follow-up length, e.g. `(3 weeks)`, moved to the first line of a program card, right after the date (it was after the plan name).
* Program numbers in a student's history use the same grey number badge as the exercise rows of a day.
* The exercise count on each day tab (Day 1, Day 2, ...) uses the same grey badge instead of the older oval.

## v1.27 - Exercise rows in the plan editor
* First line of each exercise: number badge, picture, name, and the remove button (X) at the far end. Long names wrap onto several lines and the X stays at the top right.
* Second line, always one row: move up, move down, sets, reps, superset button.
* The last exercise of a day shows the superset button greyed out (there is no next exercise to link with).
* **Bug fix:** the superset button did nothing (an error about a missing colour list, present since about v1.12). It now links an exercise with the next one (labels 1A, 1B, ...), chains three, and unlinks again; each group has its own colour.
* **Bug fix:** on phone width the plan editor was wider than the screen; the page layout now shrinks to fit.

## v1.28 - Round remove buttons
* The remove button of an exercise in the plan editor is now an empty circle with a red outline and a red X (it was a filled square).
* The same circle replaces the Delete button on program cards in the student page and sits at the far right of the first line. It still asks for confirmation.

## v1.29 - Edit a student's program in a popup
* "Edit program" on the student page no longer jumps to the Plan page. It opens the same plan editor (name, level, goal, days, sex, day tabs, exercises, sets, reps, supersets, muscle maps) in a popup on the student page.
* Changes affect only that student's own copy of the program; the plan in the library is never changed. Close with "Done" or Escape; the program card refreshes.

## v1.30 - Pencil button for editing a program
* The "Edit program" text button is replaced by a blue circle with a pencil, the same size and shape as the red remove circle, placed right next to it at the end of the first line of the program card. Greyed out when the record has no program.
* "Edit details" stays as a text button at the bottom of the card.

## v1.31 - Close the program editor by clicking outside
* Clicking on the dark area outside the student program editor popup closes it (same as Done). Pressing the mouse inside the popup and releasing outside, for example when selecting text, does not close it.

## v1.32 - Popups, icons, exercise counts, add-exercise list
* Every popup closes when you click outside it (add exercise, edit exercise, assign program, confirmation boxes, exercise details, program editor). Selecting text inside and releasing outside does not close it.
* The plus, minus and arrow signs inside buttons are now drawn icons, centred with equal space above and below (they were text characters sitting low). Used in the sets/reps/height/weight steppers, the add-exercise list and the move up/down buttons.
* Exercise counts: the day heading shows `Muscles worked on day 1 (7 Exercises)` in a smaller size and updates the moment an exercise is added or removed. The whole-plan map (in the plan list) shows `(N Exercises)` for the active days.
* Add-exercise popup: hovering highlights the whole row up to its right edge, in grey; chosen exercises are blue, so the two are easy to tell apart.
* Add-exercise popup: typing in the search box (or changing a filter) scrolls the list back to the top.

## v1.33 - Import a plan from Excel, shorter headings
* New **Import plan** button on the Plan page, next to + New plan. It opens a small popup with two steps: download the sample file, then choose your filled Excel (.xlsx) file.
* The Excel file has a sheet **Plan** (Name, Days, Level, Goal, Sex) and a sheet **Exercises** (Day, Day title, Exercise name, Sets, Reps, Superset). A third sheet, How to fill, explains the rules. One plan per file.
* Exercise names are matched to the library (not case sensitive). Unknown names are skipped and listed after the import. Sets and reps are whole numbers; rows of the same day with the same Superset letter next to each other become a superset.
* The imported plan is added to the plan library and opened. If the file is not a valid Excel file, the popup says so and nothing is changed. Works without any internet library.
* The sample file `sample-plan-import.xlsx` (a 3-day split with real library names) can be downloaded from the popup and is also delivered with this version.
* Headings shortened everywhere: `Muscles on day 1` and `Muscles in the plan`.

## v1.34 - New site icon, default students and plans
* The browser tab icon is now the bearded bodybuilder picture (embedded in the file, also used as the phone home-screen icon).
* New tick box on every student and every plan in the list, shown **only in the Claude view** (the website on Cloudflare does not show it). It sits over the right edge of the card, so card sizes and layout did not change.
* Ticked students and plans become the website defaults: pressing the save-version button (GitHub icon) now writes them into the saved file (a data block named dfData). Wherever that file runs, the defaults appear automatically in a fresh browser. A default the user later deletes in a browser does not come back there.
* The save message says how many default students and plans were included. When a saved file is sent back to Claude, its defaults are carried into later versions.

## v1.35 - Many plans per Excel file, GitHub button sends defaults
* Import button on the Plan page is now an icon (file with a down arrow) next to + New plan.
* One Excel file can hold many plans. Sheet **Plans** has one row per plan (Name, Days, Level, Goal, Sex); sheet **Exercises** now starts with a **Plan** column that names the plan each row belongs to. If a plan name already exists in the app, the imported one is added as `Name (2)` so nothing is overwritten. The result message lists every imported plan, renamed plans and skipped rows. The sample file now holds three plans (men and women).
* Default tick on plan cards moved to the top left of each collapsed card (when a card is open it sits beside the arrow). Student ticks stay at the right.
* The GitHub button (Claude view only) no longer downloads a file. It sends the ticked students and plans to the repository file `app/data/defaults.json` (a commit on main). The first time it asks for a GitHub token and keeps it only in that browser; a red dot shows when the ticks changed since the last send.
* The website (Cloudflare) reads `data/defaults.json` when it opens and shows those students and plans in any browser that has not seen them before. Ticks and the GitHub button are not shown on the website.

## v1.36 - Transparent larger icon, tick in the corner, defaults saved inside Claude
* Site icon: the white background is gone (transparent PNG, 128 px) and the picture fills the whole square. The phone home-screen icon keeps a white background, because iPhones turn transparent icons black.
* The default tick on plan cards now sits at the very top-left corner of each collapsed card.
* The GitHub button no longer tries to reach GitHub (the Claude page blocks outside connections: error NetworkError when attempting to fetch resource). It now saves the ticked students and plans into the page's own database (collections dfStudents and dfPlans, one document per item; unticked ones are removed). The token window was removed.
* Claude reads those saved defaults and writes them to `app/data/defaults.json` on GitHub when asked to push, so the website shows them.

## v1.37 - Plan tick higher
* The default tick on collapsed plan cards moved a few pixels up and left, into the very corner of the card.

## v1.38 - Plan tick 3 pixels higher
* The default tick on collapsed plan cards moved 3 pixels further up.

## v1.39 - Sample file download works in the Claude page
* Download sample file in the import popup showed the error This link can't be opened here inside the Claude page. It now uses the page's save-file feature there (with a confirmation), and still downloads normally on the website.

## v1.40 - New import icon
* The Import plans button now shows a list with a plus sign.

## v1.41 - Muscle map colours fixed on iPhone
* On iPhone Safari (and the Telegram in-app browser) the muscle figure showed the original rainbow colours of the body picture around the highlighted muscles. Safari ignores the CSS grey filter inside SVG. The grey body now uses an SVG filter (feColorMatrix) that every browser supports. On desktop Chrome the picture is pixel-identical to before.

## v1.42 - Student page: view mode, Edit and Save
* **New student** no longer creates a record right away. The form opens as a draft; the student is created only when Save is pressed (a name is required). Clicking another student, or Cancel, throws the draft away, so no empty student is ever left in the list.
* A saved student now opens in **view mode**: first line = selected face avatar, the name (not editable), an Edit button and the trash button. The saved details (birth date, age, blood type, body type, height, weight, BMI) are shown below as plain text in the same layout.
* The edit form (name, sex, birth date, blood type, body type, height, weight) opens only after Edit. Edit turns into **Save**; nothing is stored until Save is pressed. Clicking another student while editing discards the changes and shows a short notice. A Cancel button was added beside Save.
* The Programs section and Assign program stay as before in every mode (Assign program is disabled for a draft that is not saved yet). Saving a student never touches the programs already assigned.
* Phone width: height and weight now sit side by side with BMI below, so the numbers are readable.

## v1.66
- Website: defaults.json can now carry a "reset" token. When a browser sees a token it has not applied yet, it deletes all its students and plans once and loads exactly the default students and plans from defaults.json (exercise edits are untouched). Later edits are kept until the next new token.

## v1.65
- Exercise pictures are now rounded squares (48 x 48 px, 8 px corners) everywhere instead of circles: the Exercises list, the picker used to add exercises to a plan, and the plan rows. In plan view mode the picture grows from 40 to 48 px.

## v1.64
- Plan page (view and edit mode): the number ovals of normal and superset exercises now line up in one column. Superset rows moved slightly left, normal rows slightly right.

## v1.63
- New favicon: the bearded mascot supplied by the trainer (transparent background, cropped to fill the icon).
- Default plans (and students) updated from the edited ones: one new default plan and two edited plans added to data/defaults.json.

## v1.62
- Plan view mode: the day title line above the exercises is removed (the title already shows on the day tab). The list now has a heading row: "Exercise" on the left and "Sets x Reps" on the right.

## v1.61
- Plan view mode: each exercise is a single line (number, photo, name) with "Sets x Reps" at the far right (e.g. 3 x 10) under one "Sets x Reps" column heading. Long names wrap to 2-3 lines with the same line height.
- Superset marker keeps the same distance from the coloured bar as in edit mode.

## v1.60
- Plan view mode: the grey native number spinners next to Sets and Reps are hidden.

## v1.59
- Plan page: removed the 14px gap between the day tabs and their panel (a more specific margin rule was overriding the tab bar's own margin).
- Day tabs show the day's name when it has one (no "Day 1:" prefix); otherwise they show "Day N".
- View mode: Level, Goal, Days and For follow each other from the left instead of being pushed to the right edge.

## v1.58
- Plan page: a day with no exercises no longer shows the muscles section or the "Add exercises to see which muscles this day works" hint.
- Plan view mode: Level, Goal, Days and For (men/women) are on one compact line (no blue square around the day count); exercise rows are tighter, with Sets and Reps on one line.

## v1.57
- Plan page now works like the student page. A new plan starts in edit mode with only a tick (save) and a cross (cancel); it is not saved until it has a name and the tick is pressed.
- After saving, the plan is shown read-only with edit, duplicate and delete buttons. Edit mode again shows only tick and cross; nothing changes until the tick, and clicking another plan (or New plan) discards unsaved changes.
- Editing a student's own copy of a program (from the student page) is unchanged.

## v1.56
- Student view header: the text block is vertically centred, so a two-line student has equal space above and below (same as the students list).

## v1.55
- Student view header has a fixed height (room for the follow-up line) so every student's first section is the same size; long names are cut with an ellipsis instead of wrapping.

## v1.54
- Student view header now matches the students list item exactly (same photo, name, age/height/weight line and follow-up line sizes).
- The details row under it is a single line: Blood type, Body type, BMI.

## v1.53
- Student page: the full-width follow-up banner is gone; the follow-up text (same colours) now sits under the student's name without changing the header height.
- Assessments chart: left axis numbers removed, chart is wider.
- Summary line now reads e.g. "Latest: 73 kg (7 kg decrease)".

## v1.52
- Program details dialog: the Delete button is removed (a program can still be deleted with the red cross on its card).

## v1.51
- Assessments chart refined: light tinted panel, thin line with soft area, small hollow dots, smaller numbers, readable short dates (e.g. 15 Sep) that never overlap.
- Weight / BMI are now small underlined text tabs instead of big buttons.
- Student info, Assessments and Programs are separated by dividers and extra spacing.

## v1.50
- Student page: new Assessments section between the student info and the Programs, with Weight and BMI tabs. Each assigned program adds one point (from that assignment's measurements, ordered by date) to the trend chart. Hidden for new students and until the first program is assigned.

## v1.49
- Program card: equal spacing between the details, program and delete round buttons.

## v1.48
- Program card: barbell icon edits the program; the "Edit details" text button is replaced by a sliders icon placed left of the barbell, both in the same round style.

## v1.47
- Assign-program dialog: the "Assign program" button stays disabled until a program is chosen (editing an existing assignment is unchanged).

## v1.46
- Assign-program dialog: new "New Assessment" row (body type, height, weight) in one line, prefilled from the student; entering new values updates the student profile, the program card and the students list.
- "Program given on" and "Follow-up after" share one line; dialog width reduced to two thirds.
- Date fields (birth date, program date) are one box: type YYYY-MM-DD or click the calendar icon to open a Year / Month / Day pop-up (with Today for program date). Invalid typed dates are flagged and block saving.

## v1.45
- Student edit and new-student header: tick (save) and cross (cancel) buttons on one line; the trash button is only shown in view mode.

## v1.44
- Browser calendar replaced by a simple Year / Month / Day drop-down picker (birth date and program date). Birth date order is Year (left), Month, Day (right); the day list adapts to the month and leap years.

## v1.43 - Student page polish
* Removed the cancel (cross) button that was added in v1.42. Save is now the usual floppy-disk icon.
* The header (name, sex, save, trash) stays on one line in edit mode and for a new student, also on phones (the name box shrinks).
* View mode: the edit and trash buttons now sit at the right end of the header line.
* View mode: the birth date is no longer shown (the age is enough).
* View mode: the gap between a title (Height, Weight, ...) and its value is now the normal 4 px used elsewhere on the site, and rows are closer together.

## Not built yet
* Phone-sized PDF export of a plan (postponed; page per day or one continuous page not yet decided).
* Persian version of the interface (planned after the English version is final).
