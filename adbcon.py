from ppadb.client import Client as AdbCl
def conn():
    client = AdbCl(host='127.0.0.1', port=5037)
    print(client.port)
    dev = client.create_connection(timeout=3000)
    dev.connect()
