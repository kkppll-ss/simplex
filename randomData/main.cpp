#include <algorithm>
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
  vector<size_t> varIndex(n);
  for (size_t i = 0; i != varIndex.size(); ++i)
    varIndex[i] = i;
  vector<size_t> funIndex(m);
  for (size_t i = 0; i != funIndex.size(); ++i)
    funIndex[i] = i;
  random_shuffle(varIndex.begin(), varIndex.end());
  random_shuffle(funIndex.begin(), funIndex.end());

  ofstream out(argv[2], std::ios::out);
  if (!out.is_open()) {
    cerr << "Cannot open file " << argv[2] << endl;
    return EXIT_FAILURE;
  }

  out << n << " " << m << endl;
  for (size_t i = 0u; i != n; ++i) {
    if (i != 0u)
      out << " ";
    out << c[varIndex[i]];
  }
  out << endl;
  for (size_t i = 0u; i != m; ++i) {
    for (size_t j = 0u; j != n; ++j) {
      if (j != 0u)
        out << " ";
      out << matrix[funIndex[i]][varIndex[j]];
    }
    out << " ";
    out << b[funIndex[i]];
    out << " ";
    out << funConstraint[funIndex[i]];
    out << endl;
  }
  for (size_t i = 0u; i != n; ++i) {
    if (i != 0u)
      out << " ";
    out << varConstraint[varIndex[i]];
  }
  out << endl;
  return EXIT_SUCCESS;
}
