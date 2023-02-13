""" This program is made to read RMN treated output (after the fourier and modifying
    the phase) to find T1 (caracteristic time) and d (diffusion something)
    this file is made to take the I/O and to call each script."""

import rmn
import fctn_sur_les_buckets as rmn_bucket
import matplotlib.pyplot as plt


def main():
    """main function"""
    data = rmn.read_rmn(input("file path"))
    rmn.afficher(data, 5)
    plt.show()
    bucket_size = input("donner la taille des buckets(ppm) voulue : ")
    correct = False
    while not correct:
        correct = True
        try:
            bucket_size = float(bucket_size)
        except ValueError:
            print("veuilelr donner un nombre")
            bucket_size = input("donner la taille des buckets(ppm) voulue : ")
            correct = False
    bucket_list = rmn_bucket.determination_des_buckets(data[1], bucket_size)
    bucket_int_list = rmn_bucket.calcul_des_integrales(bucket_list, data[1])
    alpha = int(input("a : "))
    integral_bucket_1 = [bucket_int_list[i][alpha] for i in range(data[2])]
    integral_bucket_1_f = []
    for i in integral_bucket_1:
        if i != 0.0:
            integral_bucket_1_f.append(i)
    delta_t = input("temps entre les spèctre : ")
    correct = False
    while not correct:
        correct = True
        try:
            delta_t = float(delta_t)
        except ValueError:
            print("veuilelr donner un nombre")
            delta_t = input("donner la taille des buckets(ppm) voulue : ")
            correct = False
    plt.plot(
        [i * delta_t for i in range(len(integral_bucket_1_f))],
        integral_bucket_1_f,
        "xb",
    )
    resfit = rmn.fitting(integral_bucket_1_f, delta_t)
    rmn.afficher_coube_model(len(integral_bucket_1_f), delta_t, *resfit[0])
    print(resfit)
    plt.show()


if __name__ == "__main__":
    main()
