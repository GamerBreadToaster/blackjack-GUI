import mysql.connector
from players import Player

def save(data: Player):
    mydb = mysql.connector.connect(
        host="82.72.20.179:2000",
        user="python",
        password="GamerBreadToaster3!",
        database="mydatabase"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO User (, address) VALUES (%s, %s)"
    val = ("John", "Highway 21")
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")