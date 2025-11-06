import requests
import os
from dotenv import load_dotenv

load_dotenv()

COMPANY_ID=7
WEBSITE_ID=2
BASE_URL = 'https://20.110.145.4:50000/b1s/v1'
COMPANY = 'Castrol'

BASE_WEBHOOK_URL=os.getenv('BASE_WEBHOOK_URL')
PRODUCTS_WEBHOOK_ID=os.getenv('PRODUCTS_WEBHOOK_ID')
CLIENTS_WEBHOOK_ID=os.getenv('CLIENTS_WEBHOOK_ID')
PRICE_LISTS_WEBHOOK_ID=os.getenv('PRICE_LISTS_WEBHOOK_ID')
STOCK_WEBHOOK_ID=os.getenv('STOCK_WEBHOOK_ID')
STOCK_LOCATIONS_WEBHOOK_ID=os.getenv('STOCK_LOCATIONS_WEBHOOK_ID')
DISCOUNT_WEBHOOK_ID=os.getenv('DISCOUNT_WEBHOOK_ID')

DISCOUNT_GROUP_FIELDS = {
    'mapping': [
        {
            "sourceId": "EnhancedDiscountGroups/DiscountGroupLineCollection",
            "field": "discountGroups",
            'fields': [
                {
                    "sourceId": "ObjectCode",
                    "field": "code",
                },
                {
                    "sourceId": "Discount",
                    "field": "discount",
                },
                {
                    "sourceId": "ObjectType",
                    "field": "objectType",
                },
            ],
        },
        {
            "sourceId": "BusinessPartnerGroups",
            "field": "businessPartnerGroups",
            'fields': [
                {
                    "sourceId": "Name",
                    "field": "name",
                },
                {
                    "sourceId": "Code",
                    "field": "code",
                },
            ],
        },
        {
            "sourceId": "Manufacturers",
            "field": "manufacturers",
            'fields': [
                {
                    "sourceId": "Code",
                    "field": "code",
                },
                {
                    "sourceId": "ManufacturerName",
                    "field": "name",
                },
            ],
        },
        
    ]
}

ADDITIONAL_FIELDS = {
    "company_id": COMPANY_ID,
    "website_id": WEBSITE_ID,
}

STOCK_FIELDS= {
    'mapping': [
        {
            "sourceId": "ItemName",
            "field": "name",
        },
        {
            "sourceId": "QuantityOnStock",
            "field": "quantity"
        },
    ],
    'additional_fields': None
}

ITEM_FIELDS = {
    'mapping': [
        {
            "sourceId": "ItemCode",
            "field": "default_code"
        },
        {
            "sourceId": "ItemName",
            "field": "name",
        },
        {
            # change
            "sourceId": "ItemsGroupCode",
            "field": "itemsGroupCode",
        },
        {
            "sourceId": "QuantityOnStock",
            "field": "quantity"
        },
        {
            "sourceId": "ItemPrices",
            "field": "prices",
            "fields": [
                {
                    "sourceId": "PriceList",
                    "field": "listId",
                },
                {
                    "sourceId": "Price",
                    "field": "price",
                },
                {
                    "sourceId": "Currency",
                    "field": "currency_id",
                },
            ]
        }
    ],
    'additional_fields': {
        'sale_ok': True,
        'detailed_type': 'product',
        'list_price': 0,
        'active': True,
        **ADDITIONAL_FIELDS,
    }
}

CLIENT_FIELDS = {
    'mapping': [
        {
            "sourceId": "CardName",
            "field": "name",
        },
        {
            "sourceId": "Phone1",
            "field": "phone",
        },
        {
            "sourceId": "CardCode",
            "field": "vat",
        },
        {
            "sourceId": "PriceListNum",
            "field": "property_product_pricelist",
        },
        {
            # change
            "sourceId": "GroupCode",
            "field": "groupCode",
        },
        {
            "sourceId": "BPAddresses",
            "field": "addresses",
            "fields": [
                {
                    "sourceId": "Country",
                    "field": "country_id"
                },
                {
                    "sourceId": "State",
                    "field": "state"
                },
                {
                    "sourceId": "City",
                    "field": "city"
                },
                {
                    "sourceId": "ZipCode",
                    "field": "zip"
                },
                {
                    "sourceId": "Street",
                    "field": "street",
                }
            ],
        },
    ],
    'additional_fields': ADDITIONAL_FIELDS,
}

PROCE_LIST_FIELDS = {
    'mapping': [
        {
            "sourceId": "PriceListName",
            "field": "name",
        },
        {
            "sourceId": "DefaultPrimeCurrency",
            "field": "currency_id",
        },
        {
            "sourceId": "PriceListNo",
            "field": "listId",
        }
    ],
    'additional_fields': {
        "discount_policy": "without_discount",
        **ADDITIONAL_FIELDS,
    }
}

# authorization request
def authorization(s: requests):
    print('credential')
    print(os.getenv('COMPANY_DB'))
    payload = {
        "CompanyDB": os.getenv('COMPANY_DB'),
        "UserName": os.getenv('CASTROL_USERNAME'),
        "Password": os.getenv('CASTROL_PASSWORD'),
    }
    url = f"{BASE_URL}/Login"
    return s.post(url, json=payload, verify=False, timeout=20)

# request to list clients
def listClients(s: requests, nextLink = None):
    endpoint = "BusinessPartners?$select=CardName,Phone1,CardCode,GroupCode,BPAddresses,PriceListNum&$filter=Properties26 eq 'tYES'"
    if nextLink is not None:
        endpoint = nextLink
    return s.get(f"{BASE_URL}/{endpoint}", verify=False)

# request to list items
def listItems(s: requests, nextLink = None):
    endpoint = "Items?$select=ItemCode,ItemName,ItemsGroupCode,ItemPrices,QuantityOnStock,ItemWarehouseInfoCollection&$filter=startswith(ItemCode, 'ACA') and SalesItem eq 'tYES' and not(ItemsGroupCode eq 106) and not(ItemsGroupCode eq 104)"
    if nextLink is not None:
        endpoint = nextLink
    return s.get(f"{BASE_URL}/{endpoint}", verify=False)

# get priceList response
def listPriceLists(s: requests, nextLink = None, query = None):
    filter = '$select=DefaultPrimeCurrency,PriceListName,PriceListNo'
    endpoint = f"PriceLists?{filter}"
    if nextLink is not None:
        endpoint = nextLink
    return s.get(f"{BASE_URL}/{endpoint}", verify=False)

# get SAP discount Groups
def listDiscountGroups(s: requests, nextLink = None, query = None):
    endpoint = 'QueryService_PostQuery?'
    entities = '$expand=EnhancedDiscountGroups($select=AbsEntry,ObjectCode,Type),EnhancedDiscountGroups/DiscountGroupLineCollection($select=ObjectCode,Discount,ObjectType,AbsEntry),Manufacturers($select=Code,ManufacturerName),BusinessPartnerGroups($select=Name,Code)'
    filter = f"$filter=EnhancedDiscountGroups/Type eq 'C' and EnhancedDiscountGroups/DiscountGroupLineCollection/ObjectType eq '43' and EnhancedDiscountGroups/DiscountGroupLineCollection/AbsEntry eq EnhancedDiscountGroups/AbsEntry and BusinessPartnerGroups/Code eq EnhancedDiscountGroups/ObjectCode and Manufacturers/Code eq EnhancedDiscountGroups/DiscountGroupLineCollection/ObjectCode"
    queryOption = f'{entities}&{filter}'
    if nextLink is not None:
        queryOption = nextLink.replace(endpoint, '')
    body = {
        'QueryPath': '$crossjoin(EnhancedDiscountGroups,BusinessPartnerGroups,Manufacturers,EnhancedDiscountGroups/DiscountGroupLineCollection)',
        'QueryOption': queryOption,
    }
    return s.post(f"{BASE_URL}/{endpoint}", json=body, verify=False)

# get odoo field name from the source field name if any
def getField(name, mapping_fields):
    for m in mapping_fields:
        if m.get('sourceId') == name:
            return m.get('field')
    return None

# check if the field is nested or simple field
def getNestedMapping(field, mapping_fields):
    for m in mapping_fields:
        if m.get('sourceId') == field and m.get('fields') is not None:
            return m.get('fields')
    return None


# replace source attribute to odoo required attribute naming convention
def mapFieldNames(item, mapping_fields, additional_fields = None):
    new_keys = {}
    for key in item.keys():
        field = getField(key, mapping_fields)
        if field is not None:
            type_field = type(item[key])
            if type_field is not dict and type_field is not list:
                new_keys[field] = item[key]
            if type_field is list:
                nested_mapping = getNestedMapping(key, mapping_fields)
                if nested_mapping is not None:
                    new_keys[field] = processFields(item[key], nested_mapping)
            if type_field is dict:
                nested_mapping = getNestedMapping(key, mapping_fields)
                if nested_mapping is not None:
                    new_keys[field] = mapFieldNames(item[key], nested_mapping)
    if additional_fields is not None:
        new_keys = {
            **new_keys,
            **additional_fields,
        }
    # print(new_keys)
    return new_keys

# transform source fields into odoo required fields structure
def processFields(items, mapping_fields, additional_fields = None):
    mappedValues = []
    for item in items:
        mappedValues.append(mapFieldNames(item, mapping_fields, additional_fields))
    return mappedValues

# send the data to the webhook
def streamData(s: requests, endpoint, payload: dict[str, any]):
    try: 
        print('sending request...')
        requests.post(f"{BASE_WEBHOOK_URL}/{endpoint}", json=payload)
        # requests.post(f'http://localhost:3000/webhook/{endpoint}', json=payload)
    except:
        print('error')

# handle clients stream data
def processClientsRequest(s: requests):
    next_link = None
    data = []
    
    while True:
        clients_response = listClients(s, next_link)
        payload = processFields(
            clients_response.json().get('value'),
            CLIENT_FIELDS.get('mapping'),
            CLIENT_FIELDS.get('additional_fields'),
            )

        for client in payload:
            email = f"{client.get('name').lower().replace(' ', '_')}@sample.com"
            client['email'] = email
            addresses = client['addresses']
            if len(addresses) > 0:
                first_address = addresses[0]
                client.update(first_address)
            if len(addresses) > 1:
                addresses.pop(0)
                client['addresses'] = addresses

        data = [
            *data,
            *payload,
        ]            

        # streamData(s, 'clients', payload=processResponse(payload))

        next_link = clients_response.json().get('odata.nextLink')
        if next_link is None:
            break
    return data

def processResponse(response):
    return {
        "count": len(response),
        "brand": COMPANY,
        "data": response,
    }

# handle items stream data
def processItemsRequest(s: requests):
    next_link = None
    data = []
    while True:
        items_response = listItems(s, next_link)
        payload = processFields(
            items_response.json().get('value'),
            ITEM_FIELDS.get('mapping'),
            ITEM_FIELDS.get('additional_fields'),
            )
        
        data = [
            *data,
            *payload
        ]
        # stock = processFields(items_response.json().get('value'), stock_fields_mapping)

        # streamData(s, 'stock', stock)

        # streamData(s, 'products', processResponse(payload))

        next_link = items_response.json().get('odata.nextLink')
        print(next_link)
        if next_link is None:
            break
    return data


# handle price lists stream data
def processPriceListRequest(s: requests, items = None):
    data = []
    next_link = None
    while True:
        price_list_response = listPriceLists(s, next_link)
        
        payload = processFields(
            price_list_response.json().get('value'),
            PROCE_LIST_FIELDS.get('mapping'),
            PROCE_LIST_FIELDS.get('additional_fields')
            )
        data = [
            *data,
            *payload,
        ]

        for list in payload:
            list['lines'] = []
            for item in items:
                for price in item.get('prices'):
                    if price.get('listId') == list.get('listId'):
                        list['lines'].append({
                            'product_tmpl_id': item.get('default_code'),
                            'name': item.get('name'),
                            'currency_id': price.get('currency_id'),
                            'fixed_price': price.get('price', 0.0)
                        })
        
        # for price_list in payload:
        #     streamData(s, 'price-lists', payload={
        #         "data": price_list,
        #     })

        next_link = price_list_response.json().get('odata.nextLink')
        if next_link is None:
            break
    return data

def processClientsList(s: requests, clients, price_lists):
    data = []
    for client in clients:
        if client['groupCode'] is not None:
            for list in price_lists:
                if client['property_product_pricelist'] == list['listId']:
                    data.append(client)
                    client_list = {
                        **list,
                        "listId": f"{list['listId']}-{client['vat']}",
                        "name": f"{list['name']} - {client['name']}",
                        'lines': []
                    }
                    items = []
                    for product in list.get('lines'):
                        if type(product['fixed_price']) is float:
                            items = [
                                *items,
                                {
                                    **product,
                                    "compute_price": 'formula',
                                    "base": "pricelist",
                                    "base_pricelist_id": list['listId'],
                                    "price_discount": "%",
                                    "applied_on": "3_global",
                                    "fixed_price": product['fixed_price'] * 2,
                                }
                            ]
                        else:
                            items = [
                                *items,
                                {
                                    **product,
                                }
                            ]
                        client_list['lines'] = items
                            
                    # print(client_list)
                    streamData(s, 'price-lists', payload=processResponse(client_list))
            break
        break
    
    return data

def handleRequest(
        s: requests,
        fields_config,
        webhook_id: str,
        exec_function: callable,
        ):
    next_link = None
    data = []
    while True: 
        response = exec_function(s, next_link)
        payload = processFields(
            response.json().get('value'),
            fields_config.get('mapping'),
        )


        data = [
            *data,
            *payload,
        ]

        streamData(s, webhook_id, payload=processResponse(payload))
        break

        next_link = response.json().get('odata.nextLink')
        if next_link is None:
            break

    return data
    

def processDiscountsRequest(s: requests):
    return handleRequest(s, DISCOUNT_GROUP_FIELDS, DISCOUNT_WEBHOOK_ID, listDiscountGroups)


def handler(event = None):
    print(event)
    with requests.Session() as s:
        authorization(s)
        # products = processItemsRequest(s)
        # print(len(products))

        # price_lists = processPriceListRequest(s, products)

        # clients = processClientsRequest(s)
        # client_lists = processClientsList(s, clients, price_lists)
        # print(len(client_lists))
        queryDiscounts = processDiscountsRequest(s)
        print(queryDiscounts)
handler()