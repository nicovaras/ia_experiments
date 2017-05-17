from solver import HitoriSolver


def test_is_nullable():
    nums = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    solver = HitoriSolver(nums)

    for i in range(3):
        for j in range(3):
            assert not solver.is_nullable(i, j)

    solver.set_at(0, 1, '1')
    assert solver.is_nullable(0, 0)
    assert solver.is_nullable(0, 1)

    solver.set_at(1, 0, '1')
    assert solver.is_nullable(1, 0)

    solver.set_at(2, 2, '3')
    assert solver.is_nullable(0, 2)
    assert solver.is_nullable(2, 2)

    solver.set_at(0, 0, '*')
    assert not solver.is_nullable(0, 0)
    assert not solver.is_nullable(0, 1)
    assert not solver.is_nullable(1, 0)

    nums = [['5' for _ in range(5)] for _ in range(5)]
    nums[0] = ['*', '1', '2', '3', '*']
    solver = HitoriSolver(nums)
    for i in range(5):
        assert not solver.is_nullable(0, i)
    nums[0][1:4] = ['5', '5', '5']
    assert not solver.is_nullable(0, 0)
    assert not solver.is_nullable(0, 1)
    assert solver.is_nullable(0, 2)
    assert not solver.is_nullable(0, 3)
    assert not solver.is_nullable(0, 4)


def test_still_connected():
    nums = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    solver = HitoriSolver(nums)
    assert solver.still_connected()

    solver.set_at(1, 0, '*')
    assert solver.still_connected()

    solver.set_at(0, 1, '*')
    assert not solver.still_connected()

    solver.set_at(2, 2, '*')
    assert not solver.still_connected()

    solver.set_at(0, 1, '2')
    assert solver.still_connected()

    solver.set_at(1, 1, '*')
    assert not solver.still_connected()


def test_is_solved():
    nums = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    solver = HitoriSolver(nums)
    assert solver.is_solved()

    solver.set_at(0, 0, '2')
    assert not solver.is_solved()

    solver.set_at(0, 1, '*')
    assert solver.is_solved()

    solver.set_at(1, 0, '*')
    assert not solver.is_solved()

    solver.set_at(1, 0, '9')
    assert solver.is_solved()


def test_5_x_5():
    nums = [['4', '5', '6', '3', '2'], ['1', '5', '2', '5', '2'], ['3', '4', '6', '3', '1'], ['2', '1', '1', '4', '5'],
            ['6', '2', '1', '6', '1']]
    solution = [(0, 2), (1, 1), (1, 4), (2, 3), (3, 2), (4, 0), (4, 4)]
    solver = HitoriSolver(nums)
    assert not solver.is_solved()

    for x, y in solution:
        assert solver.is_nullable(x, y)
        solver.set_at(x, y, '*')
        assert solver.still_connected()

    assert solver.is_solved()

    nums = [['4', '5', '6', '3', '2'], ['1', '5', '2', '5', '2'], ['3', '4', '6', '3', '1'], ['2', '1', '1', '4', '5'],
            ['6', '2', '1', '6', '1']]
    solver = HitoriSolver(nums)
    solver_solution = solver.solve()
    assert solver_solution is not None
    assert solver.is_solved()
