import numpy as np
import sys

epsilon = sys.float_info.epsilon


def std_var_constraints(LP_matrix, var_constraints):
    """
    after the operation, the LP_matrix and func_constraints is adjusted such that
    variables_constraints is all positive
    :param LP_matrix: The matrix for Linear Programming, size (m+1) x (n+1)
    :param var_constraints: type of variable constraints, size (n), dtype np.integer
    :return: LP_matrix: the LP matrix after this operation
    (neg_constraint_vars, no_constraint_vars): the indices of negative and
    no constraint variables. Used for restore original value after computation
    finished
    nolimit_extra: the extra variable added for variables without constraints, use for restoring
    their values
    """
    rows, columns = LP_matrix.shape
    neg_constraint_vars = np.where(var_constraints == -1)[0]
    LP_matrix[:, neg_constraint_vars] = -LP_matrix[:, neg_constraint_vars]
    no_constraint_vars = np.where(var_constraints == 0)[0]
    if no_constraint_vars.size:
        coefs_sum = np.sum(LP_matrix[:, no_constraint_vars], axis=1)
        LP_matrix = np.insert(LP_matrix, columns-1, -coefs_sum, axis=1)
        nolimit_extra = columns - 1
    else:
        nolimit_extra = None
    return LP_matrix, neg_constraint_vars, no_constraint_vars, nolimit_extra


def std_func_constraints(LP_matrix, func_constraints):
    """
    after the operation, the LP_matrix and func_constraints is adjusted such that
    variables_constraints is all positive
    :param LP_matrix: The matrix for Linear Programming, size (m+1) x (n+1)
    :param func_constraints: type of functional constraints, size (m), dtype np.integer
    :return: LP_matrix: the LP matrix after this operation
    phase1_slack_vars: the indices of slack variables used for phase 1
    extra_vars: other slack, surplus and artificial variables
    bases: the bases variables
    """
    rows, columns = LP_matrix.shape
    b = LP_matrix[1:, columns-1]
    A_and_b = LP_matrix[1:].view()
    neg_indices = np.where(b < -epsilon)
    A_and_b[neg_indices] = -A_and_b[neg_indices]
    func_constraints[neg_indices] = -func_constraints[neg_indices]
    bases = np.zeros(func_constraints.size, dtype=np.int64)

    LP_matrix, le_slack_vars = add_vars(LP_matrix, func_constraints, -1, 1, bases)
    LP_matrix, eq_slack_vars = add_vars(LP_matrix, func_constraints, 0, 1, bases)
    LP_matrix, ge_surplus_vars = add_vars(LP_matrix, func_constraints, 1, -1, bases)
    LP_matrix, ge_slack_vars = add_vars(LP_matrix, func_constraints, 1, 1, bases)
    extra_vars = np.hstack((le_slack_vars, ge_surplus_vars))
    phase1_slack_vars = np.hstack((eq_slack_vars, ge_slack_vars))
    return LP_matrix, phase1_slack_vars, extra_vars, bases


def add_vars(LP_matrix, func_constraints, ctype, vtype, bases):
    rows, columns = LP_matrix.shape
    constraint_indices = np.where(func_constraints == ctype)[0]
    constraint_number = constraint_indices.size
    if constraint_number:
        appended_matrix = np.zeros((rows, constraint_number))
        appended_A = appended_matrix[1:].view()
        appended_A[constraint_indices, range(constraint_number)] = vtype
        LP_matrix = np.insert(LP_matrix, [columns-1] * constraint_number, appended_matrix, axis=1)

        bases_indices = columns - 1 + np.array(range(constraint_number))
        if vtype == 1:
            bases[constraint_indices] = bases_indices
        return LP_matrix, bases_indices
    else:
        return LP_matrix, np.array([], dtype=np.int64)


def standardize(LP_matrix, var_constraints, func_constraints, verbose=False):
    LP_matrix, neg_constraint_vars, no_constraint_vars, nolimit_extra = std_var_constraints(LP_matrix, var_constraints)
    LP_matrix, phase1_slack_vars, extra_vars, bases = std_func_constraints(LP_matrix, func_constraints)
    if verbose:
        print("After standardization, LP_matrix is \n{}\nvars {} are negative, vars {} have no constraints, "
              "vars {} is nolimit_extra\nvars {} are phase 1 slack vars, and {} are extra vars\n"
              "vars {} are bases".format(LP_matrix, neg_constraint_vars, no_constraint_vars, nolimit_extra,
                                         phase1_slack_vars, extra_vars, bases))
    return LP_matrix, neg_constraint_vars, no_constraint_vars, nolimit_extra, phase1_slack_vars, bases
