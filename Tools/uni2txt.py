import os
import json


def get_int16(addr, bytes_data):
    return bytes_data[addr] | (bytes_data[addr + 1] << 8)


def get_bits(start, nbit, i, bytes_data):
    if nbit in [1, 2, 4]:
        idx = int(start + (i * nbit) // 8)
        byte = bytes_data[idx]
        shift = 8 - nbit - (i * nbit % 8)
        ovalue = byte >> shift
        return ovalue & ((1 << nbit) - 1)
    elif nbit > 0 and nbit % 8 == 0:
        nbyte = nbit // 8
        value = 0
        a = int(start + i * nbyte)
        for _ in range(nbyte):
            value = (value << 8) | bytes_data[a]
            a += 1
        return value
    else:
        raise ValueError("Unsupported bit size")


def main(filename):
    try:
        with open(filename, "rb") as f:
            bytes_data = list(f.read())
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return

    i1 = get_int16(0, bytes_data)
    i2 = i1 + get_int16(2, bytes_data)
    i3 = i2 + get_int16(6, bytes_data)
    i4 = i3 + get_int16(6, bytes_data)

    rootkey = list(" abcdefghijklmnopqrstuvwxyz,.'[]")

    output_dict = {}
    step = 0
    for i in range(1024):
        k0 = rootkey[i // 32]
        k1 = rootkey[i % 32]

        if k0 == " ":
            continue

        # 獲取索引區間
        start_ci = get_int16(i * 2, bytes_data)
        end_ci = get_int16(i * 2 + 2, bytes_data)

        for ci in range(start_ci, end_ci):
            bit24 = get_bits(i4, 24, ci, bytes_data)
            hi = get_bits(i1, 2, ci, bytes_data)
            lo = bit24 & 0x3FFF

            k2 = rootkey[bit24 >> 19]
            k3 = rootkey[(bit24 >> 14) & 0x1F]

            # 組合 Key 並去除空白 (模仿 trim)
            full_key = (k0 + k1 + k2 + k3).strip()

            char = chr((hi << 14) | lo)

            # 輸出結果
            if full_key not in output_dict:
                output_dict[full_key] = []
            output_dict[full_key].append(f"{char}")
            # print(f"[{full_key}]\t{char}")
            step += 1

    out_file = os.path.splitext(os.path.abspath(filename))[0] + ".json"
    print(f"{out_file}")
    with open(out_file, "w", encoding="utf-8") as ofile:
        json.dump(output_dict, ofile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    for name in os.scandir("TAB"):
        if os.path.splitext(name.path)[-1] != ".tab":
            continue
        main(name.path)
