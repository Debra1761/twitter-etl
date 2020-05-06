#Download driver from https://dev.mysql.com/downloads/connector/python/

#pip install mysql-connector-python

#start daemon
#sudo /usr/local/mysql/bin/mysqld_safe

#create database twitterdb
#

#to enter into the terminal
#/usr/local/mysql/bin/mysql -u root -p
#/usr/local/mysql/bin/mysqld --user=_mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data --plugin-dir=/usr/local/mysql/lib/plugin --log-error=/usr/local/mysql/data/mysqld.local.err --pid-file=/usr/local/mysql/data/mysqld.local.pid --keyring-file-data=/usr/local/mysql/keyring/keyring --early-plugin-load=keyring_file=keyring_file.so


import mysql.connector
from mysql.connector import Error
from pymongo import MongoClient
import time

from transformations import clean_tweets, preprocess, sentiment




while True:
    print('starting sql dump loop...')
    myclient = MongoClient()
    mydb = myclient["tweetbase"]
    staging_col = mydb["tweets_staging"]


    cursor = staging_col.find({})



    con = mysql.connector.connect(host='127.0.0.1',
                                          database='twitterdb',
                                          user='root',
                                          password='debra1761',
                                          charset='utf8',
                                          auth_plugin='mysql_native_password')

    for document in cursor:

        document['text'] = clean_tweets(document['text'])
        document['text'] = preprocess(document['text'])
        document['sentiment'] = sentiment(document['text'])

        if 'created_at' in document:
            try:
                if con.is_connected():
                    """
                    Insert twitter data
                    """


                    if document['user']:
                        cursor = con.cursor()
                        query = "INSERT INTO user (user_id, user_created_at, screen_name, friends_count, statuses_count, followers_count) VALUES (%s, %s, %s, %s, %s, %s)"
                        cursor.execute(query, (
                        document['user']['id'], document['user']['created_at'], document['user']['screen_name'], document['user']['friends_count'], document['user']['statuses_count'], document['user']['followers_count']))
                        con.commit()
                        cursor.close()

                    if document['place']:
                        cursor = con.cursor()
                        query = "INSERT INTO place (place_id, country, place_type, full_name) VALUES (%s, %s, %s, %s)"
                        cursor.execute(query, (
                        document['place']['id'], document['place']['country'], document['place']['place_type'], document['place']['full_name']))
                        con.commit()
                        cursor.close()


                    if document['user']:
                        if document['place']:
                            cursor = con.cursor()
                            query = "INSERT INTO tweet (id, created_at, source, text, user_id, place_id, sentiment) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(query, (document['id'], document['created_at'], document['source'], document['text'], document['user']['id'], document['place']['id'], document['sentiment']))
                            con.commit()
                            cursor.close()
                        else:
                            cursor = con.cursor()
                            query = "INSERT INTO tweet (id, created_at, source, text, user_id, sentiment) VALUES (%s, %s, %s, %s, %s, %s)"
                            cursor.execute(query, (document['id'], document['created_at'], document['source'], document['text'], document['user']['id'], document['sentiment']))
                            con.commit()
                            cursor.close()



                    # query = "INSERT INTO place (place_id, country, full_name) VALUES (%s, %s, %s)"
                    # cursor.execute(query, (document['place']['place']['id'], document['user']['name'], document['text']))




            except Error as e:
                print(e)

        result = staging_col.delete_one({"_id": document['_id']})

    con.close()
    print('done.')
    print('sleeping..')
    time.sleep(100)
