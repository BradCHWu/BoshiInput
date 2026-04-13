import os
import json


def get_ovalue(start, i, bytes_data):
    nbit = 2
    byte = bytes_data[start + (i * nbit) // 8]
    shift = 8 - nbit - (i * nbit % 8)
    ovalue = byte >> shift
    return ovalue & ((1 << nbit) - 1)


def get_bits(start, i, bytes_data):
    nbyte = 3
    value = 0
    a = start + i * nbyte
    for _ in range(nbyte):
        value = (value << 8) | bytes_data[a]
        a += 1
    return value


def main(filename):
    try:
        with open(filename, "rb") as f:
            bytes_data = list(f.read())
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return

    i1 = int.from_bytes(bytes_data[0:2], "little")
    i2 = i1 + int.from_bytes(bytes_data[2:4], "little")
    i3 = i2 + int.from_bytes(bytes_data[6:8], "little")
    i4 = i3 + int.from_bytes(bytes_data[6:8], "little")

    rootkey = list(" abcdefghijklmnopqrstuvwxyz,.'[]")

    output_dict = {}
    for i in range(1024):
        k0 = rootkey[i // 32]
        k1 = rootkey[i % 32]

        if k0 == " ":
            continue

        start_ci = int.from_bytes(bytes_data[i * 2 : i * 2 + 2], "little")
        end_ci = int.from_bytes(bytes_data[i * 2 + 2 : i * 2 + 4], "little")

        for ci in range(start_ci, end_ci):
            bit24 = get_bits(i4, ci, bytes_data)
            hi = get_ovalue(i1, ci, bytes_data)
            lo = bit24 & 0x3FFF

            k2 = rootkey[bit24 >> 19]
            k3 = rootkey[(bit24 >> 14) & 0x1F]

            full_key = (k0 + k1 + k2 + k3).strip()

            char = chr((hi << 14) | lo)

            if full_key not in output_dict:
                output_dict[full_key] = []
            output_dict[full_key].append(f"{char}")

    abs_file = os.path.abspath(filename)
    out_file = os.path.splitext(abs_file)[0] + ".json"
    with open(out_file, "w", encoding="utf-8") as ofile:
        json.dump(output_dict, ofile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    for name in os.scandir("./"):
        if os.path.splitext(name.path)[-1] != ".tab":
            continue
        print(f"Process {name.path}")
        main(name.path)
