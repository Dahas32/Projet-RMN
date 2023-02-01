"""this file is the test file for rmn"""

import rmn


def test_read_1d():
    """test for 1D"""
    output = rmn.read_rmn("test_data/1D.dx")
    test_data = open("test_data/1D_DATA.txt", "r").readlines()
    assert output[0] == 16384
    for i in enumerate(test_data, 0):
        donne = i[1].split()
        donne[0] = float(donne[0])
        donne[1] = float(donne[1])
        assert (abs(output[1][0][i[0]][0] - donne[0]) < 1e-3) and (
            abs(output[1][0][i[0]][1] - donne[1]) < 1e-3
        )  # I couldn't use approx because test data made w/ the online tool gave approximated value w/ 10^-3 and not 10^-6
        print(donne)
    # print(test_data)
    print(output[1][0][-1])


'''def test_read_2d():
    """test for 2d"""
    output=rmn.read_rmn("test_data/serum_dynamic_221125.dx")'''
