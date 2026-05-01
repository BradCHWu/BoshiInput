from FileConvert import BinFileToJson

if __name__ == "__main__":
    value = BinFileToJson("liu.bin")

    AA = [len(v) for v in value.values()]
    keys = list(value.keys())
    print(keys[121], AA.index(max(AA)), max(AA))
