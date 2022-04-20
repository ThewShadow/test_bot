import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 65432))
sock.listen()

class User:
    def __init__(self, id):
        self.id = id
        self.geo = None
        self.img = None
        self.text = None

    def __str__(self):
        return str([self.id, self.geo, self.text])

    def set_attr(self, **kwargs):
        if 'geo' in kwargs:
            self.geo = kwargs['geo']
        if 'img' in kwargs:
            self.geo = kwargs['img']
        if 'text' in kwargs:
            self.geo = kwargs['text']

    def get_attr(self):
        return [self.id, self.geo, self.img, self.text]


class DarkBox:
    elements = []

    def push(self, e):
        DarkBox.elements.append(e)
        print(f'elements in DarkBox: {DarkBox.elements}')

    def get_user(self, id):
        for usr in DarkBox.elements:
            if hasattr(usr, 'id') and usr.id == id:
                return usr

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    darkbox = DarkBox()
    new_user = User('124323')
    darkbox.push(new_user)

    while True:
        print('socket listening')
        conn, addr = sock.accept()
        with conn:
            value = b''
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                value += data
            conn.close()
            value = value.decode('utf-8').strip()
            usr = darkbox.get_user('124323')
            usr.set_attr(geo=value)
            print(usr)

