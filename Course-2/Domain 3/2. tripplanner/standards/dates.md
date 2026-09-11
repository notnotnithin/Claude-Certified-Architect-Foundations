# Date Handling Standards

This file is pulled into the main `CLAUDE.md` using `@standards/dates.md`.
Keeping it separate means these rules can be reused or updated in one place
without making the main memory file long.

## Rules

- All dates are stored as **`YYYY-MM-DD`** strings (ISO 8601), e.g. `2026-10-02`.
- Validate dates with `datetime.strptime(date, "%Y-%m-%d")`. This rejects both
  wrong formats (`02-10-2026`) and impossible days (`2026-02-30`).
- Never store dates in day-first or month-first formats. One format everywhere
  keeps sorting and comparison correct.
- When showing a date to the user, the stored `YYYY-MM-DD` form is fine — do not
  reformat it into locale-specific styles.

---

*CCA-Foundations · Domain 3 · TripPlanner · ANKIT MISTRY*
