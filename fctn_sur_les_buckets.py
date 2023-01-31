"""this file contains or will contain all the operations done on the buckets objects, such as their determination,
the suppression of the noise and the computing of the integrals. All the fonctions of this file depend on the result
of rmn.py, so we get the list [n_point,[[data_dim1,data_dim2,...]]] where data_dim1 is a list of couplethe couple is two float like this (ppm,amplitude)"""

from math import floor

# this is the function that determine the buckets. it takes in entry data_list wich is the second element of the list return by
# rmn.py : [[data_dim1,data_dim2,...]] and taille_bucket is a float given by the user.
# this function return a list whith the shape bucket_list = [buckets_dim1,bucket_dim2] where bucket_dim1
# is a list of tuple (debut,fin) wher debut and fin are two int indicating the index of the inf and sup boundaries of the bucket


def determination_des_buckets(data_list, taille_buckets_ppm):
    number_of_dimension = len(data_list[0])
    buckets_list = []

    for i in range(number_of_dimension):
        buckets_list += [[]]
        current_dimension = i

        index_dernier_ppm = len(data_list[0][current_dimension]) - 1
        valeur_premier_ppm = data_list[0][current_dimension][0][0]
        valeur_dernier_ppm = data_list[0][current_dimension][-1][0]
        if abs(valeur_premier_ppm)<=abs(valeur_dernier_ppm):
            max_valeur_ppm = abs(valeur_dernier_ppm)
        else:
            max_valeur_ppm = abs(valeur_premier_ppm-1)
        taille_buckets_index = floor(
            (taille_buckets_ppm)*(index_dernier_ppm/max_valeur_ppm)
        )
        index_current_ppm = 0

        while (index_current_ppm + 1) * taille_buckets_index <= index_dernier_ppm:
            debut_bucket = index_current_ppm * taille_buckets_index
            fin_bucket = (index_current_ppm + 1) * taille_buckets_index
            buckets_list[current_dimension] += [(debut_bucket, fin_bucket)]
            index_current_ppm += 1

    return buckets_list

# this is the function that remove bucket above or below a certain threshold. it takes in entry data_list wich is the second element of the list return by
# rmn.py : [[data_dim1,data_dim2,...]],  buckets_list : [buckets_dim1,bucket_dim2]   
# and threshold is a integer given by the user.
# this function return a list of bucket without bucket not required whith the shape buckets_filter_list = [buckets_dim1,bucket_dim2] where bucket_dim1
# is a list of tuple (first,last) where first and last are two int indicating the index of the inf and sup boundaries of the bucket


def noise_threshold(data_list, buckets_list, threshold):
    number_of_dimension = len(data_list[0])
    buckets_filter_list = []
    
    for i in range(number_of_dimension):
        buckets_filter_list += [[]]
        current_dimension = i

        for bucket in buckets_list[current_dimension]:
            
            for y in range (bucket[0],bucket[1],1):
                noise = False
                valeur_I = data_list[0][current_dimension][y][1]
                # to change if we want a specific threshold : up threshold and down threshold
                if (valeur_I >= -threshold) and (threshold >= valeur_I):
                    noise = True
                    break
            if noise == False: buckets_filter_list[current_dimension] += [bucket]
      
    return buckets_filter_list