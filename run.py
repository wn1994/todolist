from net_setting import *
from app import create_app
# import config

app = create_app()

if __name__ == '__main__':
    app.run(host=DEV_HOST, port=DEV_PORT)
