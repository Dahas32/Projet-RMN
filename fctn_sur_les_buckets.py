"""this file contains or will contain all the operations done on the buckets objects, such as their determination,
the suppression of the noise and the computing of the integrals. All the fonctions of this file depend on the result
of rmn.py, so we get the list [n_point,[[data_dim1,data_dim2,...]]] where data_dim1 is a list of couplethe couple is two float like this (ppm,amplitude)"""

from math import floor


def determination_des_buckets(data_list, taille_buckets_ppm):
    """data_list=[[data_dim1,data_dim2,...]]
    this is the function that determine the buckets. it takes in argument data_list wich is the second element of the list return by
    rmn.py : data_list=[[data_dim1,data_dim2,...]] and taille_bucket is a float given by the user.
    this function return a list whith the shape bucket_list = [buckets_dim1,bucket_dim2] where bucket_dim1
    is a list of tuple (debut,fin) where debut and fin are two int indicating the index of the inf and sup boundaries of the bucket
    """

    number_of_dimension = len(data_list)
    buckets_list = []

    for n in range(number_of_dimension):
        buckets_list.append([])
        current_dimension = n
        index_dernier_ppm = len(data_list[current_dimension]) - 1
        longueur_ppm = len(data_list[current_dimension])
        valeur_premier_ppm = data_list[current_dimension][0][0]
        valeur_dernier_ppm = data_list[current_dimension][-1][0]
        if abs(valeur_premier_ppm) <= abs(valeur_dernier_ppm):
            etendu_ppm = abs(valeur_dernier_ppm - valeur_premier_ppm)
        else:
            etendu_ppm = abs(valeur_premier_ppm - valeur_dernier_ppm)

        taille_buckets_longueur = floor((taille_buckets_ppm) * (longueur_ppm / etendu_ppm))
        index_current_ppm = 0
        if taille_buckets_longueur < 1:
            taille_buckets_longueur = 1
        if (index_current_ppm + 1) * taille_buckets_longueur >= index_dernier_ppm:
            taille_buckets_longueur = index_dernier_ppm
        while (index_current_ppm + 1) * taille_buckets_longueur <= index_dernier_ppm:
            debut_bucket = index_current_ppm * taille_buckets_longueur
            fin_bucket = (index_current_ppm + 1) * taille_buckets_longueur
            buckets_list[current_dimension] += [(debut_bucket, fin_bucket)]
            index_current_ppm += 1

    return buckets_list


def calcul_des_integrales(filtered_bucket_list, data_list):
    """this is the function that compute the buckets integrals. it takes in argument data_list wich is the second element of the list return by
    rmn.py : data_list=[[data_dim1,data_dim2,...]] and filtered_bucket_list wich is the list of the bucket without the noised ones.
    this function return a list whith the shape integral_list = [[integral_bucket1,integral_bucket2,...],[integral_bucket_dim2_1,integral_bucket_dim2_2...],...]
    where integral_bucket1 is a float.
    the index of the integral of a particular bucket is the same as the index of this bucket in _filtered_bucket_list
    """
    number_of_dimension = len(filtered_bucket_list)
    integral_list = []

    for n in range(number_of_dimension):
        current_dimension = n
        integral_list.append([])

        for bucket in filtered_bucket_list[current_dimension]:
            bucket_integral = 0
            number_of_rectangle = bucket[1] - bucket[0]

            for i in range(number_of_rectangle):
                first_point_amplitude = data_list[current_dimension][bucket[0] + i][1]
                second_point_amplitude = data_list[current_dimension][
                    bucket[0] + i + 1
                ][1]
                average_amplitude = (first_point_amplitude + second_point_amplitude) / 2
                rectancle_width = (
                    data_list[current_dimension][bucket[0] + i][0]
                    - data_list[current_dimension][bucket[0] + i + 1][0]
                )
                rectangle_area = average_amplitude * rectancle_width
                bucket_integral += rectangle_area
            integral_list[current_dimension].append(bucket_integral)

    return integral_list


def noise_threshold(data_list, buckets_list, threshold):
    """data_list: [[data_dim1],[data_dim2],...]], buckets_list: [[buckets_dim1],[bucket_dim2],...] , threshold: int
        return buckets_filter_list : [[(first,last),...],[buckets_filter_list_dim2]...]

    this is the function that remove bucket above or below a certain threshold. it takes in entry data_list wich is the second element of the list return by
    rmn.py : [[data_dim1,data_dim2,...]],  buckets_list : [buckets_dim1,bucket_dim2]
    and threshold is a integer given by the user.
    this function return a list of bucket without bucket not required whith the shape buckets_filter_list = [buckets_dim1,bucket_dim2] where bucket_dim1
    is a list of tuple (first,last) where first and last are two int indicating the index of the inf and sup boundaries of the bucket
    """
    number_of_dimension = len(data_list)
    buckets_filter_list = []

    for n in range(number_of_dimension):
        buckets_filter_list.append([])
        current_dimension = n

        for bucket in buckets_list[current_dimension]:
            for i in range(bucket[0], bucket[1], 1):
                noise = False
                valeur_I = data_list[current_dimension][i][1]
                # to change if we want a specific threshold : up threshold and down threshold
                if (valeur_I >= -threshold) and (threshold >= valeur_I):
                    noise = True
                    break
            if noise == False:
                buckets_filter_list[current_dimension].append(bucket)

    return buckets_filter_list


def noise_automate(data_list, buckets_list):
    """data_list: [[data_dim1],[data_dim2],...]], buckets_list: [[buckets_dim1],[bucket_dim2],...]
    return buckets_filter_list : [[(first,last),...],[buckets_filter_list_dim2]...]
    """
    number_of_dimension = len(data_list)
    buckets_filter_list = []

    for n in range(number_of_dimension):
        buckets_filter_list.append([])
        current_dimension = n
        average_buckets = []
        average_of_average_buckets = 0
        # average abs of each bucket
        for bucket in buckets_list[current_dimension]:
            average_bucket = 0
            for i in range(bucket[0], bucket[1], 1):
                average_bucket += data_list[current_dimension][i][1]
            average_bucket = abs(int((average_bucket // (bucket[1] - bucket[0]))))
            average_buckets.append(average_bucket)
            average_of_average_buckets += average_bucket

        length_average_buckets = len(average_buckets)
        average_of_average_buckets = int(
            average_of_average_buckets // length_average_buckets
        )

        variance = 0
        for i in range(length_average_buckets):
            variance += (
                data_list[current_dimension][i][1] - average_of_average_buckets
            ) ** 2
        variance = int(variance // length_average_buckets)
        standard_deviation = int(variance ** (1 / 2))

        for i in range(1, length_average_buckets - 1):
            if average_buckets[i] != 0:
                if (
                    average_buckets[i - 1] / average_buckets[i] < 2
                    and average_buckets[i + 1] / average_buckets[i] < 2
                    and average_buckets[i]
                    > average_of_average_buckets - standard_deviation
                ):
                    buckets_filter_list[current_dimension].append(
                        buckets_list[current_dimension][i]
                    )

    return buckets_filter_list
