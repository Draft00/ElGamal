# -*- coding: UTF-8 -*-

import asn1


def encode(
    b, # public key
    p, # prime
    a, # generator
    a_y, c, # (a^y, c)
    cipher_length, 
    cipher_text
    ):

    asn1_encoder = asn1.Encoder()

    asn1_encoder.start()

    # Sequence_1 start
    asn1_encoder.enter(asn1.Numbers.Sequence)

    # Set_1 start
    asn1_encoder.enter(asn1.Numbers.Set)

    # Sequence_2 start
    asn1_encoder.enter(asn1.Numbers.Sequence)

    # \x80\x01\x02\x01 - ElGamal encryption with open key, f(m, b^y) = m * b^y (mod p)
    # \x80\x01\x02\x02 - ElGamal encryption with open key, f(m, b^y) = m + b^y (mod p)
    # \x80\x01\x02\x03 - ElGamal encryption with open key, f(m, b^y) = m - b^y (mod p)
    asn1_encoder.write(b'\x80\x01\x02\x03', asn1.Numbers.OctetString)
    asn1_encoder.write(b'ElGamal encryption with open key, f(m, b^y) = m - b^y (mod p)', asn1.Numbers.UTF8String)

    #
    asn1_encoder.enter(asn1.Numbers.Sequence)
    # b - public key
    asn1_encoder.write(b, asn1.Numbers.Integer)
    asn1_encoder.leave()

    # Cryptographic parameters
    asn1_encoder.enter(asn1.Numbers.Sequence)
    # p - prime
    asn1_encoder.write(p, asn1.Numbers.Integer)
    # a - generator
    asn1_encoder.write(a, asn1.Numbers.Integer)
    asn1_encoder.leave()

    # (a^y, c)
    asn1_encoder.enter(asn1.Numbers.Sequence)
    # a_y - a^y
    asn1_encoder.write(a_y, asn1.Numbers.Integer)
    # c - cipher 
    asn1_encoder.write(c, asn1.Numbers.Integer)
    asn1_encoder.leave()

    # Sequence_2 end
    asn1_encoder.leave()

    # Set_1 end
    asn1_encoder.leave()

    #
    asn1_encoder.enter(asn1.Numbers.Sequence)
    # \x01\x32 - 3DES
    asn1_encoder.write(b'\x01\x32', asn1.Numbers.OctetString)
    asn1_encoder.write(cipher_length, asn1.Numbers.Integer)
    asn1_encoder.leave()

    # Sequence_1 end
    asn1_encoder.leave()

    asn1_encoder.write(cipher_text)

    return asn1_encoder.output()


def decode(filename):

    decoded_parameters = []

    with open(filename, 'rb') as file:
        data = file.read()
        decoder = asn1.Decoder()
        decoder.start(data)
        decoded_parameters = parse(decoder, decoded_parameters)
        data = bytearray(data)
        cipher_len = decoded_parameters[-1]
        cipher_bytes = bytearray()

        for i in range(len(data) - cipher_len, len(data)):
            cipher_bytes.append(data[i])

        with open('~tmp', 'wb') as file_cipher:
            file_cipher.write(cipher_bytes)

    return decoded_parameters[0], decoded_parameters[1], decoded_parameters[2], decoded_parameters[3], decoded_parameters[4], decoded_parameters[5], 
    # b 
    # p
    # a
    # a^y
    # c
    # cipher_len


def parse(file, decoded_values):

    while not file.eof():
        try:
            tag = file.peek()

            if tag.nr == asn1.Numbers.Null:
                break

            if tag.typ == asn1.Types.Primitive:
                tag, value = file.read()

                if tag.nr == asn1.Numbers.Integer:
                    decoded_values.append(value)

            else:
                file.enter()
                decoded_values = parse(file, decoded_values)
                file.leave()

        except asn1.Error:
            break

    return decoded_values


