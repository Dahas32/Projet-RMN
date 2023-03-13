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

        taille_buckets_longueur = floor(
            (taille_buckets_ppm) * (longueur_ppm / etendu_ppm)
        )
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
    
    this is a function that remove noise
    make in each dim average abs intensity of each bucket and from average of average make a standard deviation
    conditon : if average abs intensity of bucket is lower of a certain factor
               if average abs intensity of bucket is lower to average of average - standard deviation
    is a noise

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


def noise_spectre(data_list, buckets_list):
    """data_list: [[data_dim1],[data_dim2],...]], buckets_list: [[buckets_dim1],[bucket_dim2],...]
    return buckets_filter_list : [[(first,last),...],[buckets_filter_list_dim2]...]

    this is a function that remove noise
    compare one bucket of each dim the gap of intensity ex: dim1_bucket_1 - dim2_bucket_1
    if not much gap about sum of each dim in one bucket is noise
    the "not much gap" its if gap under average
    """

    number_of_dimension = len(data_list)
    bucket_intensity_list = [[] for i in range(number_of_dimension)]
    bucket_gaps_list = [[] for i in range(len(buckets_list[0]))]
    buckets_filter_list = []

    for n in range(number_of_dimension):
        buckets_filter_list.append([])
        current_dimension = n

        if len(bucket_intensity_list[n]) == 0:
            for b in range(len(buckets_list[current_dimension])):
                sum_intesity_bucket = 0
                for i in range(
                    buckets_list[current_dimension][b][0],
                    buckets_list[current_dimension][b][1],
                    1,
                ):
                    sum_intesity_bucket += data_list[current_dimension][i][1]
                bucket_intensity_list[n].append(int(sum_intesity_bucket))

        for s in range(n + 1, number_of_dimension):
            for b in range(len(buckets_list[s])):
                if len(bucket_intensity_list[s]) <= b:
                    sum_intesity_bucket = 0
                    for i in range(buckets_list[s][b][0], buckets_list[s][b][1], 1):
                        sum_intesity_bucket += data_list[s][i][1]
                    bucket_intensity_list[s].append(int(sum_intesity_bucket))

                if abs(bucket_intensity_list[n][b]) >= bucket_intensity_list[s][b]:
                    bucket_diff = abs(
                        bucket_intensity_list[n][b] - bucket_intensity_list[s][b]
                    )
                else:
                    bucket_diff = abs(
                        bucket_intensity_list[s][b] - bucket_intensity_list[n][b]
                    )
                bucket_gaps_list[b].append(bucket_diff)

    bucket_gap_list = []
    average_gap_bucket = 0
    for bucket in bucket_gaps_list:
        sum_gap_bucket = 0
        for gap in bucket:
            sum_gap_bucket += gap
        average_gap_bucket += sum_gap_bucket
        bucket_gap_list.append(sum_gap_bucket)
    average_gap_bucket = int(average_gap_bucket // len(bucket_gaps_list))

    for i in range(len(bucket_gap_list)):
        if bucket_gap_list[i] < sum_gap_bucket:
            bucket_gap_list[i] = 0

    for n in range(number_of_dimension):
        for i in range(len(bucket_gap_list)):
            if bucket_gap_list[i] != 0:
                buckets_filter_list[n].append(buckets_list[n][i])

    return buckets_filter_list


def sort_bucket(bucket_int_list, nb_buckets):
    """bucket_int_list: [[buckets_dim1],[bucket_dim2],...], nb_buckets: [nb_buckets_dim1,nb_buckets_dim2...] (value in list: int)
    return integral_buckets_list: [integral_buckets_1,integral_buckets_2...] (value in list: int)
    
    this is a function who sort the integral_bucket_list
    take off bucket integral equal 0 and remove bucket list in integral_buckets_list below a certain non-exaustive level for the fit
    """
    nb_max_buckets = max(nb_buckets)
    nb_dim = len(bucket_int_list)
    integral_buckets_list = [[] for i in range(nb_max_buckets)]

    for n in range(nb_dim):
        for b in range(nb_buckets[n]):
            if bucket_int_list[n][b] != 0:
                integral_buckets_list[b].append(bucket_int_list[n][b])

    buckets_delete = 0
    for i in range(nb_max_buckets):
        if len(integral_buckets_list[i - buckets_delete]) < 7:
            integral_buckets_list.pop(i - buckets_delete)
            buckets_delete += 1

    return integral_buckets_list, len(integral_buckets_list)
