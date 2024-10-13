#zum einmaligen Ausführen

import components.servercomponents.pythonfastapi.builder as builder

PYTHONFASTAPI_DIRECTORY = 'components/servercomponents/pythonfastapi/'

builder.build([{'filename': PYTHONFASTAPI_DIRECTORY + 'fastapi-main.py', 'params': {}},
       {'filename': PYTHONFASTAPI_DIRECTORY + 'cors.py', 'params': {'!!allow_origins!!': '*', '!!allow_methods!!': '*', '!!allow_headers!!': '*'}},
       {'filename': PYTHONFASTAPI_DIRECTORY + 'helloworld.py', 'params': {'!!path!!': 'helloworld'}},
       {'filename': PYTHONFASTAPI_DIRECTORY + 'postgresqlconnection.py', 'params': {'!!db_name!!': 'mydb', '!!db_host!!': 'localhost', '!!db_user!!': 'postgres', '!!db_pass!!': 'abc', '!!db_port!!': '5432'}},
       {'filename': PYTHONFASTAPI_DIRECTORY + 'postgresqlquery.py', 'params': {'!!method!!': 'get', '!!path!!': 'tags', '!!url_params!!': '', '!!method_name!!': 'getTags', '!!params!!': '', '!!query!!': 'select * from tags order by id'}}], 'sample-server.py')