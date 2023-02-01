"""this is the code of the programm"""


def read_rmn(file: str):
    """ read the "File" and return a list w/ all the needed information ->
     [n_point,[data_dim1,data_dim2,...]] where data_dim1 is a list of couple
     the couple is two float like this (ppm,amplitude)"""
    # I will use [a:-1] to remove useless part of the data.
    o_file = open(file, "r")
    o_file_list = o_file.readlines()
    start = len(o_file_list) + 1
    data_list = [[]]
    current_dimension = 0
    start_data = len(o_file_list) + 1
    XDIM=False;End=False;abs_f1=False;abs_f2=False
    for i in enumerate(o_file_list, 0):  # the data isn't alway at the same place.
        if not(XDIM) and("##$XDIM" in i[1]):
            n_point = int(i[1][9:-1])
            XDIM=True

        if not(End) and ("$$ End of Bruker specific parameters" in i[1]):
            start = i[0] + 1
            End=True

        if not(abs_f1) and ("##$ABSF1" in i[1]):
            max_ppm = float(i[1][10:-1])
            abs_f1=True

        if not(abs_f2) and("##$ABSF2" in i[1]):
            min_ppm = float(i[1][10:-1])

        if i[0] > start and ("##" not in i[1]):
            point = i[1].split()
            point[0] = int(point[0]) * ((max_ppm - min_ppm) / n_point) + min_ppm
            point[1] = float(point[1])
            data_list[current_dimension].append(point)
            start_data = i[0] + n_point

        if i[0] > start_data:
            data_list.append(list())
            current_dimension += 1
            start = start_data

    # print(n_point, data_list)

    return [n_point, data_list]


if __name__ == "__main__":
    print(read_rmn("test_data/1D.dx"))
