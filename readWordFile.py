from docx import Document
import json

def evaludateText_Segment(paragraph, text_segments):
     for run in paragraph.runs:
        if run.bold or run.font.element.style=='csbl' or run._parent.style.name == 'Heading 1' or run._parent.style.name == 'Heading 2':
            text_segments.append({"type": "bold", "text": run.text})
        elif run.italic or run.font.element.style=='Italic' or run.font.element.style=='csItl':
            text_segments.append({"type": "italic", "text": run.text})
        elif run.font.strike:
            text_segments.append({"type": "strikeThrough", "text": run.text})
        elif run.underline:
            text_segments.append({"type": "underline", "text": run.text})
        else:
            text_segments.append({"type": "text", "text": run.text}) 

def read_docx_with_formatting(file_path):
    doc = Document(file_path)
    content_list = []

    for paragraph in doc.paragraphs:
        paragraph_format = paragraph.paragraph_format
        nested_li = "false"
        # if(paragraph_format.first_line_indent == -347345):
        if(paragraph_format.left_indent is not None and paragraph_format.first_line_indent is not None and (abs(paragraph_format.first_line_indent) != abs(paragraph_format.left_indent))):
            # print(f"{paragraph.style} text : {paragraph.text}")
            # print(f"{paragraph_format.first_line_indent} text : {paragraph.text}")
            # print(f"{paragraph_format.left_indent} text : {paragraph.text}")
            nested_li = "true"


        # print(f"{paragraph_format.first_line_indent}")
        # print(f"{paragraph_format.left_indent}")
        
        if("Bullet" in paragraph.style.name or nested_li=="true"):
            text_segments = []
            evaludateText_Segment(paragraph , text_segments)
            content_list.append({
                    "tag": "li",
                    "text": text_segments
                })
            
        else:
            text_segments = []
            evaludateText_Segment(paragraph , text_segments)
            content_list.append({
                    "tag": "p",
                    "text": text_segments
                })

    #print(content_list)

    transformed_list = []

    for item in content_list:
        for text_item in item['text']:
            text = text_item['text']
            for char in text:
                if(char!='\n'):
                    transformed_list.append({
                        "tag": item['tag'],
                        # "id": item['id'],
                        "type": text_item['type'],
                        "text": char
                    })

    # print(transformed_list)

    file_path = "docList.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        for item in transformed_list:
            file.write(str(item) + "\n")


    return transformed_list

# file_path = "C:\RnD\DocReactPOC\docTest.docx"
# formatted_text = read_docx_with_formatting(file_path)
# print(formatted_text)
