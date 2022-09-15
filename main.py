import sys
import driveApp.app as yandex_drive_application
import logging


def main():

    sys.setrecursionlimit(50000)
    yandex_drive_application.run()


if __name__ == '__main__':
    main()
