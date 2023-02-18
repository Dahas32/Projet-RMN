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
            print("veuiler donner un nombre")
            bucket_size = input("donner la taille des buckets(ppm) voulue : ")
            correct = False
    bucket_list = rmn_bucket.determination_des_buckets(data[1], bucket_size)
    # bucket_list_filtre = rmn_bucket.noise_threshold(data[1], bucket_list, 2000)
    # bucket_int_list = rmn_bucket.calcul_des_integrales(bucket_list_filtre, data[1])
    bucket_int_list = rmn_bucket.calcul_des_integrales(bucket_list, data[1])
    nb_buckets = [len(bucket_int_list[i]) for i in range(len(bucket_int_list))]

    integral_buckets_list, nb_max_buckets = rmn_bucket.sort_bucket(
        bucket_int_list, nb_buckets
    )
    
    # to change 
    delta_t_list = [0.2, 0.05, 0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5] 

    directory_export = "./export"
    if os.path.exists(directory_export):
        shutil.rmtree(directory_export)
    os.makedirs(directory_export + "/img/")
    t1 = time.process_time()
    resfit_list = []
    for b in range(nb_max_buckets):
        plt.plot(
            [i * delta_t_list[i] for i in range(len(integral_buckets_list[b]))],
            integral_buckets_list[b],
            "xb",
        )
        resfit = rmn.fitting(integral_buckets_list[b], delta_t_list)
        resfit_list.append([resfit])
        rmn.afficher_coube_model(len(integral_buckets_list[b]), delta_t_list, *resfit[0])
        image = "./export/img/bucket_{}.png".format(b)
        plt.savefig(image)
        plt.close()
    rmn.export_xlsx(data[1], bucket_list, nb_max_buckets, path, resfit_list)
    t2 = time.process_time()
    print("duree :", t2 - t1)
    quit = input("voulez vous quitter y/n")
    while quit == "n":
        quit = input("voulez vous quitter y/n")


if __name__ == "__main__":
    main()
