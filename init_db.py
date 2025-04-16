import os
import psycopg2
from dotenv import load_dotenv, dotenv_values
load_dotenv()
# Connect to database
conn = psycopg2.connect(
    host = "drhscit.org",
    database = os.getenv('DB'),
    user = os.getenv('DB_UN'),
    password = os.getenv('DB_PW')
)

# Open a cursor to perform database operations
# cur = conn.cursor()

# # Create a new table for reviews
# # cur.execute('DROP TABLE IF EXISTS book_reviews;')
# # cur.execute('CREATE TABLE book_reviews (id integer generated always as identity primary key, title varchar(150) not null, author varchar(50) not null, page_count integer, review text, date_added date default current_date)')

# # From Exploration: Insert data

# # cur.execute('INSERT INTO reviews(name, review, rating)' 
#             'VALUES (%s, %s, %s)',
#             ('Fox Mulder','Loved the pizza!', 5)
#             )

# # cur.execute('INSERT INTO reviews(name, review, rating)' 
#             'VALUES (%s, %s, %s)',
#             ('Xavier File','Great dessert choices!', 4)
#             )


# # Commit the transaction to save the changes
# # conn.commit()


# # From exploration: Select data


# cur.execute('SELECT * FROM reviews WHERE name = %s', ('Fox Mulder',))
# results = cur.fetchall()
# print(results)



# #Close the cursor and connection
# cur.close()
# conn.close()
