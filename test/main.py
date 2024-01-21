from alert import Alert
from object import prediction


class Test:
    alert: Alert

    def __init__(self):
        self.nb_alert = 5
        print("Launch test")
        self.alert = Alert(prediction)
        self.alert.run()
        if self.alert.get_number_alerts() == self.nb_alert:
            print("Test success")
        else:
            print("Test failed")


if __name__ == '__main__':
    Test()
