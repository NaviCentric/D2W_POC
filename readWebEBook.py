import requests
from bs4 import BeautifulSoup

def appendSegment(index, text_segments , child,tag):
     if(index == 0 and "-  " in child.get_text()):
         child_text = child.get_text().lstrip("-  ")
     elif(index == 0 and tag == 'ul'):
         child_text = child.get_text().lstrip()
     else:
         child_text = child.get_text()

     if isinstance(child, str):
        text_segments.append({"type": "text", "text": child_text})
     elif child.name == 'strong':
        text_segments.append({"type": "bold", "text": child_text})
     elif child.name == 'em':
        text_segments.append({"type": "italic", "text": child_text})
     elif child.name == 'span':
        text_segments.append({"type": "tooltip", "text": child_text})
     elif child.name == 's':
        text_segments.append({"type": "strikeThrough", "text": child_text})
     elif child.name == 'u':
            text_segments.append({"type": "underline", "text": child_text})
     elif child.name == 'a':
            text_segments.append({"type": "link", "text": child_text})
     elif child.name == 'data':
            if hasattr(child, 'children'):
              for index, grand_child in enumerate(child.children):
                appendSegment(index, text_segments , grand_child, tag)

            else:
                text_segments.append({"type": "text", "text": child_text})


def process_list(segment_id):
        
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
        'version': '2021',
        'userIdentifier': '4034555',
    }

    responseURL = requests.post(url, headers=headers, json=data)

    if responseURL.status_code == 200:
        print("Request successful")
        print("Response:", responseURL.json())
        download_url = responseURL.json()['downloadUrl']
    else:
        print("Request failed with status code:", responseURL.status_code)



    response = requests.get(download_url)

    if response.status_code == 200:
        json_data = response.json()

        content = None
        
        for result in json_data["result"]:
            for handbook in result["handbook"]:
                for item in handbook:
                    if item["id"] == segment_id:
                        content = item["content"]
                        break

        # if content:
        #     print("Content for ID", id_to_find, ":", content)
        # else:
        #     print("ID", id_to_find, "not found.")


        soup = BeautifulSoup(content, 'html.parser')

        content_list = []

        for element in soup.find_all():
            # print(element.name)
            if(element.name=='p'):
                text_segments = []

                if("class" in element.attrs and element.attrs["class"][0]=='level-1'):
                     text_segments.append({"type": "text", "text": "\t"})

                for index, child in enumerate(element.children):
                    appendSegment(index,text_segments , child,'p')
                content_list.append({
                    "tag": "p",
                    "id": element['id'],
                    "text": text_segments
                })

            elif (element.name=='div'):
                if not ("id" in element.attrs and element.attrs["id"] == segment_id):
                    text_segments = []
                    for index, child in enumerate(element.children):
                        appendSegment(index,text_segments , child,'div')
                    content_list.append({
                        "tag": "p",
                        # "id": child['id'],
                        "text": text_segments
                })


            elif (element.name=='ul'):
                li_tags = element.find_all('li')
                li_contents = []
                for li_tag in li_tags:
                    text_segments = []
                    # print(li_tag.text)
                    for index, child in enumerate(li_tag.children):
                        appendSegment(index,text_segments , child,'ul')

                    li_contents.append({
                    "tag": "li",
                    "id": li_tag['id'],
                    "content": text_segments
                })
                content_list.append({
                    "tag": "ul",
                    "class": element['class'][0],
                    "items": li_contents
                })


        # print(content_list)

        transformed_list = []

        for item in content_list:
            if(item['tag'] == 'p'):
                for text_item in item['text']:
                    text = text_item['text']
                    for char in text:
                        if(char != "\xa0"):
                            transformed_list.append({
                                "tag": item['tag'],
                                "id": item.get('id',"default_id"),
                                "type": text_item['type'],
                                "text": char
                            })
                    # print(transformed_list)
            elif(item['tag'] == 'ul'):
                for ul_items in item['items']:
                    for content_texts in ul_items['content']:
                        text = content_texts['text']
                        for char in text:
                             if(char != "\xa0"):
                                transformed_list.append({
                                    "tag": ul_items['tag'],
                                    "id": ul_items['id'],
                                    "type": content_texts['type'],
                                    "text": char
                                })
                        # print(transformed_list)

        # print(transformed_list)


        file_path = "webList.txt"

        with open(file_path, "w", encoding="utf-8") as file:
            for item in transformed_list:
                file.write(str(item) + "\n")

    else:
        print("Failed to fetch data:", response.status_code)

    return transformed_list