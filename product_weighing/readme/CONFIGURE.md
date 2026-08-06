Assign the API integration user to the **Weighing Integration** group.
Only members of this group can createweighing lines; no group can edit 
or delete them.

The three aggregate fields on the product (Total Net Weight, Weighing
Count, Weighing Confirmed At) are computed from the weighing lines, so
the integration only needs to create `product.weighing.line` records; it
does not write to `product.template`.
