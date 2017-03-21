#__Author__:oliver
#__DATE__:3/8/17
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.path.join(BASE_DIR)

from src.run import client


if __name__ == '__main__':
    client()