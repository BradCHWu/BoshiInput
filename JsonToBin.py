import json
import zlib


def _get_ovalue(start, i, bytes_data):
    nbit = 2
    byte = bytes_data[start + (i * nbit) // 8]
    shift = 8 - nbit - (i * nbit % 8)
    ovalue = byte >> shift
    return ovalue & ((1 << nbit) - 1)


def _get_bits(start, i, bytes_data):
    nbyte = 3
    value = 0
    a = start + i * nbyte
    for _ in range(nbyte):
        value = (value << 8) | bytes_data[a]
        a += 1
    return value


def TabtoJson(tab_file: str, json_file: str) -> None:
    try:
        with open(tab_file, "rb") as f:
            bytes_data = list(f.read())
    except FileNotFoundError:
        print(f"Error: {tab_file} not found.")
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
            bit24 = _get_bits(i4, ci, bytes_data)
            hi = _get_ovalue(i1, ci, bytes_data)
            lo = bit24 & 0x3FFF

            k2 = rootkey[bit24 >> 19]
            k3 = rootkey[(bit24 >> 14) & 0x1F]

            full_key = (k0 + k1 + k2 + k3).strip()

            char = chr((hi << 14) | lo)

            if full_key not in output_dict:
                output_dict[full_key] = []
            output_dict[full_key].append(f"{char}")

    with open(json_file, "w", encoding="utf-8") as ofile:
        json.dump(output_dict, ofile, indent=4, ensure_ascii=False)


def JsonToBinFile(json_data: str, bin_file: str) -> None:
    with open(bin_file, "wb", encoding="utf-8") as ofile:
        compressed = zlib.compress(json_data.encode())
        ofile.write(compressed)


def JsonFileToBinFile(json_file: str, bin_file: str) -> None:
    with open(json_file, encoding="utf-8") as ifile:
        data = json.load(ifile)
    JsonToBinFile(data, bin_file)


def BinFileToJson(bin_file: str) -> dict:
    with open(bin_file, "rb") as ifile:
        compressed = ifile.read()
    decompressed = zlib.decompress(compressed)
    json_string = decompressed.decode()
    return json.loads(json_string)


def BinFileToJsonFile(bin_file: str, json_file: str) -> None:
    json_data = BinFileToJson(bin_file)
    with open(json_file, "w", encoding="utf-8") as ofile:
        json.dump(json_data, ofile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    TabtoJson("liu-uni.tab")
    JsonFileToBinFile("liu.json", "liu.bin")
    BinFileToJsonFile("liu.bin", "liu.json")
