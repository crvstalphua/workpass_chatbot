#### Connection to AWS RDS - MySQL DB

import mysql.connector
from datetime import datetime
import pytz

# local modules
from constants import (
    AWS_RDS_PASSWORD,
    AWS_RDS_ENDPOINT
)

# Establish a connection to the database
def create_connection():
    connection = mysql.connector.connect(
        host=AWS_RDS_ENDPOINT,
        user="admin",
        password=AWS_RDS_PASSWORD,
        database="chatbotdb"
    )
    return connection

# Create a sample table
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS qna(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        time_enquired VARCHAR(255),
                        queryid VARCHAR(255),
                        resultids MEDIUMTEXT,
                        question VARCHAR(255),
                        answer VARCHAR(255),
                        source_doc MEDIUMTEXT,
                        chat_history MEDIUMTEXT
                   )''')

# Insert a record
def insert_record(connection, queryid, resultids, question, answer, source_doc, chat_history):
    cursor = connection.cursor()
    now = datetime.strftime(datetime.now(pytz.timezone('Asia/Singapore')), "%Y-%m-%d %H:%M:%S")
    sql_query = "INSERT INTO qna (time_enquired, queryid, resultids, question, answer, source_doc, chat_history) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    print(sql_query)
    cursor.execute(sql_query, (now, queryid, str(resultids), question, answer, str(source_doc), str(chat_history)))
    connection.commit()

# Drop table
def drop_table(connection):
    cursor = connection.cursor()
    sql_query = "DROP TABLE IF EXISTS chatbotdb.qna;"
    cursor.execute(sql_query)
    connection.commit()

# Select records
def select_records(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM qna")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Update a record
def update_record(connection, name, age, id):
    cursor = connection.cursor()
    query = "UPDATE sample SET name = %s, age = %s WHERE id = %s"
    cursor.execute(query, (name, age, id))
    connection.commit()

# Delete a record
def delete_record(connection, id):
    cursor = connection.cursor()
    query = "DELETE FROM sample WHERE id = %s"
    cursor.execute(query, (id,))
    connection.commit()

# Insert multiple records
def insert_multiple_records(connection, records):
    cursor = connection.cursor()
    query = "INSERT INTO sample (name, age) VALUES (%s, %s)"
    cursor.executemany(query, records)
    connection.commit()