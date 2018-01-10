# Report from Yao Zou

## Implementation of primal simplex method

An LP problem is represented by a 2-dimensional `numpy.ndarray` usually called `LP_matrix`. The matrix consists from $\mathbf{c}$, $\mathbf{A}$ and $\mathbf{b}$. It is represented as
$$
LP\_matrix = 
\begin{bmatrix}
\mathbf{c}^T & 0\\
\mathbf{A} & \mathbf{b}
\end{bmatrix}
$$

I implemented two major functions, the first is `standardize(LP_matrix, var_constraints, func_constraints, verbose=False) -> LP_matrix, neg_constraint_vars, no_constraint_vars, nolimit_extra, phase1_slack_vars, bases`, which is used to convert the problem taken from user input to canonical form. The second is `solve_canonical_LP(LP_matrix, bases, verbose=False)->solution, solution_value`, which is use to solve the canonical LP problem returned by `standardize()`.

### Details about `standardize()`

The `standardize` function has to ensure that:

- all the variables are converted to non-negative
- all the functional constraints are converted to $=$
- the initial basic feasible solution is easily readable from the simplex tableau

How to complete the three tasks? Let's take care of the variables first. For variables that are already non-negative, no further action is needed. For non-positive variables, we can take their negation and in this way they can be converted to non-negative variables. For variables with no constraint, we need a trick.

For example, if $x_j$ has no constraint, we can introduce two additional variables, $x_j^+$ and $x_J^-$, which are both non-negative. Then, denote $x_j$ as $x_j^+ - x_j^-$. In this way, we replace a variable with no constraint with two non-positive variables. 

If two or more variables have no constraints, we do not need to introduce an additional variable for each of them. Instead, we just need to introduce only one additional variable. Suppose we have two variables, $x_i$ and $x_j$, with no constraints. We can denote them as $x_i = x_i^- + x'$ and $x_j = x_j^+ - x'$, with $x_i^+ \ge 0, x_j^+\ge 0$ and $x' \ge 0$. Note that they share a common $x'$.

The variable problem is thus handled in the method discussed above. This task is handled in the function `std_var_constraints()`. 

For the functional constraints, we can address them with standard methods. This task is mainly performed in the function `std_func_constraints()`.

- First of all, for all constraints with a negative $b_i$, flip its sign. For example, if $\sum_{j = 1}^{n}a_{ij}x_j \le b_i$ and $b_i<0$, we should convert it to $\sum_{j = 1}^{n}-a_{ij}x_j \ge -b_i$. In this way, the right hand side of the simplex tableau will be non-negative, and the initial basic solution we read directly from the tableau will be *feasible*. Otherwise, we will have one or more basic variables with value $\le 0$ and they break the non-negative constraints.
- For $\le$ constraint, add a slack variable.
- For $=$ constraint, add an artificial variable. For example, if $\sum_{j = 1}^{n}a_{ij}x_j = b_i$, we should add an artificial variable $\overline{x}_i \ge$ and convert the constraint to $\sum_{j = 1}^{n}a_{ij}x_j + \overline{x}_i= b_i$.
- For $\ge$ constraints, we can add a surplus variable and an artificial variable. For example, if $\sum_{j = 1}^{n}a_{ij}x_j \ge b_i$, we should add a surplus variable $x_i' \ge 0$  and an artificial variable $\overline{x}_i \ge 0$ and convert the constraint to $\sum_{j = 1}^{n}a_{ij}x_j - x_i' + \overline{x}_i= b_i$

`standardize()` just calls the function `std_var_constraints()` and `std_func_constraints()` to standardize the LP. The logic to solve the standardized LP is mainly implemented in the function `solve_LP()`.

### Solving LP

If we have added at least one artificial variable we should enter phase 1 to find an initial basic feasible solution. Otherwise, we have only added slack variables, which means that there are only $\le$ constraints in the LP and that we can read the initial solution directly from the simplex tableau. Therefore, we can enter phase 2 directly. The function `solve_canonical_LP()` is called to solve phase 1 and phase 2 LP. 

`solve_canonical_LP()` just runs the simplex method. In every iteration, it finds the first variable with negative coefficients as the entering bases variable and finds the leaving bases variable according to their bounds. Then, it performs the necessary transformation to the simplex tableau and enters the next iteration. The details from simplex method can be found on any standard operational research textbook so it is not repeated here.

The advantage of representing the whole simplex tableau with a `LP_matrix` instead of manipulating $\mathbf{c}$, $\mathbf{A}$ and $\mathbf{b}$ separately is that we can perform the transformation to the entire matrix, with a single transformation matrix. As is known, after we find the entering and leaving bases variables, we should transform the simplex tableau to desired form with elementary row operation, so we can set up a matrix (which is called `modify` in my program) and let `LP_matrix = np.dot(modify, LP_matrix)` to update the simplex tableau as a whole.




