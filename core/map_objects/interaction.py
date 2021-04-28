from core.map_objects.production import *
from core.virtual_objects.materials import *
from core.map_objects.production.production import *
from core.map_objects.production.power_source import *
from time import time


def timeit(func):
    def wrap(*args, **kwargs):
        t = time()
        res = func(*args, **kwargs)
        print(f'{func.__name__} exec time:', time() - t)
        return res

    return wrap


@timeit
def test_furnace(iters):
    furnace = BurnerFurnace()
    furnace.put_energy(Coal(12))
    furnace.put_input(Iron(10))
    for _ in range(iters):
        furnace.process()

    print(furnace.input)
    print(furnace.output)


def test_ass_machine(iters):
    machine = BurnerAssemblingMachine()
    print(machine.put_energy(Coal(10)))
    machine.set_target(IronGearWheel)
    machine.put_input(IronPlates(10))
    for _ in range(iters):
        machine.process()
        print(machine)

    print(machine)


def test_el_ass_machine(iters):
    power = Power()
    power.power = 300
    machine = ElectricAssemblingMachine()
    machine.put_energy(power)
    print(machine.set_target(IronGearWheel))
    machine.put_input(IronPlates(10))

    for _ in range(iters):
        machine.process()
        print(machine)

    print(machine.input)
    print(machine.output)
    print(power.power)


def test_drill(iters):
    cell = MapCell('123')
    cell.raw_material_batch = Iron(10)
    drill = BurnerMiningDrill(cell)
    drill.put_energy(Coal(10))
    for _ in range(iters):
        drill.process()
        print(drill)


def test_el_furnace(iters):
    power = Power()
    power.power = 300
    furnace = ElectricFurnace()
    furnace.put_input(Iron(10))
    furnace.put_energy(power)
    for _ in range(iters):
        furnace.process()
        print(power.power)

    print(furnace.input)
    print(furnace.output)
    furnace.disable()
    print(power.power)


# test_ass_machine(100)
# print('-'*30)
# # test_el_ass_machine()
# test_el_ass_machine(100)

# test_el_furnace(100)
# print('-' * 30)
# test_furnace(100)

test_drill(100)

# b_furn = BurnerFurnace()
# b_furn.put_energy(Wood(10))
# print(b_furn)
