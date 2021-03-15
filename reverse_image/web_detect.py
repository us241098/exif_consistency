import argparse
import io
import json
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson
import glob
from multiprocessing import Process

def annotate(path):

    """Returns web annotations given the path to an image."""
    try:
        client = vision.ImageAnnotatorClient()

        if path.startswith('http') or path.startswith('gs:'):
            image = types.Image()
            image.source.image_uri = path

        else:
            with io.open(path, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

        web_detection = client.web_detection(image=image).web_detection
        jsonObj = MessageToJson(web_detection)
        jsonObj=json.loads(jsonObj)
        with open(path+'.json', 'w') as f:
            json.dump(jsonObj, f)
        
        return jsonObj
    except:
        pass

def report(annotations):
    """Prints detected features in the provided web annotations."""
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if annotations.full_matching_images:
        print('\n{} Full Matches found: '.format(
              len(annotations.full_matching_images)))

        for image in annotations.full_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.partial_matching_images:
        print('\n{} Partial Matches found: '.format(
              len(annotations.partial_matching_images)))

        for image in annotations.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
              len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))


if __name__ == '__main__':
    txt_files = glob.glob("./politi_train/*.jpg")
    json_files = glob.glob("./politi_train/*.json")
    
    image_files=[]
    yes=[]
    print(len(txt_files))
    for i in txt_files:
        flag=0
        for j in json_files:
            if i in j:
                flag=1
                yes.append('yes')
        
        if flag==0:
            print (i)
            annotate(i)
        
        #print (flag)
    
    print (len(yes))
        #annotate(i)

    
    #image_files.append(i)
    #
    #report(annotate(args.image_url))