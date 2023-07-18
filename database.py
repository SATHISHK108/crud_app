import pymysql.cursors
# Connect to the database
connection = pymysql.connect(host='34.172.125.208',
                             user='root',
                             password='crudapp',
                             database='crudapp',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `userdetails` (`username`, `email`, `password_`, `phone_number`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, ('sathish', 'sathishkandaswamy108@python.org', 'crudapp', 7904546465))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
    print('connection and record created successfully')