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

# the set export csv from ANDES provides a map between set id and set number
sets = pd.read_csv('IML2025007_set_export.csv', encoding='windows-1252')

for file in sorted(glob.glob(f'{IMAGE_PATH}/*.jpg')):
    filename = file.split('\\')[-1]

    # parse set_number from the filename
    set_num = int(filename.split('_')[1])
    # map to set_id from the CSV
    set_id = sets['set_id'][sets['set_number']==set_num].values[0]

    print(file, set_num, set_id)
    asip.post_image(set_id, file)
    # exit()
