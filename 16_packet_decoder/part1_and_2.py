#!/usr/bin/env python3

from functools import partial
from itertools import chain
from math import prod
from operator import attrgetter, eq, gt, lt
from pathlib import Path
from typing import NamedTuple

PACKET_VERSION_LENGTH = PACKET_TYPE_LENGTH = 3
PACKET_DIGIT_LENGTH = 5

SUB_PACKET_TYPE_LENGTH = 1
SUB_PACKET_LENGTH = 15
SUB_PACKET_CHILDREN_COUNT_LENGTH = 11

MIN_PACKET_SIZE = PACKET_VERSION_LENGTH + PACKET_TYPE_LENGTH + PACKET_DIGIT_LENGTH

PACKET_TYPE_LITERAL_NUMBER = 4
PACKET_TYPE_TO_OPERATOR = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: lambda values: int(gt(*values)),
    6: lambda values: int(lt(*values)),
    7: lambda values: int(eq(*values)),
}


class Packet(NamedTuple):
    version: int
    type_id: int
    payload: int | list["Packet"]


flatten = chain.from_iterable
bin_to_int = partial(int, base=2)


def hex_to_bits(hex):
    width = len(hex) * 4
    return f"{int(hex, 16):0{width}b}"


def read(data, start, length):
    end = start + length
    chunk = data[start:end]
    return chunk, end


def parse(hex_data):
    bits = hex_to_bits(hex_data)
    packets, _ = parse_bin(bits)
    return packets


def parse_bin(bits, max_packets=float("inf")):
    read_bits = partial(read, bits)
    packets = []
    pointer = 0
    end = len(bits)
    while (pointer <= end - MIN_PACKET_SIZE) and (len(packets) < max_packets):
        version, pointer = read_bits(pointer, PACKET_VERSION_LENGTH)
        type_id, pointer = read_bits(pointer, PACKET_TYPE_LENGTH)
        version, type_id = bin_to_int(version), bin_to_int(type_id)

        if type_id == PACKET_TYPE_LITERAL_NUMBER:  # Literal number
            parts = []
            while True:
                raw, pointer = read_bits(pointer, PACKET_DIGIT_LENGTH)
                is_last = raw[0] == "0"
                parts.append(raw[1:])
                if is_last:
                    break
            value = bin_to_int("".join(parts))

        else:  # Operator
            sub_packet_type, pointer = read_bits(pointer, SUB_PACKET_TYPE_LENGTH)

            if sub_packet_type == "0":
                raw, pointer = read_bits(pointer, SUB_PACKET_LENGTH)
                sub_packet_length = bin_to_int(raw)
                raw, pointer = read_bits(pointer, sub_packet_length)
                value, _ = parse_bin(raw)

            elif sub_packet_type == "1":
                raw, pointer = read_bits(pointer, SUB_PACKET_CHILDREN_COUNT_LENGTH)
                sub_packets_count = bin_to_int(raw)
                value, remainder = parse_bin(
                    bits[pointer:], max_packets=sub_packets_count
                )
                pointer = end - len(remainder)

            else:
                raise ValueError("Unknown sub packet type")

        packet = Packet(version, type_id, value)
        packets.append(packet)

    return packets, bits[pointer:]


def get_versions_sum(data):
    packets = parse(data)
    return _get_versions_sum(packets)


def _get_versions_sum(packets):
    top_level_versions = sum(map(attrgetter("version"), packets))

    nested_packets = list(
        flatten(
            map(
                attrgetter("payload"),
                filter(
                    lambda packet: packet.type_id != PACKET_TYPE_LITERAL_NUMBER,
                    packets,
                ),
            )
        )
    )
    nested_level_versions_sum = (
        _get_versions_sum(nested_packets) if nested_packets else 0
    )

    return top_level_versions + nested_level_versions_sum


def evaluate_expression(data):
    packets = parse(data)
    assert len(packets) == 1
    return evaluate_sub_expression(packets[0])


def evaluate_sub_expression(packet):
    values = [
        sub_packet.payload
        if sub_packet.type_id == PACKET_TYPE_LITERAL_NUMBER
        else evaluate_sub_expression(sub_packet)
        for sub_packet in packet.payload
    ]
    fn = PACKET_TYPE_TO_OPERATOR[packet.type_id]
    return fn(values)


if __name__ == "__main__":
    example_literal_number_packet = "D2FE28"
    assert hex_to_bits(example_literal_number_packet) == "110100101111111000101000"
    assert parse(example_literal_number_packet) == [(6, 4, 2021)]

    example_operator_packet = "38006F45291200"
    assert (
        hex_to_bits(example_operator_packet)
        == "00111000000000000110111101000101001010010001001000000000"
    )
    assert parse(example_operator_packet) == [(1, 6, [(6, 4, 10), (2, 4, 20)])]

    example_operator_packet = "EE00D40C823060"
    assert (
        hex_to_bits(example_operator_packet)
        == "11101110000000001101010000001100100000100011000001100000"
    )
    assert parse(example_operator_packet) == [(7, 3, [(2, 4, 1), (4, 4, 2), (1, 4, 3)])]

    example_nested_operators = "8A004A801A8002F478"
    assert parse(example_nested_operators) == [(4, 2, [(1, 2, [(5, 2, [(6, 4, 15)])])])]

    assert get_versions_sum("8A004A801A8002F478") == 16
    assert get_versions_sum("620080001611562C8802118E34") == 12
    assert get_versions_sum("C0015000016115A2E0802F182340") == 23
    assert get_versions_sum("A0016C880162017C3686B18A3D4780") == 31

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    versions_sum = get_versions_sum(input_data[0])
    print(f"{versions_sum=}")

    assert evaluate_expression("C200B40A82") == 3
    assert evaluate_expression("04005AC33890") == 54
    assert evaluate_expression("880086C3E88112") == 7
    assert evaluate_expression("CE00C43D881120") == 9
    assert evaluate_expression("D8005AC2A8F0") == 1
    assert evaluate_expression("F600BC2D8F") == 0
    assert evaluate_expression("9C005AC2F8F0") == 0
    assert evaluate_expression("9C0141080250320F1802104A08") == 1

    expression_result = evaluate_expression(input_data[0])
    print(f"{expression_result=}")
