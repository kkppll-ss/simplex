from typing import Tuple

import numpy as np
import sys
from standardize import standardize

epsilon = sys.float_info.epsilon


class InfeasibleError(ValueError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UnboundedError(ValueError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def solve_canonical_LP(LP_matrix: np.ndarray, bases: np.ndarray, verbose=False) -> Tuple[np.ndarray, np.ndarray]:
    assert LP_matrix.ndim == 2, \
        "LP_matrix should be a 2-dimensional vector, got {} dimension".format(LP_matrix.ndim)
    assert bases.ndim == 1, "bases should be a 1-dimensional vector, got {} dimension".format(bases.ndim)

    assert np.issubdtype(bases.dtype, np.integer), "bases should be integer, got {}".format(bases.dtype)
    assert np.issubdtype(LP_matrix.dtype, np.float), "LP_matrix should be float, got {}".format(bases.dtype)
    rows, columns = LP_matrix.shape
    assert rows - 1 == bases.size, "the size of bases should be the row number of LP_matrix minus 1. " \
                                   "got {} and {}".format(bases.size, rows)
    assert np.all(np.abs(LP_matrix[0, bases]) < epsilon), \
        "we want the coefficients of basic variables in the objective function to be 0, get {}".format(LP_matrix[0])
    assert not np.any(LP_matrix[1:, columns-1] < -epsilon), \
        "we want the right side to be positive, get {}".format(LP_matrix[1:, columns-1])

    it = 0
    while True:
        it += 1

        c = LP_matrix[0, :columns - 1].view()
        A = LP_matrix[1:, :columns - 1].view()
        b = LP_matrix[1:, columns - 1].view()

        # get the indices of negative coefficients in the objective function
        neg_obj_coefs = np.where(c < -epsilon)[0]
        if not neg_obj_coefs.size:
            solution = np.zeros_like(c)
            solution[bases] = b
            solution_value = -LP_matrix[0, columns - 1]
            if verbose:
                print("solution got!")
            return solution, solution_value

        i_enter = neg_obj_coefs[0]
        variable_coefs = A[:, i_enter]
        valid_indices = variable_coefs > epsilon
        bounds = np.zeros_like(variable_coefs)
        bounds[variable_coefs < epsilon] = float('Inf')
        bounds[valid_indices] = np.divide(b, variable_coefs, where=valid_indices)[valid_indices]
        if np.all(bounds == float('Inf')):
            raise UnboundedError("no bound found for this LP, "
                                 "the LP_matrix is \n{}\nthe chosen entering variable is x_{}"
                                 .format(LP_matrix, i_enter))
        i_leave = np.argmin(bounds)
        bases[i_leave] = i_enter
        i_leave = i_leave + 1
        pivot = LP_matrix[i_leave, i_enter]
        modify = np.identity(LP_matrix.shape[0], np.float64)
        modify[:, i_leave] = -LP_matrix[:, i_enter] / pivot
        modify[i_leave, i_leave] = 1 / pivot
        LP_matrix[:, :] = np.dot(modify, LP_matrix)
        LP_matrix[i_leave, i_enter] = 1
        LP_matrix[:i_leave, i_enter] = 0
        LP_matrix[i_leave+1:, i_enter] = 0
        if verbose:
            solution = np.zeros_like(c)
            solution[bases] = b
            solution_value = -LP_matrix[0, columns - 1]
            print("After iteration {}, LP_matrix = \n{}\nbases = {}\ncurrent solution is {}, value is {}"
                  .format(it, LP_matrix, bases, solution, solution_value))


def transform_canonical(LP_matrix: np.ndarray, bases: np.ndarray, verbose=False):
    c_and_z = LP_matrix[0].view()
    A_and_b = LP_matrix[1:].view()
    transformer = c_and_z[bases]
    c_and_z -= np.dot(transformer, A_and_b)
    if verbose:
        print("After transformation, LP_matrix = \n{}\nbases = {}".format(LP_matrix, bases))


def solve_LP(LP_matrix, var_constraints, func_constraints, verbose=False):
    _, columns = LP_matrix.shape
    var_number = columns - 1
    if verbose:
        print("the input of the problem is: LP_matrix = \n{}\nvar_constraints = {}, func_constraints = {}"
              .format(LP_matrix, var_constraints, func_constraints))
    LP_matrix, neg_constraint_vars, no_constraint_vars, nolimit_extra, phase1_slack_vars, bases \
        = standardize(LP_matrix, var_constraints, func_constraints, verbose)
    if phase1_slack_vars.size:
        rows, columns = LP_matrix.shape
        c = LP_matrix[0, :columns-1].copy()
        LP_matrix[0] = 0
        LP_matrix[0, phase1_slack_vars] = 1
        if verbose:
            print("enter phase 1, input for phase 1 is \n{}".format(LP_matrix))
        transform_canonical(LP_matrix, bases, verbose)
        solution, solution_value = solve_canonical_LP(LP_matrix, bases, verbose)
        if solution_value > epsilon:
            raise InfeasibleError("phase 1 failed. The LP is not feasible")
        LP_matrix[0, :columns-1] = c
        LP_matrix[:, phase1_slack_vars] = 0
        if verbose:
            print("phase 1 end, input for phase 2 is \n{}".format(LP_matrix))
        transform_canonical(LP_matrix, bases, verbose)
    if verbose:
        print("enter phase 2")
    solution, solution_value = solve_canonical_LP(LP_matrix, bases, verbose)
    solution[neg_constraint_vars] = -solution[neg_constraint_vars]
    if no_constraint_vars.size:
        solution[no_constraint_vars] -= solution[nolimit_extra]
    solution = solution[:var_number]
    if verbose:
        print("original solution is {}, value is {}".format(solution, solution_value))
    return solution, solution_value
    