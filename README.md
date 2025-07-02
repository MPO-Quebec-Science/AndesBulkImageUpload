# AndesBulkImageUpload


input: a file listing with using a standardized naming format, i.e.,`IML-2025-012_16E_001_0007.jpg`

<mission_id>_<zone>_<set_number>_<image_number>.jpg

output: api calls to an andes instance to add Set images (the set is parsed from the file name)

# notes
- The files will not be uploaded to the server, the API call will only create the Image Object.
- The image files has to be uploaded to the ANDES server.
- API calls will need a valid CSRF token and headers.

