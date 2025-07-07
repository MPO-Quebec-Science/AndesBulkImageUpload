# AndesBulkImageUpload


input: a file listing with using a standardized naming format, i.e.,`IML-2025-012_16E_001_0007.jpg`

<mission_id>_<zone>_<set_number>_<image_number>.jpg
The code will need to parse the set_number or set-id out of the filename.

output: api calls to an andes instance to add Set images (the set is parsed from the file name)
The API call needs the `set_id`. If we only have the `set_number` it is possible to map it to `set_number` using the set export csv from ANDES.

# How go I get all the tokens!?
One day I'll add an API token manager to Andes. In the meantime, login to ANDES and use the swagger interface (http://<ANDES_URL>/api/images/) to make a post request for a test image. Look at the devtools' network tab to see the request headers and form data payload.
There you should be able to sniff out the `csrftoken`, `sessionid` and `csrfmiddlewaretoken`.

# notes
- The API call will upload files to the ANdes target instance.
- API calls will need a valid CSRF token and headers.
- The APi call needs to know the `set_id`.
- If the `set_number` is parsed from the filename, it can be mapped to `set_id` using the set export CSV.

