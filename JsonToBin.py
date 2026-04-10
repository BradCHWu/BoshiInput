import json
import zlib


def JsonFileToJson(json_file: str) -> dict:
    with open(json_file, encoding="utf-8") as ifile:
        data = json.load(ifile)
    return data["chardefs"]


def JsonToBinFile(json_data: str, bin_file: str) -> None:
    json_string = json.dumps(json_data, ensure_ascii=False)
    compressed = zlib.compress(json_string.encode())
    with open(bin_file, "wb") as ofile:
        ofile.write(compressed)


def BinFileToJson(bin_file: str) -> dict:
    with open(bin_file, "rb") as ifile:
        compressed = ifile.read()
    decompressed = zlib.decompress(compressed)
    json_string = decompressed.decode()
    return json.loads(json_string)


if __name__ == "__main__":
    data = JsonFileToJson("liu.json")
    JsonToBinFile(data, "liu.bin")

    data = BinFileToJson("liu.bin")
    print(data["wv"])
