from absalg import *

field = GF(16)

for p in field:
    print repr(p)

print is_field(field)

print is_group(field[1:], addition=multiplication)
