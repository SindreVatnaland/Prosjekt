import xlrd
import numpy as np
from os import remove, listdir
from os.path import isfile, join
import os


def update_dictionary():
    loc = ("files/vareliste.xls")
    folder_loc = "files/"
    folder = [f for f in listdir(folder_loc) if isfile(join(folder_loc, f))]
    dictionary = np.load('my_file.npy',allow_pickle='TRUE').item()
    try:
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        for i in range(sheet.nrows):
            ean = (str(sheet.cell_value(i, 0))[0:-2])
            name = (str(sheet.cell_value(i, 6)))
            name2 = (str(sheet.cell_value(i, 7)))

            dictionary[ean] = name+" "+name2

        np.save('my_file.npy', dictionary)
        for file in folder:
            remove(folder_loc+file)
    except:
        for file in folder:
            try:
                remove(folder_loc+file)
            except:
                continue
        return


def make_folders():
    if not os.path.exists('oversikt/year/2020'):
        os.makedirs('oversikt/year/2020')
    if not os.path.exists('telling/year/2020'):
        os.makedirs('telling/year/2020')
    if not os.path.exists('ferdig'):
        os.makedirs('ferdig')
    if not os.path.exists('files'):
        os.makedirs('files')
    if not os.path.exists('barcodes'):
        os.makedirs('barcodes')

def setup():
    make_folders()
    update_dictionary()

if __name__ == '__main__':
    setup()