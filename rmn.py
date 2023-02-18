"""this is the code of the programm"""

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy import exp
import xlsxwriter


def read_rmn(file: str):
    """read the "File" and return a list w/ all the needed information ->
    [n_point,[data_dim1,data_dim2,...]] where data_dim1 is a list of couple
    the couple is two float like this (ppm,amplitude)"""
    # I will use [a:-1] to remove useless part of the data.
    o_file = open(file, "r")
    o_file_list = o_file.readlines()
    start = len(o_file_list) + 1
    data_list = [[]]
    current_dimension = 0
    XDIM = False
    End = False
    abs_f1 = False
    abs_f2 = False
    vardim = False
    n_dim = 1
    for i in enumerate(o_file_list, 0):  # the data isn't alway at the same place.
        if not (XDIM) and ("##NPOINTS" in i[1]) and ("$$" not in i[1]):
            # print(i[1])
            # print()
            n_point = int(i[1][11:-1])
            XDIM = True

        if not (End) and ("$$ End of Bruker specific parameters" in i[1]):
            start = i[0] + 17
            End = True

        if not (abs_f1) and ("##$ABSF1" in i[1]):
            max_ppm = float(i[1][10:-1])
            abs_f1 = True

        if not (abs_f2) and ("##$ABSF2" in i[1]):
            min_ppm = float(i[1][10:-1])

        if not (vardim) and ("##VAR_DIM" in i[1]):
            vardimaslist = i[1].split()
            n_point = int(vardimaslist[2][:-1])
            n_dim = int(vardimaslist[1][:-1])
            vardim = True

        if i[0] > start and ("##" not in i[1]):
            point = i[1].split()
            point[0] = int(point[0]) * ((max_ppm - min_ppm) / n_point) + min_ppm
            point[1] = float(point[1])
            data_list[current_dimension].append(point)

        elif (i[0] > start) and ("##END" not in i[1]):
            # print(i[1])
            data_list.append([])
            current_dimension += 1
            start = i[0] + 3
        # print(n_point, data_list)
    return [n_point, data_list, n_dim]


def afficher(rawdata, dim):
    """take rawdata and show the spectrum"""
    dim = dim - 1
    points = [rawdata[1][dim][i][0] for i in range(len(rawdata[1][dim]))]
    amplitude = [rawdata[1][dim][i][1] for i in range(len(rawdata[1][dim]))]
    print(points[0])
    points.reverse()
    amplitude.reverse()
    print(points[0])
    (line,) = plt.plot(points, amplitude, linewidth=float("0.1"))
    plt.gca().invert_xaxis()
    line.set_antialiased(False)


def model_t0(x, i0, t0):
    return i0 * (1 - 2 * exp((-x) / t0))


def fitting(bucket_int, delta_list):
    x = [i * delta_list[i] for i in range(len(bucket_int))]
    print(x, bucket_int)
    p0 = [100, 1]
    popt, pops = curve_fit(model_t0, x, bucket_int, p0)
    return (popt, pops)


def afficher_coube_model(ndim, delta_list, i0, t0):
    x = [i * delta_list[i] for i in range(ndim)]
    y = []
    for i in x:
        # print(i)
        y.append(model_t0(i, i0, t0))
    # print(x, y)
    plt.plot(x, y)


def export_xlsx(data_list, buckets_list, nb_max_buckets, input, resfit_list):
    """data_list: [[data_dim1],[data_dim2],...]], buckets_list: [[buckets_dim1],[bucket_dim2],...],
    resfit : [int,int], input: str
    """
    parametre = 4

    if "/" in input:
        name = str(input.split("/")[-1])
    else:
        name = str(input.split("\\")[-1])

    workbook = xlsxwriter.Workbook("./export/data.xlsx")
    worksheet = workbook.add_worksheet()

    cell_width = 50
    cell_height = 200
    worksheet.set_column(0, len(buckets_list[0]), cell_width)
    worksheet.set_row(5, cell_height)

    worksheet.write(0, 0, name)
    worksheet.write(0, 1, parametre)

    for i in range(nb_max_buckets):
        bucket_number = "bucket" + str(i + 1)
        bucket_start = data_list[0][buckets_list[0][i][0]][0]
        bucket_last = data_list[0][buckets_list[0][i][1]][0]
        bucket_mid = (
            data_list[0][buckets_list[0][i][1]][0]
            + data_list[0][buckets_list[0][i][0]][0]
        ) / 2
        parameter_exp = str(resfit_list[i])
        path_image = "./export/img/bucket_{}.png".format(str(i))

        worksheet.write(1, i, bucket_number)
        worksheet.write(2, i, bucket_start)
        worksheet.write(3, i, bucket_mid)
        worksheet.write(4, i, bucket_last)
        worksheet.write(5, i, parameter_exp)
        worksheet.insert_image(
            6,
            i,
            path_image,
            {"object_position": 1, "x_scale": 0.58, "y_scale": 0.57},
        )

    workbook.close()


if __name__ == "__main__":
    afficher_coube_model(12, 7.7, 7.90304580e04, -7.94691988e07)
    plt.show()
