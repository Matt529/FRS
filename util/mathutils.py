from typing import Sequence, Union
import numpy as np

MatrixLike = Union[np.matrix, Sequence]


def is_row_vector(v: np.matrix) -> bool:
    r, c = v.shape
    return r == 1 and c >= 1


def is_column_vector(v: np.matrix) -> bool:
    r, c = v.shape
    return r >= 1 and c == 1


def is_vector_form(a: np.matrix) -> bool:
    return is_column_vector(a) or is_row_vector(a)


def is_matrix_form(a: np.matrix) -> bool:
    return not is_vector_form(a)


def create_matrix(entries: Sequence[Sequence[...]]) -> np.matrix:
    if isinstance(entries, np.matrix):
        return entries

    return np.mat(entries)


def as_column_vector(v: np.matrix) -> np.matrix:
    return v.T if is_row_vector(v) else v


def as_row_vector(v: np.matrix) -> np.matrix:
    return v.T if is_column_vector(v) else v


def create_2d_vector(entries: Sequence, make_column_vector: bool=True, force_column_vector: bool=False) -> np.matrix:
    """
    Given a sequence, creates a row or column vector. If a matrix is provided then the matrix is unmodified unless it is
    in the form of a row or column vector and the flag to force the vector to a column vector form is set.

    :param entries: Sequence of elements to convert to 2d vector
    :param make_column_vector: Whether or not the result should be a column vector (nx1 instead of 1xn)
    :param force_column_vector: Forces the values to a column vector iff the provided entries is already a matrix in
        vector form.
    :return: Row or column vector
    """
    if isinstance(entries, np.matrix):
        if force_column_vector and is_vector_form(entries):
            return as_column_vector(entries) if make_column_vector else entries
        else:
            return entries

    return as_column_vector(np.matrix(entries)) if make_column_vector else np.matrix(entries)


def solve_linear_least_squares(A: MatrixLike, z: MatrixLike) -> np.matrix:
    """
    Solves an over-determined linear system of equations by Linear Least Squares (With UL Decomposition via Cholesky
    Decomposition), given the coefficient matrix, [A], and the result vector, [z].

    Namely, it finds an approximate solution to the system [A][x] = [z] for the vector [x] by the method of Linear Least
    Squares. It is not particularly necessary, but this method is primarily useful for over-determined systems where if
    [A] is an mxn matrix, m > n (more equations than variables).


    :param A: Coefficient matrix
    :param z: Result vector
    :return: Approximate solution for the vector, x
    """
    A = create_matrix(A)
    z = create_2d_vector(z, force_column_vector=True)

    # (Eq. 1): [A][x] = [y]
    # (Eq. 2): [A]^T[A][x] = [A]^T[y], from (Eq. 1)
    #          [P][x] = [S], [P] = [A]^T[A] and [S] = [A]^T[y]
    P = A.T * A
    S = A.T * z

    # (Eq. 3): [L][L]^T[x] = [S], where [L] is the lower triangular matrix from Cholesky Decomposition of [P]
    L = np.linalg.cholesky(P)

    # (Eq. 4): [L][z] = [S], [z] = [L]^T[x]
    #          Using Forward Substitution to solve for vector [y]
    z = np.zeros(S.size)
    for m, s_entry in enumerate(S.flatten()):
        """
        To understand this and backwards substitution, consider the followign equation:
        | a 0 0 |   | x |   | alpha |
        | b c 0 | x | y | = | beta  |
        | d e f |   | z |   | gamma |
        """
        z[m] = s_entry               # If its the first row, definitely is the entry in s

        if m != 0:
            for i in range(m):
                z[m] -= z[i] * L[m, i]

        z[m] /= L[m, m]             # Divide by matrix entry

    # [z] is known, [z] = [L]^T[x], [L]^T is an upper triangular matrix,
    # backwards substitute to solve for [x].
    L_transpose = L.T
    x = np.zeros(S.size)
    for m in range(S.size - 1, -1, -1):
        x[m] = z[m]
        if m != 0:
            for i in range(S.size - 1, m, -1):
                x[m] -= x[i] * L_transpose[m, i]
        x[m] /= L_transpose[m, m]

    return x
