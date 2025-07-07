import glob
import pandas as pd
from andes_set_image_poster import AndesSetImagePoster


# Mission Pétoncle Minganie 2025
# Two runs, one for 16E and 16F, activate mission in ANDES for each

SERVER_URL = "http://iml-science-4.ent.dfo-mpo.ca:25012"
# SERVER_URL = "http://localhost:8000"

IMAGE_PATH = '\\\\stockage-vroy.ent.dfo-mpo.ca/stockage/BIIGLE/EGSL-Minganie-Pétoncles/IML-2025-012'

asip = AndesSetImagePoster(url=SERVER_URL)
asip.set_headers(
    csrftoken='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    sessionid='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    csrfmiddlewaretoken='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    )


# the set export csv from ANDES provides a map between set id and set number
# sets = pd.read_csv('IML2025012E_set_export.csv', encoding='windows-1252')
sets = pd.read_csv('IML2025012F_set_export.csv', encoding='windows-1252')

for file in sorted(glob.glob(f'{IMAGE_PATH}/*.jpg')):
    filename = file.split('\\')[-1]
    missions_variant = filename.split('_')[1]

    # if missions_variant == '16E':
        # set_num = int(filename.split('_')[2])
        # set_id = sets['set_id'][sets['set_number']==set_num].values[0]
        # print(file, set_num, set_id)
        # asip.post_image(set_id, file)

    if missions_variant == '16F':
        # parse set_number from the filename
        set_num = int(filename.split('_')[2])
        set_id = sets['set_id'][sets['set_number']==set_num].values[0]
        print(file, set_num, set_id)
        asip.post_image(set_id, file)

    # exit()
