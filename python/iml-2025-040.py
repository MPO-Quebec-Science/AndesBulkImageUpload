import glob
import pandas as pd
from andes_set_image_poster import AndesSetImagePoster


# Mission Spécial Buccin (Bic Sainte-Flavie) 2025


SERVER_URL = "http://iml-science-4.ent.dfo-mpo.ca:25040"

IMAGE_PATH = '\\\\stockage-buccin.ent.dfo-mpo.ca/stockage/IML-2025-040/photos_andes'

asip = AndesSetImagePoster(url=SERVER_URL)
asip.set_headers(
    csrftoken='blablabla',
    sessionid='blablabla',
    csrfmiddlewaretoken='blablabla'
    )
# asip.post_image(525, IMAGE_PATH+'/IMG_0647_IML-2025-040_001.jpg')
# exit()

# provides a map between set id and set number
sets = pd.read_csv('IML2025040_set_export.csv', encoding='windows-1252')

for file in sorted(glob.glob(f'{IMAGE_PATH}/*.jpg')):
    # print(file)
    filename = file.split('\\')[-1]
    filename = filename.split('.')[0]

    set_num = int(filename.split('_')[3])
    set_id = sets['set_id'][sets['set_number']==set_num].values[0]
    # setNumber_181__IML-2024-058_181_2002.jpg
    # print(f"setNumber_{set_num:03d}__{filename},")
    # print(file, set_num, set_id)

    asip.post_image(set_id, file)
    # print(r)
    # exit()
