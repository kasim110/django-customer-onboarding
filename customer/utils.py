import boto3
import json
from django.conf import settings



def extract_text_from_document(file_path):
    client = boto3.client('textract', 
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME)
    
    
    imageBytes = file_path.read()
    
    # Call Amazon Textract
    response = client.analyze_document(Document={'Bytes': imageBytes}, FeatureTypes=['FORMS'])
    
    extracted_data = extract_key_value_pairs(response)
    extract_data_2 = {}

    for text,value in extracted_data.items():
        if 'surname' in text.lower():
            extract_data_2['surname'] = value
        elif 'firstname' in text.lower() or 'first name' in text.lower():
            extract_data_2['firstname'] = value
        elif 'nationality' in text.lower():
            extract_data_2['nationality'] = value
        elif 'gender' in text.lower() or 'sex' in text.lower():
            extract_data_2['gender'] = value


    
    return extract_data_2

def extract_key_value_pairs(textract_response):
        blocks = textract_response['Blocks']
        key_map, value_map, block_map = {}, {}, {}

        for block in blocks:
            block_id = block['Id']
            block_map[block_id] = block
            if block['BlockType'] == "KEY_VALUE_SET":
                if block['EntityTypes'][0] == 'KEY':
                    key_map[block_id] = block
                else:
                    value_map[block_id] = block

        kvs = get_kv_relationship(key_map, value_map, block_map)
        return kvs

def get_kv_relationship(key_map, value_map, block_map):
    kvs = {}
    for key_block in key_map.values():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)
        kvs[key] = val
    return kvs

def find_value_block(key_block, value_map):
    for relationship in key_block['Relationships']:
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                return value_map[value_id]

def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '    
    return text.strip()