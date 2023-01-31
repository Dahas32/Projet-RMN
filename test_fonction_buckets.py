""""ce programme contient les tests des fonctions contenus dans le fichier "fonctions_sur_les_buckets.py""" ""

from fctn_sur_les_buckets import determination_des_buckets


# test determination_des_buckets


def test_determination_buckets_1D_1():
    liste_test1 = [[[(i, 0) for i in range(10)]]]
    taille_bucket_ppm = 1
    assert determination_des_buckets(liste_test1, taille_bucket_ppm) == [
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
    ]
    taille_bucket_ppm = 2
    assert determination_des_buckets(liste_test1, taille_bucket_ppm) == [
        [(0, 2), (2, 4), (4, 6), (6, 8)]
    ]


def test_determination_buckets_1D_2():
    liste_test2 = [[[(i, 0) for i in range(10)]]]
    taille_bucket_ppm = 2
    assert determination_des_buckets(liste_test2, taille_bucket_ppm) == [
        [(0, 2), (2, 4), (4, 6), (6, 8)]
    ]


def test_determination_buckets_1D_3():
    liste_test3 = [[[(i * 0.5, 0) for i in range(10)]]]
    taille_bucket_ppm = 0.5
    assert determination_des_buckets(liste_test3, taille_bucket_ppm) == [
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
    ]


def test_determination_buckets_1D_4():
    liste_test3 = [[[(i * 0.5, 0) for i in range(0,10,1)]]]
    liste_test3_1 = [[[(i * 0.5, 0) for i in range(10,0,-1)]]]
    taille_bucket_ppm = 0.5

    assert determination_des_buckets(liste_test3, taille_bucket_ppm) == [
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
    ]
    assert determination_des_buckets(liste_test3_1, taille_bucket_ppm) == [
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
    ]


def test_determination_buckets_1D_5():
    liste_test1 = [[[(i, 0) for i in range(-5,17,1)]]]
    liste_test2 = [[[(i, 0) for i in range(17,-5,-1)]]]
    taille_bucket_ppm = 3

    assert determination_des_buckets(liste_test1, taille_bucket_ppm) == determination_des_buckets(liste_test2, taille_bucket_ppm)


def test_determination_buckets_2D_1():
    liste_test4 = [
        [[(i * 0.5, 0) for i in range(10)], [(i * 0.5, 0) for i in range(10)]]
    ]
    taille_bucket_ppm = 0.5
    assert determination_des_buckets(liste_test4, taille_bucket_ppm) == [
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)],
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)],
    ]

