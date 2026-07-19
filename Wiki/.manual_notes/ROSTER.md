# Manual Notes Roster

This roster lists the wiki surfaces that are intentionally preserved across compiles.
The compiler skips the `.manual_notes` directory so these notes remain verbatim.

---

| Surface | Why it is preserved |
|---|---|
| `Wiki/Home.md` footer | The navigation footer is maintained by hand and kept visible in the generated home page. |
| `Wiki/Falsifiability_Report.md` | Manual-audit classifications and narrative context are preserved as an editorial surface. |
| `Wiki/.manual_notes/entries/*.md` | Manual DRI notes and session annotations stay intact between compiles. |

---

## Current manual entry files

- *No manual entry files yet.*

---

## Usage

- Add a new manual note under `Wiki/.manual_notes/entries/`.
- Re-run the compiler; files under `.manual_notes` remain untouched.
- Keep the roster updated when Luis adds or removes preserved surfaces.
