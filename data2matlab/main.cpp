#include <fstream>
#include <iostream>
#include <vector>
using namespace std;

int main(int argc, char *argv[]) {
  if (argc < 3) {
    cerr << "No enough arguments" << endl;
    return EXIT_FAILURE;
  }
  ifstream in(argv[1], std::ios::in);
  if (!in.is_open()) {
    cerr << "Cannot open file " << argv[1] << endl;
    return EXIT_FAILURE;
  }

  size_t n, m;
  in >> n >> m;
  vector<vector<double>> matrix(m);
  vector<double> c(n);
  vector<double> b(m);
  vector<int> funConstraint(m);
  vector<int> varConstraint(n);
  for (size_t i = 0u; i != n; ++i) {
    in >> c[i];
  }
  for (size_t i = 0u; i != m; ++i) {
    matrix[i].resize(n);
    for (size_t j = 0u; j != n; ++j) {
      in >> matrix[i][j];
    }
    in >> b[i];
    in >> funConstraint[i];
  }
  for (size_t i = 0u; i != n; ++i) {
    in >> varConstraint[i];
  }
  in.close();
  ofstream out(argv[2], std::ios::out);
  if (!out.is_open()) {
    cerr << "Cannot open file " << argv[2] << endl;
    return EXIT_FAILURE;
  }
  out << "f = [";
  for (size_t i = 0u; i != c.size(); ++i) {
    if (i != 0u)
      out << ", ";
    out << c[i];
  }
  out << "]" << endl;
  out << "A = [";
  size_t count = 0u;
  for (size_t i = 0u; i != matrix.size(); ++i) {
    if (funConstraint[i] == 0)
      continue;
    if (count++ != 0u)
      out << "; ";
    for (size_t j = 0u; j != matrix[i].size(); ++j) {
      if (j != 0u)
        out << ", ";
      out << -funConstraint[i] * matrix[i][j];
    }
  }
  out << "]" << endl;
  out << "b = [";
  count = 0u;
  for (size_t i = 0u; i != b.size(); ++i) {
    if (funConstraint[i] == 0)
      continue;
    if (count++ != 0u)
      out << ", ";
    out << -funConstraint[i] * b[i];
  }
  out << "]" << endl;
  out << "Aeq = [";
  count = 0u;
  for (size_t i = 0u; i != matrix.size(); ++i) {
    if (funConstraint[i] != 0)
      continue;
    if (count++ != 0u)
      out << "; ";
    for (size_t j = 0u; j != matrix[i].size(); ++j) {
      if (j != 0u)
        out << ", ";
      out << matrix[i][j];
    }
  }
  out << "]" << endl;
  out << "beq = [";
  count = 0u;
  for (size_t i = 0u; i != b.size(); ++i) {
    if (funConstraint[i] != 0)
      continue;
    if (count++ != 0u)
      out << ", ";
    out << b[i];
  }
  out << "]" << endl;
  out << "lb = [";
  for (size_t i = 0u; i != varConstraint.size(); ++i) {
    if (count != 0u)
      out << ", ";
    if (varConstraint[i] == 1)
      out << 0;
    else
      out << "-Inf";
  }
  out << "]" << endl;
  out << "ub = [";
  for (size_t i = 0u; i != varConstraint.size(); ++i) {
    if (count != 0u)
      out << ", ";
    if (varConstraint[i] == -1)
      out << 0;
    else
      out << "+Inf";
  }
  out << "]" << endl;
  out << "[x, val, flag] = linprog(f, A, b, Aeq, beq, lb, "
         "ub)"
      << endl;
  return EXIT_SUCCESS;
}
