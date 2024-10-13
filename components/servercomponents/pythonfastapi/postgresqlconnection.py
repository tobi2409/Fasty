import psycopg2

postgresql_connection = psycopg2.connect(database="!!db_name!!",
                                   host="!!db_host!!",
                                   user="!!db_user!!",
                                   password="!!db_pass!!",
                                   port="!!db_port!!")

postgresql_cursor = postgresql_connection.cursor()
