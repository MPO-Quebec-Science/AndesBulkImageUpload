# AndesBulkImageUpload


input: a file listing with using a standardized naming format, i.e.,`IML-2025-012_16E_001_0007.jpg`

<mission_id>_<zone>_<set_number>_<image_number>.jpg

output: api calls to an andes instance to add Set images (the set is parsed from the file name)

# How go I get all the tokens!?
One day I'll add an API token manager to Andes. In the meantime, login to ANDES and use the swagger interface (http://<ANDES_URL>/api/images/) to make a post request for a test image. Look at the devtools' network tab to see the request headers and form data payload.
There you should be able to sniff out the `csrftoken`, `sessionid` and `csrfmiddlewaretoken`.

# notes
- The files will not be uploaded to the server, the API call will only create the Image Object.
- The image files has to be uploaded to the ANDES server.
- API calls will need a valid CSRF token and headers.

