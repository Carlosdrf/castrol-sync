import requests
import os
from dotenv import load_dotenv
import sys
import time

load_dotenv()

webhook_session = requests.Session()

webhook_session.headers.update({
    "x-api-key": os.getenv('WEBHOOK_CLIENT_API')
})

COMPANY_ID=os.getenv('COMPANY_ID')
WEBSITE_ID=os.getenv('WEBSITE_ID')
BASE_URL=os.getenv('BASE_URL')
COMPANY=os.getenv('COMPANY')

BASE_WEBHOOK_URL=os.getenv('BASE_WEBHOOK_URL')
ITEMS_WEBHOOK_ID=os.getenv('ITEMS_WEBHOOK_ID')
CLIENTS_WEBHOOK_ID=os.getenv('CLIENTS_WEBHOOK_ID')
PRICE_LISTS_WEBHOOK_ID=os.getenv('PRICE_LISTS_WEBHOOK_ID')
STOCK_WEBHOOK_ID=os.getenv('STOCK_WEBHOOK_ID')
STOCK_LOCATIONS_WEBHOOK_ID=os.getenv('STOCK_LOCATIONS_WEBHOOK_ID')
DISCOUNT_WEBHOOK_ID=os.getenv('DISCOUNT_WEBHOOK_ID')

DISCOUNT_GROUP_FIELDS = {
    'mapping': [
        {
            "sourceId": "AbsEntry",
            "field": "identifier",
        },
        {
            "sourceId": "ObjectCode",
            "field": "code",
        },
        {
            "sourceId": "Type",
            "field": "type",
        },
        {
            "sourceId": "DiscountGroupLineCollection",
            "field": "discountGroupLine",
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
                    "field": "type",
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
            "sourceId": "ItemCode",
            "field": "default_code",
        },
        {
            "sourceId": "InStock",
            "field": "inventory_quantity_auto_apply"
        },
        {
            "sourceId": "WarehouseCode",
            "field": "warehouse_code",
        },
    ],
    'additional_fields': None
}

STOCK_LOCATIONS_FIELDS = {
    'mapping': [
        {
            "sourceId": "WarehouseName",
            "field": "warehouse_name"
        },
        {
            "sourceId": "WarehouseCode",
            "field": "warehouse_code",
        },
    ]
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
            "sourceId": "Manufacturer",
            "field": "manufacturer"
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
        # {
        #     "sourceId": "CardName",
        #     "field": "name",
        # },
        # {
        #     "sourceId": "Phone1",
        #     "field": "phone",
        # },
        # {
        #     "sourceId": "CardCode",
        #     "field": "vat",
        # },
        # {
        #     "sourceId": "PriceListNum",
        #     "field": "property_product_pricelist",
        # },
        # {
        #     # change
        #     "sourceId": "GroupCode",
        #     "field": "groupCode",
        # },
        {
            'sourceId': 'PriceLists',
            'field': 'priceLists',
            'fields': [
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
            ]
        },
        {
            'sourceId': 'BusinessPartners',
            'field': 'businessPartners',
            'fields': [
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
                    "field": "commerce_id",
                },
                {
                    "sourceId": "PriceListNum",
                    "field": "property_product_pricelist",
                },
                {
                    'sourceId': 'FederalTaxID',
                    'field': 'vat'
                },
                {
                    # change
                    "sourceId": "GroupCode",
                    "field": "groupCode",
                },
                {
                    'sourceId': 'Sucursal',
                    'field': 'sucursal',
                },
            ],
        },
        {
            "sourceId": "BusinessPartners/BPAddresses",
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
                },
                {
                    "sourceId": "TaxCode",
                    "field": "tax_code",
                },
            ],
        },
    ],
    'additional_fields': ADDITIONAL_FIELDS,
}

PRICE_LIST_FIELDS = {
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

def handler(event = None):
    print(event)
    with requests.Session() as s:
        authorization(s)
        # products = processItemsRequest(s)

        # processDistributionCenterRequest(s)
        clients = processClientsRequest(s)

        # price_lists = processPriceListRequest(s, products)

        # print(clients.get('groupCodes'))

        # client_lists = processClientsList(s, clients, price_lists)

        # queryDiscounts = processDiscountsRequest(s, clients, price_lists)

# authorization request
def authorization(s: requests):
    payload = {
        "CompanyDB": os.getenv('COMPANY_DB'),
        "UserName": os.getenv('CASTROL_USERNAME'),
        "Password": os.getenv('CASTROL_PASSWORD'),
    }
    url = f"{BASE_URL}/Login"
    return s.post(url, json=payload, verify=False, timeout=20)

# request to list clients
# def listClients(s: requests, nextLink = None):
#     endpoint = "BusinessPartners?$select=CardName,Phone1,CardCode,GroupCode,BPAddresses,PriceListNum&$filter=Properties26 eq 'tYES'"
#     if nextLink is not None:
#         endpoint = nextLink
#     return s.post(f"{BASE_URL}/{endpoint}", verify=False)

def listClients(s: requests, next_link: str = None):
    endpoint = 'QueryService_PostQuery?'
    entities = '$expand=BusinessPartners($select=CardName,Phone1,CardCode,PriceListNum,GroupCode,FederalTaxID,Properties26,Properties1,Properties2,Properties3,Properties4,Properties5,Properties6),BusinessPartners/BPAddresses($select=Country,State,City,ZipCode,Street,TaxCode),PriceLists($select=PriceListName,DefaultPrimeCurrency,PriceListNo)'
    filter = f"$filter=BusinessPartners/U_Cwhatsapp eq 'S' and BusinessPartners/PriceListNum eq PriceLists/PriceListNo and BusinessPartners/BPAddresses/BPCode eq BusinessPartners/CardCode and not(BusinessPartners/BPAddresses/TaxCode eq '')"
    queryOption = f'{entities}&{filter}'
    if next_link is not None:
        queryOption = next_link.replace(endpoint, '')
    body = {
        'QueryPath': '$crossjoin(BusinessPartners,PriceLists,BusinessPartners/BPAddresses)',
        'QueryOption': queryOption,
    }
    return s.post(f"{BASE_URL}/{endpoint}", verify=False, json=body)

# request to list items
def listItems(s: requests, nextLink = None):
    endpoint = "Items?$select=ItemCode,ItemName,ItemsGroupCode,ItemPrices,Manufacturer,QuantityOnStock,ItemWarehouseInfoCollection,U_awhatsapp&$filter=U_awhatsapp eq 's'"
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
# def listDiscountGroups(s: requests, nextLink = None, query = ''):
#     endpoint = 'QueryService_PostQuery?'
#     entities = '$expand=EnhancedDiscountGroups($select=AbsEntry,ObjectCode,Type),EnhancedDiscountGroups/DiscountGroupLineCollection($select=ObjectCode,Discount,ObjectType,AbsEntry),Manufacturers($select=Code,ManufacturerName),BusinessPartnerGroups($select=Name,Code)'
#     filter = f"$filter=EnhancedDiscountGroups/Type eq 'C' and EnhancedDiscountGroups/DiscountGroupLineCollection/ObjectType eq '43' and EnhancedDiscountGroups/DiscountGroupLineCollection/AbsEntry eq EnhancedDiscountGroups/AbsEntry and BusinessPartnerGroups/Code eq EnhancedDiscountGroups/ObjectCode and Manufacturers/Code eq EnhancedDiscountGroups/DiscountGroupLineCollection/ObjectCode"
#     queryOption = f'{entities}&{filter} {query}'
#     if nextLink is not None:
#         queryOption = nextLink.replace(endpoint, '')
#     body = {
#         'QueryPath': '$crossjoin(EnhancedDiscountGroups,BusinessPartnerGroups,Manufacturers,EnhancedDiscountGroups/DiscountGroupLineCollection)',
#         'QueryOption': queryOption,
#     }
#     return s.post(f"{BASE_URL}/{endpoint}", json=body, verify=False)

def listDiscountGroups(s: requests, BPCode: str, BPGCode: str, next_link: str = None):
    filter = f"$filter=(Type eq 'C' and ObjectCode eq '{BPGCode}') or (Type eq 'S' and ObjectCode eq '{BPCode}') or (Type eq 'A') or (Type eq 'V' and ObjectCode eq '{BPGCode}')"
    endpoint = f'EnhancedDiscountGroups?{filter}'
    if next_link is not None:
        endpoint = next_link
    return s.get(f"{BASE_URL}/{endpoint}", verify=False)

def listDistributionCenters(s: requests, next_link = None, query = ''):
    endpoint = 'Warehouses'
    if next_link is not None:
        endpoint = next_link
    return s.get(f"{BASE_URL}/{endpoint}", verify=False)
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
        request = webhook_session.post(f"{BASE_WEBHOOK_URL}/{endpoint}", json=payload)
        print(request.json())
        request.raise_for_status()
        return request
    except requests.exceptions.RequestException as e:
        print('exception')
        print(e)
    except Exception as e:
        print(f'error: {e}')


def propertiesFieldManaging(response: requests.Response):
    data = []
    clients_response = response.json().get('value')
    for client in clients_response:
        print(client.get('BusinessPartners'))
        business = client.get('BusinessPartners')
        sucursal = 'Almacén Veracruz',
        if business.get('Properties1') == 'Y':
            sucursal = 'Almacén Villahermosa'
        if business.get('Properties2') == 'Y':
            sucursal = 'Almacén Tuxtla'
        if business.get('Properties3') == 'Y':
            sucursal = 'Almacén Tapachula'
        if business.get('Properties4') == 'Y':
            sucursal = 'Almacén Ciudad del Carmen'
        if business.get('Properties5') == 'Y':
            sucursal = 'Almacén Mérida'
        if business.get('Properties6') == 'Y':
            sucursal = 'Almacén Cancún'
        data.append({
            **client,
            'BusinessPartners': {
                **client.get('BusinessPartners'),
                'Sucursal': sucursal,
            },
        })

    return data

# handle clients stream data
def processClientsRequest(s: requests):
    next_link = None
    data = []
    
    while True:
        clients_response = listClients(s, next_link)
        clients_list = propertiesFieldManaging(clients_response)
        clients_fields = processFields(
            clients_list,
            CLIENT_FIELDS.get('mapping'),
            CLIENT_FIELDS.get('additional_fields'),
            )
        payload = []
        for item in clients_fields:
            email = f"{item.get('businessPartners').get('name').lower().replace(' ', '_')}@sample.com"
            payload.append({
                'name': item.get('businessPartners').get('name'),
                'phone': item.get('businessPartners').get('phone'),
                'vat': item.get('businessPartners').get('vat'),
                'sucursal': item.get('businessPartners').get('sucursal'),
                'groupCode': item.get('businessPartners').get('groupCode'),
                'commerce_id': item.get('businessPartners').get('commerce_id'),
                'country_id': item.get('addresses').get('country_id'),
                'state': item.get('addresses').get('state'),
                'city': item.get('addresses').get('city'),
                'zip': item.get('addresses').get('zip'),
                'street': item.get('addresses').get('street'),
                'tax_code': item.get('addresses').get('tax_code'),
                'property_product_pricelist': item.get('priceLists').get('name'),
                'distribution_center_id': 'Almacén Veracruz',
                'list_id': item.get('priceLists').get('listId'),
                'currency_id': item.get('priceLists').get('currency_id'),
                'listId': item.get('priceLists').get('listId'),
                'email': email,
                **ADDITIONAL_FIELDS,
            })
        
        data = [
            *data,
            *payload,
        ]            

        streamData(s, CLIENTS_WEBHOOK_ID, payload=prepareResponse(payload, 'Clients'))

        next_link = clients_response.json().get('odata.nextLink')
        if next_link is None:
            break
    return data

def prepareResponse(response, entity = None, additional_attr = {}):
    return {
        "model": 'not assigned' if entity is None else entity,
        "count": len(response),
        "brand": COMPANY,
        "data": response,
        **additional_attr,
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
            *payload,
        ]
        
        for item in items_response.json().get('value'):
            stock = item.get('ItemWarehouseInfoCollection')
            # print(stock)
            stock_fields = processFields(
                stock,
                STOCK_FIELDS.get('mapping'),
                )
            
            # streamData(s, STOCK_WEBHOOK_ID, prepareResponse(stock_fields, 'Stock'))
            # time.sleep(0.5)

        
        streamData(s, ITEMS_WEBHOOK_ID, prepareResponse(payload))

        next_link = items_response.json().get('odata.nextLink')
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
            PRICE_LIST_FIELDS.get('mapping'),
            PRICE_LIST_FIELDS.get('additional_fields')
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
                            'itemsGroupCode': item.get('itemsGroupCode'),
                            'manufacturer': item.get('manufacturer'),
                            'product_tmpl_id': item.get('default_code'),
                            'name': item.get('name'),
                            'currency_id': price.get('currency_id'),
                            'fixed_price': price.get('price', 0.0)
                        })
        
        
        streamData(s, PRICE_LISTS_WEBHOOK_ID, prepareResponse(payload, 'PriceLists'))

        next_link = price_list_response.json().get('odata.nextLink')
        if next_link is None:
            break
    return data

# handle client price lists data stream
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
                    streamData(s, PRICE_LISTS_WEBHOOK_ID, payload=prepareResponse(client_list, 'Client Price Lists'))
            break
        break
    
    return data

# process discount groups data
def processDiscountsRequest(s: requests, clients: list, price_lists: list):
    next_link = None
    update_clients = []
    client_price_lists = []
    i = 0
    MAX_ELEMENTS = len(clients)
    for index, client in enumerate(clients, 1):
        print(index)
        i = i + 1
        for list in price_lists:
            # if list['listId'] == 15:
            if client['list_id'] == list['listId'] and client['commerce_id'] == 'C022904':
                discount_exists=False
                data = []
                print(i)

                client_list = {
                    **list,
                    # "listId": f"{list['listId']}-C01101",
                    # "name": f"{list['name']} - Gerardo Vera Arroyo",
                    "listId": f"{list['listId']}-{client['commerce_id']}",
                    "name": f"{list['name']} - {client['name']}",
                    'lines': []
                }

                while True:
                    time.sleep(0.2)
                    response = listDiscountGroups(s, client['commerce_id'], client['groupCode'], next_link)
                    # response = listDiscountGroups(s, 'C01101', 114, next_link)

                    payload = processFields(
                        get_response(response),
                        DISCOUNT_GROUP_FIELDS.get('mapping'),
                    )

                    data = [
                        *data,
                        *payload,
                    ]

                    next_link = response.json().get('odata.nextLink')
                    if next_link is None:
                        break
                for item in list.get('lines'):
                    largest_discount = 0.0
                    for discount in data:
                        for discountLine in discount.get('discountGroupLine'):
                            if item['itemsGroupCode'] == discountLine['code'] and discountLine['type'] == 'dgboItemGroups':
                                largest_discount = discountLine['discount'] if discountLine['discount'] > largest_discount else largest_discount
                            if item['product_tmpl_id'] == discountLine['code'] and discountLine['type'] == 8:
                                largest_discount = discountLine['discount'] if discountLine['discount'] > largest_discount else largest_discount
                            if str(item['manufacturer']) == discountLine['code'] and discountLine['type'] == 'dgboManufacturer':
                                largest_discount = discountLine['discount'] if discountLine['discount'] > largest_discount else largest_discount
                    
                    final_price = item['fixed_price'] - ((item['fixed_price'] * largest_discount) / 100)
                    client_list['lines'].append({
                        **item,
                        'discount': largest_discount,
                        'final_price': final_price,
                    })
                    if largest_discount == 0:
                        print('no discount in here')
                    else:
                        discount_exists = True
                        print('there is a discount in here')
                print(discount_exists)
                if discount_exists:
                    client_price_lists.append(client_list)
                    update_clients.append({
                        **client,
                        'property_product_pricelist': f"{list['listId']}-{client['commerce_id']}"
                    })
                print(list)

            else:
                continue
        if i == 50 or index == MAX_ELEMENTS:
            print(index, MAX_ELEMENTS)

            i = 0
            if len(update_clients) > 0:
                streamData(s, CLIENTS_WEBHOOK_ID, prepareResponse(update_clients, 'Update Clients list'))
            if len(client_price_lists) > 0:
                streamData(s, DISCOUNT_WEBHOOK_ID, prepareResponse(client_price_lists, 'Discounts Price list'))
            print(update_clients)
            print(client_price_lists)
            update_clients = []
            client_price_lists = []
            time.sleep(0.5)
            # break

    # return data

def get_response(response: requests.Response):
    return response.json().get('value')

def processDistributionCenterRequest(s: requests):
    next_link = None
    data = []
    while True:
        response = listDistributionCenters(s, next_link)
        payload = processFields(
            get_response(response),
            STOCK_LOCATIONS_FIELDS.get('mapping'),
        )
        data = [
            *data,
            *payload,
        ]
        streamData(s, STOCK_LOCATIONS_WEBHOOK_ID, prepareResponse(payload, 'Distribution centers'))

        next_link = response.json().get('odata.nextLink')
        if next_link is None:
            break

    return data

handler()