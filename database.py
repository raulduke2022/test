from peewee import *
from datetime import date


db = SqliteDatabase('people.db')

class Data(Model):
    requestTime = CharField(null = True)
    dcExpirationDate = CharField(null = True)
    pointAddress = CharField(null = True)
    chassis = CharField(null = True)
    operatorName = IntegerField(null = True)
    odometerValue = IntegerField(null = True)
    dcNumber = IntegerField(null = True)
    model = CharField(null = True)
    brand = CharField(null = True)

    class Meta:
        database = db # This model uses the "people.db" database.

db.connect()
db.create_tables([Data])
db.close()


