class Zone:

    def __init__(self, city: str, mydb):
        self.city: str = city
        self.mydb = mydb

    def get_zone_orange(self):
        cursor = self.mydb.cursor()
        cursor.execute('select x1, x2, y1, y2 from line '
                       'where ville = %s and type=1', (self.city,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_zone_red(self):
        cursor = self.mydb.cursor()
        cursor.execute('select x1, x2, y1, y2 from line '
                       'where ville = %s and type=2', (self.city,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_zone_green(self):
        cursor = self.mydb.cursor()
        cursor.execute('select x1, x2, y1, y2 from line '
                       'where ville = %s and type=3', (self.city,))
        result = cursor.fetchall()
        cursor.close()
        return result
