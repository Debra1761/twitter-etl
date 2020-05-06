import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="debra1761"
)

mycursor = mydb.cursor()

try:
    mycursor.execute("CREATE DATABASE twitterdb")
    mycursor.execute("USE twitterdb")
except:
    print('failed to create database.')
    pass


#Dimension tables
mycursor.execute("""CREATE TABLE user 
(user_id double NOT NULL PRIMARY KEY, 
user_created_at VARCHAR(255), 
screen_name VARCHAR(255), 
friends_count VARCHAR(255),
statuses_count VARCHAR(255),
followers_count VARCHAR(255))""")

mycursor.execute("""CREATE TABLE place 
(place_id varchar(255) NOT NULL PRIMARY KEY, 
country VARCHAR(255), 
place_type VARCHAR(255),
full_name VARCHAR(255))""")


#Fact table
mycursor.execute("""CREATE TABLE tweet 
(id double NOT NULL PRIMARY KEY, 
created_at VARCHAR(255),
source VARCHAR(255), 
text VARCHAR(255),
sentiment int,

user_id double,
place_id varchar(255),

FOREIGN KEY(user_id) REFERENCES user(user_id),
FOREIGN KEY(place_id) REFERENCES place(place_id))
""")




print('created fact and dimension tables.')