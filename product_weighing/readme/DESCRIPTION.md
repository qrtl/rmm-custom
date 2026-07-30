This module adds an **append-only** weighing line model
(`product.weighing.line`) that stores weighing results (gross weight,
dust deduction and net weight) sent from an external system against a product.

To support the "no tampering of weighing data" claim, weighing lines are
create-only: creation is allowed only for the dedicated integration
group, and the model overrides `write` and `unlink` to always raise, so a
line can never be modified or deleted after creation through any path -
UI, RPC, `sudo` or the developer-mode superuser included (direct SQL is
out of scope by design). The parent product cannot be deleted either
while lines exist (`ondelete="restrict"`), so the trail is preserved.

The product form gets a read-only **Weighing** tab showing three
aggregate fields (computed from the lines) and the list of weighing
lines.
