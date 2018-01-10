Tester: Jinchegn YU, 3150101155
## Two-dimension cases
- case 1:
This is a very normal case that yields an optimal solution without degeneration
$$
\min{x_1+x_2}\\
\begin{align}
2x_1 - x_2 & \geqslant -2 \\
3x_1 - x_2 &\geqslant 0 \\
x_1 + x_2 &\geqslant 3 \\
2x_2 + x_2 &\geqslant -5 \\
\end{align}
$$
The optimal solution is $[0.75,2.25]$ with the optimal variable $3$.
- case 2:
This is the case that yields an optimal solution with degeneration.
$$
\min{x_2}\\
\begin{align}
x_1+x_2 &\geqslant -1\\
x_1 &\leqslant 0\\
x_2 &\leqslant 0\\
\end{align}
$$
The optimal solution is $[0, -1]$ with the optimal variable $-1$.
- case 3:
Again a very normal case but the variable constraint implies in the function constraint.
$$
\min{2x_1-x_2}\\
\begin{align}
x_1 - x_2 & \geqslant -1 \\
x_2 &\geqslant 0 \\
x_1 + x_2 &\geqslant 1 \\
\end{align}
$$
The solution is $[0, 1]$ with the optimal variable $-1$
- case 4:
A special case without any feasible solution and the objected function is always zero.
$$
\min{0}\\
\begin{align}
x_1 + x_2 & \leqslant 1 \\
2x_1 + x_2 &\geqslant 1 \\
2x_1 - x_2 &\leqslant 0 \\
x_2 & \leqslant 0
\end{align}
$$
There is no solution for this problem.
- case 5:
A special case that the feasible area is a signal point.
$$
\min{x_1+x_2}\\
\begin{align}
x_1  & = 0 \\
x_2 & = 0 \\
\end{align}
$$
The solution is $[0,0]$ with the optimal variable $0$.
- case 6:
A special case that the linear programming has no functional constraints but has variable constraints.
$$
\min{x_1+x_2}\\
\begin{align}
x_1 & \geqslant 0\\
x_2 & \geqslant 0
\end{align}
$$
The solution is $[0,0]$ with optimal variable $0$.
## Multi-dimension case
I choice the multi-dimension special case with degeneration proposed by Bland.
$$
\min{-\frac{3}{4}x_4+20x_5-\frac{1}{2}x_6+6_x7}\\
\begin{align}
x_1 + \frac{1}{4}x_4 - 8x_5 - x_6 + 9x_7 &= 0 \\
x_2 + \frac{1}{2} - 12x_5 -\frac{1}{2}x_6+3x_7 &=0\\
x_3 - x_6 &= 0\\
x_j & \geqslant 0, j=1,\cdots ,7
\end{align}
$$
The solution is $[0.75, 0, 0, 1, 0, 1, 0]$ with optimal variable $-1.25$
## Large scale cases
I generate two large scale cases with scale $50\times50$ and $200\times500$ as the test case 8 and 9. The former one has unbounded solution and the latter one has one optimal solution.

## Test Method
- To proof the solution is right I right a simply c++ program to convert the input data of our solver to matlab format so that we can get the correct result of the problem of matlab to compare with ours. Please refer to the `data2matlab` for more details.
- To test the program, we can use I/O redirection to input instead of copying and paste. For instance:
    ```bash
    cat data_1.txt | python3 simplex.py
    ```
    Then we can compare the output very easily.
    Of course, we can code a more complex script to test every data and compare the result automatically. But it's beyond our duty.