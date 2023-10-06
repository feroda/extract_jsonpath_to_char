import sys
import json
from jsonpath_rw import jsonpath, parse

class SymbolsList(list):

    CLOSE_MAP = {
        "{": "}",
        "[": "]",
    }
    count_square_close = 0
    count_curly_close = 0
    count_square_open = 0
    count_curly_open = 0

    def add_sym(self, sym):
        if sym == "{":
            if self.count_curly_close > 0:
                self.remove(self.CLOSE_MAP[sym])
                self.count_curly_close -= 1
            else:
                self.insert(0, self.CLOSE_MAP[sym])

        elif sym == "}":
            if self.count_curly_open > 0:
                self.remove(sym)
                self.count_curly_open -= 1
            else:
                self.insert(0, sym)
                self.count_curly_close += 1

        if sym == "[":
            if self.count_square_close > 0:
                self.remove(self.CLOSE_MAP[sym])
                self.count_square_close -= 1
            else:
                self.insert(0, self.CLOSE_MAP[sym])

        elif sym == "]":
            if self.count_square_open > 0:
                self.remove(sym)
                self.count_square_open -= 1
            else:
                self.insert(0, sym)
                self.count_square_close += 1

        else:
            # discard symbol
            pass


def preprocess_json(json_str, to_char):
    if not to_char or to_char > len(json_str):
        return json_str

    i_prev_eol = json_str[:to_char].rfind("\n")+1
    i_next_eol = json_str[to_char:].find("\n")+to_char
    # DEBUG print(f"{i_next_eol=}")

    # WARNING: avoid to truncate the line at curly brackets or comma index into string values
    i_next_close_bracket = json_str[:i_next_eol].rfind("}")
    i_next_comma = json_str[:i_next_eol].rfind(",")
    # DEBUG print(f"{i_next_close_bracket=} {i_next_comma=}")

    i_to_compare = max(i_next_close_bracket, i_next_comma)
    # DEBUG print(f"{i_prev_eol=}")
    i_end_key = json_str[i_prev_eol:i_next_eol].find('"', 2)+i_prev_eol+2  # adds 2 chars ":
    if max(to_char,i_end_key) < i_to_compare < i_next_eol:
        i_to_go = i_to_compare
        # DEBUG print(f"i_to_compare: {i_to_go=} {i_end_key=}")
    else:
        i_to_go = i_next_eol
        # DEBUG print(f"i_next_eol: {i_to_go=} {i_end_key=}")

    # Updates to_char, to the next close "}" or "," or "\n"
    json_str_trunc = json_str[:i_to_go]
    # DEBUG print(json_str_trunc)
    # DEBUG print()
    
    reverted_json_str_trunc = json_str_trunc[::-1]
    symbols = SymbolsList()
    # DEBUG print(reverted_json_str_trunc)
    for ch in reverted_json_str_trunc:
        if ch in SymbolsList.CLOSE_MAP.keys() or ch in SymbolsList.CLOSE_MAP.values():
            # DEBUG print("MATCH", ch)
            symbols.add_sym(ch)
            # DEBUG print(symbols[::-1])

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
        # print(f"OUTPUT PATH: {x.full_path=}")
        print(f"OUTPUT PATH: {x.full_path}")


if __name__ == "__main__":
    main(sys.argv)
