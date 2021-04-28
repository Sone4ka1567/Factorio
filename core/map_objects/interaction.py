from core.map_objects.production import *
from core.virtual_objects.materials import *
from time import time


def timeit(func):
    def wrap(*args, **kwargs):
        t = time()
        res = func(*args, **kwargs)
        print(f'{func.__name__} exec time:', time() - t)
        return res

    return wrap


@timeit
def test_furnace():
    furnace = BurnerFurnace()
    furnace.put_input(Iron(10))
    for _ in range(10):
        furnace.process()

    print(furnace.input)
    print(furnace.output)


def test_ass_machine():
    machine = BurnerAssemblingMachine()
    machine.put_energy(Coal(10))
    machine.set_target(IronGearWheel)
    machine.put_input(IronPlates(9))
    for _ in range(500):
        machine.process()

    print(machine.input)
    print(machine.output)


def test_drill():
    cell = MapCell('123')
    cell.raw_material_batch = Iron(10)
    drill = BurnerMiningDrill(cell)
    drill.put_energy(Coal(10))
    for _ in range(10):
        drill.process()
        print(cell.raw_material_batch)
        print(drill.output)


test_drill()
