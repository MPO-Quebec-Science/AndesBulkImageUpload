import glob
import pandas as pd
from andes_set_image_poster import AndesSetImagePoster


# Mission 

SERVER_URL = "http://iml-science-4.ent.dfo-mpo.ca:XXXX"
IMAGE_PATH = '\\\\stockage-vroy.ent.dfo-mpo.ca/stockage/XXXXX'

asip = AndesSetImagePoster(url=SERVER_URL)
asip.set_headers(
    csrftoken='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    sessionid='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    csrfmiddlewaretoken='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    )

# asip.post_image(XXX, IMAGE_PATH+'/XXXX.jpg')
# exit()

# the set export csv from ANDES provides a map between set id and set number
sets = pd.read_csv('XXX_set-export.csv', , encoding='windows-1252'))

for file in sorted(glob.glob(f'{IMAGE_PATH}/*.jpg')):
    filename = file.split('\\')[-1]

    # parse set_number from the filename
    set_num = int(filename.split('_')[1])
    # map to set_id from the CSV
    set_id = sets['set_id'][sets['set_number']==set_num].values[0]
    print(file, set_num, set_id)
    # asip.post_image(set_id, file)
    # exit()
