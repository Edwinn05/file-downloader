import os
import re
import requests
import mimetypes
import platform
from urllib.parse import urlparse

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
})

def unique_file_path(storage_location,file_name,extension):
    extn= f"{extension}" if extension and not extension.startswith('.') else extension
    counter = 1
    basefile = f"{file_name}.{extn}"
    storage_path = os.path.join(storage_location,basefile)
    while os.path.exists(storage_path):
        basefile = f"{file_name}({counter}).{extn}"
        storage_path = os.path.join(storage_location,basefile)
        counter += 1
    return storage_path
def get_storage_location():
    if platform.system() in ['Windows','Darwin']:
        storage =os.path.join(os.path.expanduser("~"), "Desktop", "Downloads storage")
        return storage
    else:
        return os.path.join(os.getcwd(),"Downloads storage")

def file_download(url,file_name="untitled"):
    url_format =  r'https?://[\w\.-]+\.[a-z]{2,}(?:/[\w\.-]*)*'
    if not re.match(url_format,url,re.IGNORECASE):
        print('incorrect format')
        return
    
    storage_location = get_storage_location()
    os.makedirs(storage_location,exist_ok=True)

    try:
        with session.get(url,stream = True,timeout = 20) as r:
            print(f"Server Response Status Code: {r.status_code}")
            print(f"Raw Content-Type Header: {r.headers.get('Content-Type')}")
            r.raise_for_status()
            content_header = r.headers.get('Content-type','')
            content_type = content_header.split(';')[0].strip() if content_header else ''
            extension = mimetypes.guess_extension(content_type)
            if extension:
                extension = extension.lstrip('.')
            
            if not extension:
                parsed_url = urlparse(url)
                url_path = parsed_url.path
                match = re.search(r'\.([a-zA-Z0-9]+)$',url_path)
                extension = match.group(1) if match else 'unknown'
            storage_path = unique_file_path(storage_location,file_name,extension)
            with open(storage_path,"wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return f'successfully saved at {storage_path}'
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Download failed: {e}")    

if __name__ == '__main__':
    file_download("https://img.cdno.my.id/cover/w_936/h_390/justice-league-crisis-on-infinite-earths-part-three-1630857307.jpg")