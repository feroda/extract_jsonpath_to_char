import sys
import json
from jsonpath_rw import jsonpath, parse


def main(argv):

    try:
        expr_string = argv[1]
    except IndexError as e:
        print(f"Usage {argv[0]} <jsonpath expr> [fname=demo.json]")
        print(f"Try with {argv[0]} '*.bicycle.price'")
        sys.exit(100)

    try:
        fname = argv[2]
    except IndexError as e:
        fname = "demo.json"
    
    
    expr = parse(expr_string)
    with open(fname, "r") as f:
        j = json.loads(f.read())
    
    print(f"INPUT EXPR: {expr_string}")
    try:
        x = expr.find(j)[-1]
    except IndexError as e:
        print("JSONPath not found")
    else:
        print(f"OUTPUT PATH: {x.full_path}")


if __name__ == "__main__":
    main(sys.argv)
