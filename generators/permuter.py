import random

# TODO Think about changing the dims parameters to be automatically detected


def get_number_permutation(dims=None, size=None):
    if dims is size is None:
        size = 9
    elif dims:
        size = dims[0] * dims[1]
    mapping = list(range(size))
    random.shuffle(mapping)
    return mapping


def get_constrained_permutation(axis=None, dims=(3, 3)):
    """
    
    Args:
        axis: Which axis to constrain on
            0 - constrain rows
            1 - constrain columns
        dims: dimensions of the board's subgrids

    Returns:
        A legal permutation mapping of the board's rows or columns
    """
    if axis is None:
        # For an m x n grid, the constraint is ambiguous, so it must be specified
        assert dims[0] == dims[1]
        # The axis doesn't matter in an n x n grid
        axis = 0
    major_axis = dims[axis - 1]
    minor_axis = dims[axis]

    mapping = [0] * major_axis * minor_axis
    large_mapping = list(range(major_axis))
    random.shuffle(large_mapping)
    for major in range(major_axis):
        small_mapping = list(range(minor_axis))
        random.shuffle(small_mapping)
        for minor in range(minor_axis):
            mapping[major * minor_axis + minor] = large_mapping[major] * minor_axis + small_mapping[minor]
    return mapping


def get_grid_permutations(permutations=(None, None, None), dims=(3, 3)):
    new_permutations = [get_constrained_permutation(axis=0, dims=dims),
                        get_constrained_permutation(axis=1, dims=dims),
                        get_number_permutation(dims=dims)]

    for i in range(3):
        if permutations[i] is not None:
            new_permutations[i] = permutations[i]

    return tuple(new_permutations)


def get_dims(grid):
    """Gets the dimensions of the grid if it is square"""
    dim = int(len(grid)**0.25)
    if dim**4 != len(grid):
        raise ValueError("Grid size must be square when dimensions are not specified")
    return dim, dim


def permute_rows(grid, permutation=None, dims=None):
    if permutation is None:
        if not dims:
            dims = get_dims(grid)
        permutation = get_constrained_permutation(axis=0, dims=dims)

    new_grid = []
    size = len(permutation)
    for row in range(size):
        for col in range(size):
            new_grid.append(grid[permutation[row] * size + col])
    return new_grid


def permute_columns(grid, permutation=None, dims=None):
    if permutation is None:
        if not dims:
            dims = get_dims(grid)
        permutation = get_constrained_permutation(axis=1, dims=dims)

    new_grid = []
    size = len(permutation)
    for row in range(size):
        for col in range(size):
            new_grid.append(grid[row * size + permutation[col]])
    return new_grid


def permute_numbers(grid, permutation=None):
    if permutation is None:
        size = int(len(grid) ** 0.5)
        permutation = get_number_permutation(size=size)
    else:
        size = len(permutation)
    new_grid = [0]*size**2
    for i in range(size**2):
        new_grid[i] = permutation[grid[i]] if grid[i] != -1 else -1
    return new_grid


def permute(grid, permutations=(None, None, None), dims=None):
    if not dims:
        dims = get_dims(grid)
    grid = permute_rows(grid, permutations[0], dims)
    grid = permute_columns(grid, permutations[1], dims)
    grid = permute_numbers(grid, permutations[2])
    return grid


def permute_pair(puzzle, solution, permutations=(None, None, None), dims=None):
    if not dims:
        dims = get_dims(solution)
    permutations = get_grid_permutations(permutations, dims)
    puzzle = permute(puzzle, permutations)
    solution = permute(solution, permutations)
    return puzzle, solution
