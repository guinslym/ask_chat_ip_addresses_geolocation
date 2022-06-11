from ask_chat_ip_addresses_geolocation.main import * 
from ask_chat_ip_addresses_geolocation.main import handler 

# import package
import lh3.api
import ipinfo

access_token = "9c2fc435da6c9c"
handler = ipinfo.getHandler(access_token)

client = lh3.api.Client()

class ReseachTesting(object):
    def test_find_unique_ip_addresses(self):
        assert  1 == 2-1
    def test_download_chats_metadata_in_df(self):
        assert  1 == 2-1
    def test_importing_chats_metadata(self):
        assert  1 == 2-1
    def test_find_geolocation_from_ip_addresses(self):
        assert  1 == 2-1
    def test_isChat(self):
        assert  1 == 2-1
    def test_practiceQueues(self):
        assert  1 == 2-1