# Changelog

Versions are in order. Each one is a git commit and a file in `history/`.
Dates are the time the snapshot was saved in the working environment.

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
