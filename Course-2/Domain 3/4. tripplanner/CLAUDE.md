# TripPlanner — Project Instructions (PROJECT-LEVEL)

This file sits at the **root of the project** and is committed to version
control, so **every teammate who clones TripPlanner gets these instructions
automatically**. This is the right place for standards that apply to the whole
project.

## Marker (for the demo)

If you ask Claude "which CLAUDE.md files are you using?", it should mention this
one as the **project-level** file. When Claude follows these rules, it proves the
project-level memory loaded.

## Project-wide coding standards

- Target **Python 3.8+**, standard library only in the app.
- Every function has a short docstring explaining *why*, not just *what*.
- Raise `ValueError` with a clear, user-facing message for bad input. Never let
  the app crash on a predictable mistake.
- Always read and write files with `encoding="utf-8"`.
- Keep the layered design: `parsing/` -> `destinations/` -> `storage/`.

## Date handling

Date rules live in their own file and are pulled in here with an import:

@standards/dates.md

---

*CCA-Foundations · Domain 3 · TripPlanner · ANKIT MISTRY*
