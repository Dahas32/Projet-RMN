""" This program is made to read RMN treated output (after the fourier and modifying
    the phase) to find T1 (caracteristic time) and d (diffusion something)
    this file is made to take the I/O and to call each script."""

import rmn
import fctn_sur_les_buckets as rmn_bucket
import matplotlib.pyplot as plt
import time
import os
import shutil


def main():
    """main function"""
    path = input("file path")
    data = rmn.read_rmn(path)
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
    nb_bucket = len(bucket_int_list[0])
    nb_dim = data[2]
    integral_buckets_list = [
        [bucket_int_list[i][a] for i in range(nb_dim)] for a in range(nb_bucket)
    ]

    integral_buckets_f_list = [
        [j for j in integral_buckets_list[i] if j != 0.0] for i in range(nb_bucket)
    ]
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

    directory_export = "./export"
    if os.path.exists(directory_export):
        shutil.rmtree(directory_export)
    os.makedirs(directory_export + "/img/")
    t1 = time.process_time()
    resfit_list = []
    for b in range(nb_bucket):
        plt.plot(
            [i * delta_t for i in range(len(integral_buckets_f_list[b]))],
            integral_buckets_f_list[b],
            "xb",
        )
        resfit = rmn.fitting(integral_buckets_f_list[b], delta_t)
        resfit_list.append([resfit])
        rmn.afficher_coube_model(len(integral_buckets_f_list[b]), delta_t, *resfit[0])
        image = "./export/img/bucket_{}.png".format(b)
        plt.savefig(image)
        plt.close()
    rmn.export_xlsx(data[1], bucket_list, path, resfit_list)
    t2 = time.process_time()
    print("duree :", t2 - t1)
    quit = input("voulez vous quitter y/n")
    while quit == "n":
        quit = input("voulez vous quitter y/n")


if __name__ == "__main__":
    main()
