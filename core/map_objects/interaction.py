from core.map_objects.production import *
from core.virtual_objects.materials import *

furnace = BurnerFurnace()
furnace.put_input(Iron(10))
for _ in range(20):
    furnace.process()

print(furnace.input)
print(furnace.output)
