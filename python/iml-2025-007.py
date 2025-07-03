import glob
import pandas as pd
from andes_set_image_poster import AndesSetImagePoster


# Mission BSM 2025
# 

SERVER_URL = "http://iml-science-4.ent.dfo-mpo.ca:25007"

IMAGE_PATH = '\\\\stockage-crabe.ent.dfo-mpo.ca\\stockage\\Photos BSM 2025\\andes'

asip = AndesSetImagePoster(url=SERVER_URL)
asip.set_headers(
    csrftoken='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    sessionid='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    csrfmiddlewaretoken='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    )
# asip.post_image(772, IMAGE_PATH+'/IML-2025-012_16E_001_0006.jpg')
# exit()

# provides a map between set id and set number
sets = pd.read_csv('IML2025007_set_export.csv', encoding='windows-1252')

for file in sorted(glob.glob(f'{IMAGE_PATH}/*.jpg')):
    filename = file.split('\\')[-1]
    set_num = int(filename.split('_')[1])
    set_id = sets['set_id'][sets['set_number']==set_num].values[0]
    # setNumber_181__IML-2024-058_181_2002.jpg
    # print(f"setNumber_{set_num:03d}__{filename} ")
    print(file, set_num, set_id)
    asip.post_image(set_id, file)
    # exit()
