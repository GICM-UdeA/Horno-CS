import serial
import time

def main():

    print('hola')

    SerialPort = "COM15"

    try:
        dev = serial.Serial(SerialPort, 115200, timeout=1)
        dev.close()
        dev.open()
        dev.flushInput()
        dev.flushOutput()

        while dev.in_waiting == 0:
            dev.write(str.encode("e"))
            print(dev.in_waiting)
            time.sleep(2)
        print("salio")
        print(dev.in_waiting)
        print("flush")
        # dev.flushInput()
        # print(dev.in_waiting)
        data = dev.readline().decode()

        print(data)

    except Exception as error:
        print(error)

    except KeyboardInterrupt:
        dev.close()

    finally:
        dev.close()


if __name__ == '__main__':
    main()
