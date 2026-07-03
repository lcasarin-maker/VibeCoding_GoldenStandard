# CoderCerberus adversarial audit (internal, cited generically per GS/CC boundary, see Wiki/Evidence)

> Citable evidence source referenced by 1 entries in the Golden Standard catalog.

## Claims

- A test using TemporaryDirectory(dir=ROOT) leaked tmp*/empty.py into the tree on interrupted runs and flipped the D1 integrity gate to REJECTED; it recurred 3 times because prior sessions deleted the zombies instead of fixing the writer.

## Referenced by

- [[Vices/VC-087|VC-087]]

---
[[Home|Back to Home]]
