from CrudeOilBlending.utils import GetCrudeProfile
import os

def test_getdatafromwebsite():
    num_files = 1
    download_path = os.getcwd() + "\\tmp\data\\"
    stream_ = ["RA"]
    page_url = "https://www.crudemonitor.ca/crudes/index.php?acr="

    GetCrudeProfile(stream_, page_url, download_path, num_files, rm_files=True)

if __name__ == "__main__":
    test_getdatafromwebsite()