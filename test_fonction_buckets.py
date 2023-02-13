""""ce programme contient les tests des fonctions contenus dans le fichier "fonctions_sur_les_buckets.py""" ""

from fctn_sur_les_buckets import (
    determination_des_buckets,
    calcul_des_integrales,
    noise_threshold,
    noise_automate,
)


def test_determination_buckets_1D_integer():
    liste_test1 = [[(i, 0) for i in range(10)]]
    taille_bucket_ppm = 1
    assert determination_des_buckets(liste_test1, taille_bucket_ppm) == [
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
    ]
    taille_bucket_ppm = 2
    assert determination_des_buckets(liste_test1, taille_bucket_ppm) == [
        [(0, 2), (2, 4), (4, 6), (6, 8)]
    ]


def test_determination_buckets_1D_float():
    liste_test1 = [[(i * 0.5, 0) for i in range(10)]]
    liste_test2 = [[(i * 0.5, 0) for i in range(10, 0, -1)]]
    taille_bucket_ppm = 0.5
    assert determination_des_buckets(liste_test1, taille_bucket_ppm) == [
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
    ]
    assert determination_des_buckets(liste_test2, taille_bucket_ppm) == [
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
    ]


def test_determination_buckets_1D_list_reversed():
    liste_test1 = [[(i, 0) for i in range(-5, 17, 1)]]
    liste_test2 = [[(i, 0) for i in range(17, -5, -1)]]
    taille_bucket_ppm = 3

    assert determination_des_buckets(
        liste_test1, taille_bucket_ppm
    ) == determination_des_buckets(liste_test2, taille_bucket_ppm)


def test_determination_buckets_2D_integer():
    liste_test1 = [[(i, 0) for i in range(10)], [(i, 0) for i in range(10)]]
    taille_bucket_ppm = 1
    assert determination_des_buckets(liste_test1, taille_bucket_ppm) == [
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)],
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)],
    ]
    taille_bucket_ppm = 2
    assert determination_des_buckets(liste_test1, taille_bucket_ppm) == [
        [(0, 2), (2, 4), (4, 6), (6, 8)],
        [(0, 2), (2, 4), (4, 6), (6, 8)],
    ]


def test_determination_buckets_2D_float():
    liste_test1 = [[(i * 0.5, 0) for i in range(10)], [(i * 0.5, 0) for i in range(10)]]
    taille_bucket_ppm = 0.5
    assert determination_des_buckets(liste_test1, taille_bucket_ppm) == [
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)],
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)],
    ]


def test_determination_buckets_2D_list_reversed():
    liste_test1 = [
        [(i, 0) for i in range(-5, 17, 1)],
        [(i, 0) for i in range(17, -5, -1)],
    ]
    liste_test2 = [
        [(i, 0) for i in range(17, -5, -1)],
        [(i, 0) for i in range(-5, 17, 1)],
    ]
    taille_bucket_ppm = 3

    assert determination_des_buckets(
        liste_test1, taille_bucket_ppm
    ) == determination_des_buckets(liste_test2, taille_bucket_ppm)


def test_noise_threshold_1D():
    liste_test1 = [[(x, (x**2) - 30) for x in range(-10, 12, 1)]]
    taille_bucket_ppm = 2
    det = determination_des_buckets(liste_test1, taille_bucket_ppm)
    seuil = 30

    assert noise_threshold(liste_test1, det, seuil) == [[(0, 3), (18, 21)]]


def test_noise_threshold_2D():
    liste_test1 = [[(i * 0.5, i * 0.5) for i in range(10)], [(i, i) for i in range(10)]]
    taille_bucket_ppm = 1
    det = determination_des_buckets(liste_test1, taille_bucket_ppm)
    assert det == [
        [(0, 2), (2, 4), (4, 6), (6, 8)],
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)],
    ]

    seuil = 2
    assert noise_threshold(liste_test1, det, seuil) == [
        [(6, 8)],
        [(3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)],
    ]
