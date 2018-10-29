from enigma import Enigma


def main():
    enigma1 = Enigma()
    enigma2 = Enigma()
    while True:
        filename = input(
            'Введите имя входного файла: '
        )
        outputname = input(
            'Введите имя выходного файла: '
        )
        num = input(
            'Какую энигму использовать?\n'
            '1 - зашифровать\n'
            '2 - дешифровать\n'
            ': '
        )
        file = open(filename, 'rb')
        text = file.readlines()
        output = open(outputname, 'wb')
        file.close()
        if num == '1':
            for line in text:
                output.write(bytes(enigma1.encrypt(code) for code in line))
        elif num == '2':
            for line in text:
                output.write(bytes(enigma2.encrypt(code) for code in line))
        output.close()


if __name__ == '__main__':
    main()
