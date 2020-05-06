#start the mongodb server
screen -S mongod -dm mongod --dbpath /usr/local/var/mongodb

#start the mongodb tweet fetcher
screen -S fetch_tweets -dm python3.7 fetch_tweets.py

#Create schema and tables
python3.7 initialise_mysql_db.py

#start mongo to sql conversion
screen -S mongo_to_sql -dm python3.7 mongo_to_sql.py



#start the visualisation notebook
jupyter notebook




#If you want to delete the twitter sql data
drop database twitterdb;

#If you want to delete collection 
db.tweets_staging.drop()


 
 
 
 