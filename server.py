import models.dbRequests
from socket import *
import json
from threadings import ThreadWithReturnValue


class Server:
    def __init__(self):
        self.server_db = models.dbRequests.ServerDB()
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('localhost', 9091))
        self.sock.listen(3)

    def start_server(self):
        while True:
            user, addr = self.sock.accept()
            print(f"Client connected:\nIP:{addr[0]}\nPORT:{addr[1]}")
            self.listener(user)

    def sender(self, user, message_type, message):
        message = {"type": message_type, "message": message}
        user.send(json.dumps(message).encode('utf-8'))

    def listener(self, user):
        is_work = True

        while is_work:
            data = {}

            try:
                data = json.loads(user.recv(1024))
            except Exception as e:
                print(e)
                data = ''
                is_work = False

            if len(data) > 0:

                if data["type"] == "disconnect":
                    user.close()

                elif data["type"] == "check register":
                    register_thread = ThreadWithReturnValue(target=self.server_db.checkRegister,
                                                            args=(data["message"], ))
                    register_thread.start()
                    message = register_thread.join()
                    self.sender(user, "check register", message)

                elif data["type"] == "check user":
                    check_thread = ThreadWithReturnValue(target=self.server_db.checkUser,
                                                         args=(data["message"][0],
                                                               data["message"][1], ))
                    check_thread.start()
                    message = check_thread.join()
                    self.sender(user, "check user", message)

                elif data["type"] == "add new user":
                    add_user_thread = ThreadWithReturnValue(target=self.server_db.addNewUser,
                                                            args=(data["message"][0], data["message"][1],
                                                                  data["message"][2], ))
                    add_user_thread.start()

                elif data["type"] == "test new strategy":
                    test_strategy_thread = ThreadWithReturnValue(target=self.server_db.testNewStrategy,
                                                                 args=(data["message"], ))
                    test_strategy_thread.start()

                elif data["type"] == "update strategies":
                    update_thread = ThreadWithReturnValue(target=self.server_db.getStrategiesWithTests,
                                                          args=(data["message"], ))
                    update_thread.start()
                    message = update_thread.join()
                    self.sender(user, "update strategies", message)

                elif data["type"] == "connect to market":
                    message = self.server_db.checkMarketData(data["message"][0], data["message"][1], data["message"][2])
                    # market_thread = ThreadWithReturnValue(target=self.server_db.checkMarketData,
                    #                                       args=(data["message"][0], data["message"][1],
                    #                                             data["message"][2],))
                    # market_thread.start()
                    # message = market_thread.join()
                    self.sender(user, "connect to market", message)

                elif True:
                    pass

                data = ""

            else:
                print("Disconnected")
                is_work = False


if __name__ == '__main__':
    Server().start_server()
