# Trainer App

A single-file web app for a bodybuilding trainer: exercise library, students and weekly training plans
with per-day and whole-plan muscle maps. Built in conversation with Claude (November 2026).
The next planned feature, a phone-sized PDF export of each plan, has not been built yet.

## Run it

1. Open `app/trainer-app.html` in Chrome (double-click or drag it into the browser).
2. Click the folder icon (top right) and choose the exercise dataset folder, the one that contains
   `data/`, `images/` and `videos/`. The browser may say "upload", but files are only read locally.
3. If the browser refuses to store data when the file is opened directly, run
   `python3 -m http.server 8000` inside `app/` and open `http://localhost:8000/trainer-app.html`.
   (I did not test opening it straight from disk; the app was developed as a hosted page.)

All data you enter (edited exercises, students, plans) lives in the browser's IndexedDB for that browser
profile. Use the export icon (arrow down, top right) to make a JSON backup and the import icon to restore it.
Student data is deliberately NOT part of this repository.

## What is not in this repository

* The exercise dataset: https://github.com/hasaneyldrm/exercises-dataset (1324 exercises).
  Its images and GIFs are (c) Gym visual.
  Download it separately; the app reads it from the folder you pick.
* The original Vecteezy download (EPS/JPG). Only the two cropped round avatars are included (`assets/avatars`).

## Layout

| Path | Content |
|---|---|
| `app/trainer-app.html` | The current app. One self-contained file, about 650 KB, with the body images, muscle paths and avatars embedded. |
| `history/` | Plain-file copy of every saved version (the same versions are also git commits). |
| `tools/` | Scripts that produced the embedded data (`extract.mjs`, generated `bodies.js`, `bodybox.js`, `avatars.js`) and the patch scripts `patch2.py` to `patch6.py` that evolved the app between versions. |
| `third_party/` | MuscleMap MIT license and provenance notes, Vecteezy license information. |
| `SPEC.md` | Everything the app must do, as requested, plus the data model and technical constraints. Start here to continue the project with another tool. |
| `CHANGELOG.md` | What each version added, and which intermediate versions were never saved. |
| `save-to-github.command` | macOS double-click script: copies the newest `trainer-app*.html` from Downloads into `app/`, commits and pushes. |

## Saving a new version (macOS)

1. Download the new `trainer-app.html` from the chat; it lands in Downloads.
2. Double-click `save-to-github.command`.
   If macOS blocks it, right-click, choose Open, confirm, or run `./save-to-github.command` in Terminal.

## Third-party material

* Body figures and muscle outlines: MuscleMap (MIT), see `third_party/`.
* Avatars: Vecteezy.com. The free license requires attribution, which the app footer provides.
  Check `third_party/Vecteezy-License-Information.pdf` for the terms of your license.
* Exercise images: (c) Gym visual (see above).
