
import logging
import requests


class AndesSetImagePoster:
    """ Add Set/Sample Images to an Andes instance using the API

        There is a small annoyance that requires manually setting sessionid and csrftoken in header data as well as csrfmiddlewaretoken in the form data.

    """

    def __init__(self, url:str|None=None, sessionid:str|None=None, csrftoken:str|None=None, csrfmiddlewaretoken:str|None=None):
        self.url = url
        self.cookies = {
            'sessionid': sessionid,
            'csrftoken': csrftoken,
        }
        self.csrfmiddlewaretoken = csrfmiddlewaretoken

    def set_headers(self, sessionid:str|None=None, csrftoken:str|None=None, csrfmiddlewaretoken:str|None=None):
        if sessionid:
            self.cookies['sessionid'] = sessionid
        if csrftoken:
            self.cookies['csrftoken'] = csrftoken
        if csrfmiddlewaretoken:
            self.csrfmiddlewaretoken = csrfmiddlewaretoken,

    def set_url(self, url:str):
        self.url = url

    def _is_ready(self):
        if not self.url:
            logging.getLogger(__name__).error("No URL set.")
            return False
        if not self.csrfmiddlewaretoken:
            logging.getLogger(__name__).error("No csrfmiddlewaretoken present in form data, use set_headers() to set one")
            return False

        for key, value in self.cookies.items():
            if not value:
                logging.getLogger(__name__).error("%s not present in cookie, use set_headers() to set one", key)
                return False
        return True


    def post_image(self, set_id:int, fname:str):
        """ Post a set image to the Andes server.
        set_id: int - the ID of the set to which the image belongs.
        fname: str - the path to the image file to be posted.
        """
        api_path = '/api/images/'
        if not self._is_ready():
            return 

        with open(fname, 'rb') as fp:
            form_data = {'sample': set_id,
                    'csrfmiddlewaretoken':self.csrfmiddlewaretoken,
                    }
            r = requests.post(self.url+api_path, data=form_data, cookies=self.cookies, files = {'image':fp})
            if not r.status_code==201:
                logging.getLogger(__name__).error("problem with set %s file %s", set_id, fname)
                logging.getLogger(__name__).error("status code %s", r.status_code)

                # print(r.text)
                # msg = r.json()
                # logging.getLogger(__name__).debug("error: %s", msg)

