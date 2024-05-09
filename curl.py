import requests
from bs4 import BeautifulSoup

url = 'https://us-central1-ifac-digital-standards-pub.cloudfunctions.net/getDownloadURL'
headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer 168e25b4-c92f-458d-9cdc-cb875ad3d682',
    'content-type': 'application/json',
    'origin': 'https://ifac-digital-standards-pub.web.app',
    'priority': 'u=1, i',
    'referer': 'https://ifac-digital-standards-pub.web.app/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

data = {
    'boardName': 'iaasb',
    'version': '2011',
    'userIdentifier': '4034555',
}

responseURL = requests.post(url, headers=headers, json=data)

if responseURL.status_code == 200:
    print("Request successful")
    # print("Response:", responseURL.json())
    download_url = responseURL.json()['downloadUrl']
else:
    print("Request failed with status code:", responseURL.status_code)



response = requests.get(download_url)

if response.status_code == 200:
    json_data = response.json()

    
    id_to_find = "MASTER_1"  # The id value you want to find
    content = None
    
    for result in json_data["result"]:
     for handbook in result["handbook"]:
        for item in handbook:
            if item["id"] == id_to_find:
                content = item["content"]
                break

        # Output
    # if content:
    #     print("Content for ID", id_to_find, ":", content)
    # else:
    #     print("ID", id_to_find, "not found.")


    soup = BeautifulSoup(content, 'html.parser')

    content_list = []

    for element in soup.find_all():
        print(element.name)

    # Extract text content from <p> tags
    p_tags = soup.find_all('p')
    for p_tag in p_tags:
        text_segments = []
        for child in p_tag.children:
            if isinstance(child, str):
                text_segments.append({"type": "text", "text": child.strip()})
            elif child.name == 'strong':
                text_segments.append({"type": "bold", "text": child.get_text(strip=True)})
            elif child.name == 'em':
                text_segments.append({"type": "italic", "text": child.get_text(strip=True)})
            elif child.name == 'span':
                text_segments.append({"type": "tooltip", "text": child.get_text(strip=True)})
            # if child.name == 'strong':
            #     text_segments.append({"type": "strong", "text": child.get_text(strip=True)})
            # elif child.name == 'em':
            #     text_segments.append({"type": "em", "text": child.get_text(strip=True)})
            # elif isinstance(child, str):
            #     text_segments.append({"type": "text", "text": child.strip()})
        content_list.append({
            "tag": "p",
            "id": p_tag['id'],
            "text": text_segments
        })

    # Extract text content from <ul> tags
    ul_tags = soup.find_all('ul')
    for ul_tag in ul_tags:
        li_tags = ul_tag.find_all('li')
        li_contents = []
        for li_tag in li_tags:
            text_segments = []
            for child in li_tag.children:
                if isinstance(child, str):
                    text_segments.append({"type": "text", "text": child.strip()})
                elif child.name == 'strong':
                    text_segments.append({"type": "bold", "text": child.get_text(strip=True)})
                elif child.name == 'em':
                    text_segments.append({"type": "italic", "text": child.get_text(strip=True)})
                elif child.name == 'span':
                    text_segments.append({"type": "tooltip", "text": child.get_text(strip=True)})
            li_contents.append({
            "tag": "li",
            "id": li_tag['id'],
            "content": text_segments
        })
        content_list.append({
            "tag": "ul",
            "class": ul_tag['class'][0],
            "items": li_contents
        })

    # print(content_list)

else:
    print("Failed to fetch data:", response.status_code)