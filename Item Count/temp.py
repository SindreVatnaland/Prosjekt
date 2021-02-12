import numpy as np
import requests
import os

dictionary = np.load('my_file.npy', allow_pickle='TRUE').item()


url = f'https://barcode.tec-it.com/barcode.ashx?data={7044416013141}&code=EAN13'
page = requests.get(url)

f_ext = os.path.splitext(url)[-1]
f_name = "barcodes/7044416013141.jpg"
with open(f_name, 'wb') as f:
    f.write(page.content)