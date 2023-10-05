import sys
import json
from jsonpath_rw import jsonpath, parse

class SymbolsList(list):

    CLOSE_MAP = {
        "{": "}",
        "[": "]",
    }

    def add_sym(self, sym):
        if sym in self.CLOSE_MAP:
            self.insert(0, self.CLOSE_MAP[sym])
        elif sym in self.CLOSE_MAP.values():
            self.remove(sym)
        else:
            # discard symbol
            pass


def preprocess_json(json_str, to_char):
    if not to_char or to_char > len(json_str):
        return json_str

    i_next_close_bracket = json_str[to_char:].find("}")
    i_next_comma = json_str[to_char:].find(",")
    i_next_eol = json_str[to_char:].find("\n")
    i_to_go = min(i_next_close_bracket, i_next_comma, i_next_eol)

    # Updates to_char, to the next close "}" or "," or "\n"
    to_char = to_char+i_to_go
    num_close_brackets = json_str[to_char:].count("}")
    num_open_brackets = json_str[to_char:].count("{")
    json_str_trunc = json_str[:to_char]
    
    reverted_json_str_trunc = json_str_trunc[::-1]
    symbols = SymbolsList()
    # print(reverted_json_str_trunc)
    for ch in reverted_json_str_trunc:
        if ch in SymbolsList.CLOSE_MAP.keys() or ch in SymbolsList.CLOSE_MAP.values():
            symbols.add_sym(ch)

    json_str_trunc += "".join(symbols[::-1])


    print(json_str_trunc)
    return json_str_trunc
    
    

def main(argv):

    try:
        expr_string = argv[1]
    except IndexError as e:
        print(f"Usage {argv[0]} <jsonpath expr> [fname=demo.json] [to_char=EOF]")
        print(f"Try with {argv[0]} '*.bicycle.price' demo.json 32")
        sys.exit(100)

    try:
        fname = argv[2]
    except IndexError as e:
        fname = "demo.json"
        to_char = None
    
    try:
        to_char = int(argv[3])
    except ValueError as e:
        print("The <to_char> parameter must be int")
        sys.exit(101)
    except IndexError as e:
        to_char = None

    expr = parse(expr_string)
    with open(fname, "r") as f:
        j = json.loads(preprocess_json(f.read(), to_char))
    
    print(f"INPUT EXPR: {expr_string}")
    try:
        x = expr.find(j)[-1]
    except IndexError as e:
        print("JSONPath not found")
    else:
        print(f"OUTPUT PATH: {x.full_path}")


if __name__ == "__main__":
    main(sys.argv)
