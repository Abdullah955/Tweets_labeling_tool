import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///users.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

#user = User("admin", "password")

 user = User("user1" , "123")
 session.add(user)
#
# user = User("user2" , "123")
# session.add(user)
#
# user = User("user3" , "123")
# session.add(user)
#
# user = User("user4" , "123")
# session.add(user)
#
# session.commit()


# select all users
result = engine.execute('SELECT * FROM "users"')
session.commit()
for _r in result:
   print (_r)

# delete specific row
#session.query(User).filter_by(username='admin').delete()

# delete all rows
# engine.execute('DELETE FROM "users"')
# result = engine.execute('SELECT * FROM "users"')
# print(result.fetchall())


# commit the record the database
session.commit()

