import copy
import random


CODES_COUNT = 256
ROTORS_COUNT = 3

CODES = [code for code in range(CODES_COUNT)]


def get_rotor():
    rotor = CODES.copy()
    random.shuffle(rotor)
    return rotor


def get_reflector():
    codes_copy = CODES.copy()
    reflector = [None for _ in range(CODES_COUNT)]
    for i in range(CODES_COUNT):
        if reflector[i] is None:
            codes_copy.remove(i)
            code = random.choice(codes_copy)
            codes_copy.remove(code)
            reflector[i] = code
            reflector[code] = i
    return reflector


def go_through_rotor(code, rotor):
    return rotor[code]


def go_through_rotor_backwards(code, rotor):
    return rotor.index(code)


def shift_rotor(rotor):
    rotor.append(rotor.pop(0))


def go_through_mechanism(code, rotors, reflector):
    for rotor in rotors:
        code = go_through_rotor(code, rotor)
    code = go_through_rotor(code, reflector)
    for rotor in reversed(rotors):
        code = go_through_rotor_backwards(code, rotor)
    return code


class Enigma:
    _rotors = [get_rotor() for _ in range(ROTORS_COUNT)]
    _reflector = get_reflector()
    _shift = 0

    def __init__(self):
        self.rotors = copy.deepcopy(Enigma._rotors)
        self.reflector = copy.deepcopy(Enigma._reflector)
        self.shift = 0

    def encrypt(self, code):
        encrypted_code = go_through_mechanism(
            code, self.rotors, self.reflector
        )
        self.shift += 1
        for i, rotor in enumerate(self.rotors):
            if self.shift % CODES_COUNT ** i == 0:
                shift_rotor(rotor)
        return encrypted_code
