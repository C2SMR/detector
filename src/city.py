from datetime import date, timedelta, datetime
from decimal import Decimal

import mysql.connector


class City:
    mydb: mysql.connector.connection.MySQLConnection
    detector_id: int

    def __init__(self, db, detector_id: int):
        self.mydb = db
        self.detector_id = detector_id

    def return_city(self) -> list[tuple[float |
                                        int | Decimal | str | bytes | date |
                                        timedelta | datetime | set[str] |
                                        bool | None, ...]]:
        cursor = self.mydb.cursor()
        cursor.execute('select NAME, '
                       'latitude, '
                       'longitude,ip,'
                       'name_ip, '
                       'password_ip,'
                       'blur,'
                       'run_detection,'
                       'type_detection, '
                       'launch_detection,'
                       'stop_detection from CITY '
                       'where detector_id = %s', (self.detector_id,))
        result = cursor.fetchall()
        print(result)
        return result