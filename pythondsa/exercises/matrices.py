class Matrix:
    """A two-dimensional array of numbers that supports addition and multiplication."""

    def __init__(self, num_rows, num_cols, rows):
        self._num_rows = num_rows
        self._num_cols = num_cols


if __name__ == '__main__':
    print('------------------------------------------')
    print('Testing addition of two matrices in P-5.33')
    m1 = Matrix()
    m2 = Matrix()
    print(m1 + m2)
