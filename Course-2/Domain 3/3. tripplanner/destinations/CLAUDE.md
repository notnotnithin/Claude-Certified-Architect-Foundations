# destinations/ — Directory-Level Instructions (DIRECTORY-LEVEL)

This CLAUDE.md sits **inside the `destinations/` folder**. It is directory-level
memory: Claude Code loads it **only when it is working on files in this folder**,
on top of the project-level CLAUDE.md at the root.

## Marker (for the demo)

These instructions apply ONLY inside `destinations/`. A good way to see this on
screen: ask Claude to summarise the rules while working in `destinations/`, then
ask again about a file in `storage/` -- these extra rules should apply in the
first case and not the second.

## Extra rules for the destinations module

- Every new stop-related function must include a one-line usage example in its
  docstring, e.g.  `Example: make_stop("Jaipur", "2026-10-02", 3)`.
- Place names are always stored trimmed of surrounding spaces.
- Never abbreviate a place name (store "Bengaluru", not "Blr").

---

*CCA-Foundations · Domain 3 · TripPlanner · ANKIT MISTRY*
