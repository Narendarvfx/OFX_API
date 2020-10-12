# import json
# import websocket
# import redis
# import requests
# import random, time
#
# def w_connect():
#     ws=websocket.WebSocket()
#
#     ws.connect("ws://localhost:8000/ws/projects/", http_proxy_host="127.0.0.1", http_proxy_port=8000)
#     #
#     # for i in range(1000):
#     #     time.sleep(3)
#     #     ws.send(json.dumps({'value': random.randint(1, 100)}))
#
#
# if __name__ == '__main__':
#     w_connect()