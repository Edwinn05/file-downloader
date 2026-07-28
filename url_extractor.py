import re 
from url_download import file_download

def url_extracter(file_name):
    url_list = []
    url_pattern =  r'\b(?:https?://|www\.)\S+\b|\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b(?:\/\S*)?'
    try:
        with open(file_name,'r',encoding='utf-8') as file:
            content = file.read()
            found_urls = set(re.findall(url_pattern,content))
            urls = found_urls
            url_list.append(urls)
            for link in found_urls:
                downloads = file_download(link)
                url_list.append(downloads)
        return url_list
    except FileNotFoundError:
        print(f'The file {file_name} was not found.')
        return []