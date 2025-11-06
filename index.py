mylist = [
    {
        'Name': 'python',
        'Id': 123123,
        'List': [{'Name': 'list name', 'Identifier': 321}],
        'Keys': {
            'Key1': 'unique key',
            'Key2': 'unique key2',
            'Key3': [
                {
                	'newVar': 'string',
                }
            ]
        }
    }
]

mapping = [
	{
    	"sourceId": "Name",
        "field": "name"
    },
    {
    	"sourceId": "Id",
        "field": "id"
    },
    {
    	"sourceId": "List",
        "field": "list",
        'fields': [
        	{
            	"sourceId": "Name",
                "field": "name",
            },
            {
            	"sourceId": "Identifier",
                "field": "id",
            },
        ]
    },
    {
    	"sourceId": "Keys",
        "field": "keys",
        'fields': [
        	{
            	"sourceId": "Key1",
                "field": "property1",
            },
            {
            	"sourceId": "Key2",
                "field": "property2",
            },
            {
            	"sourceId": "Key3",
                "field": "list",
                'fields': [
                    {
                    	"sourceId": "newVar",
                        "field": "xd",
                    }
                ]
            },
        ]
    },
]


def findMappedField(key, mapping):
  for item in mapping:
        if item.get('sourceId') == key:
            return item.get('field')
  return None


def mapFields(mapping, item):
  new_keys = {}
  for key in item.keys():
    field = findMappedField(key, mapping)
    if field is not None:
        item_type = type(item[key])
        if item_type is str or item_type is int:
          new_keys[field] = item[key]
        if item_type is list:
            nested_mapping = getNestedFields(mapping, key)
            new_keys[field] = processFields(item[key], nested_mapping)
        if item_type is dict:
            nested_mapping = getNestedFields(mapping, key)
            new_keys[field] = mapFields(nested_mapping, item[key])
  return new_keys

def getNestedFields(mapping_fields, field):
  for m in mapping_fields:
  	if m.get('sourceId') == field and m.get('fields') is not None:
          return m.get('fields')
  return None

def processFields(list_data, mapping_fields):
  data = []
  for item in list_data:
    data.append(mapFields(mapping_fields, item))
  return data

data = processFields(mylist, mapping)
print(mylist)
print('----')
print(data)
