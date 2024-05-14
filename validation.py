import readWebEBook
import readWordFile

wordFileList = readWordFile.read_docx_with_formatting("C:\RnD\DocReactPOC\docTestNew.docx");


# wordFileList = readWordFile.read_docx_with_formatting("C:\RnD\DocReactPOC\A005 2021 Preface to the I.docx");
webEbookList = readWebEBook.process_list("MASTER_1");

print("Char length of the word file list:", len(wordFileList));
print("Char length of the web ebook file list:", len(webEbookList));


for index, item1 in enumerate(webEbookList):
    item2 = wordFileList[index]

    if(item1['type'] == 'tooltip'): # bypassed tooltip as it is not present in word file
        webtype = 'text'
    else:
        webtype = item1['type']

        

    if (item1['text'] == item2['text']):
         if(webtype != item2['type']):
             print(f"Type of char at index {index} is different: web e book-{webtype} != word file-{item2['type']} for char {item1['text']}")  
         if(item1['tag'] != item2['tag']):
             print(f"Tag of char at index {index} is different: web e book-{item1['tag']} != word file-{item2['tag']} for char {item1['text']}")  

            
    else:
        print(f"Text at char at index {index} is different: web e book-{item1['text']} != word file-{item2['text']}")
        # my_list = [779, 1014, 3575, 3864, 4556] # bypassed 's
        # if(index not in my_list):
        # break