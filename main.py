#! /bin/env python3 

from interpreter import Interpreter, Lexer


if __name__ == "__main__":

    while True:
        text = input(">>> ")

        try:
            if not text:
                continue

            r = Interpreter(Lexer(text)).expr()
            print(r)

        except Exception as exc:
            print(str(exc))
            break
