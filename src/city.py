class City:
    def __init__(self, db):
        self.mydb = db

    def return_city(self) -> list[list[str | float]]:
        cursor = self.mydb.cursor()
        cursor.execute('select NAME, latitude, longitude,ip,'
                       'name_ip, password_ip from CITY')
        result = cursor.fetchall()
        cursor.close()
        print(result)
        return result
