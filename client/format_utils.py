import json


def to_json(prop_map):
    return json.dumps(prop_map)


def trim_description(metadata, desc_length):
    if metadata.prop_map['description'] is not None:
        desc = metadata.prop_map['description']
        desc = (desc[:desc_length] + '...') if len(desc) > desc_length else desc
        metadata.prop_map['description'] = desc
