""" This program is made to read RMN treated output (after the fourier and modifying
    the phase) to find T1 (caracteristic time) and d (diffusion something)
    this file is made to take the I/O and to call each script."""

import rmn
import matplotlib.pyplot as plt


def main():
    """main function"""
    data = rmn.read_rmn(input("file path"))
    for i in range(data[-1]):
        rmn.afficher(data, i)
    plt.show()


if __name__ == "__main__":
    main()

