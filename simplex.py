import numpy as np
from solve_simplex import solve_LP, InfeasibleError, UnboundedError


def main():
    num_var, num_fun = input().split()
    num_var, num_fun = int(num_var), int(num_fun)

    LP_matrix = []
    func_constraints = []
    c_str = input()
    c = list(map(float, c_str.split()))
    c.append(0)
    LP_matrix.append(c)
    for _ in range(num_fun):
        constraint_str = input()
        *row_i, func_constraint_i = constraint_str.split()
        row_i, func_constraint_i = list(map(float, row_i)), int(func_constraint_i)
        LP_matrix.append(row_i)
        func_constraints.append(func_constraint_i)
    var_constraints_str = input()
    var_constraints = var_constraints_str.split()
    var_constraints = list(map(int, var_constraints))

    LP_matrix = np.array(LP_matrix)
    func_constraints = np.array(func_constraints)
    var_constraints = np.array(var_constraints)

    try:
        solution, solution_value = solve_LP(LP_matrix, var_constraints, func_constraints, verbose=True)
        # +0 is use to format negative 0
        print("1\n{0:.4f}\n{1}".format(solution_value + 0, " ".join("{0:.4f}".format(cell + 0) for cell in solution)))
    except UnboundedError:
        print("0")
    except InfeasibleError:
        print("-1")


if __name__ == '__main__':
    np.set_printoptions(precision=4, suppress=True)
    main()

