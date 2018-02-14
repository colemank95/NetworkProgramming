import Client_Start_Point
import sys

if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print ('Incorrect arguments. usage: python client.py hostname port')
        sys.exit()
    Client_Start_Point.main(sys.argv[1], int(sys.argv[2]))
