
from ply import lex
from ply.lex import Lexer, LexToken
from collections.abc import Iterable
import sys

NO_INDENT = 0
MAY_INDENT = 1
MUST_INDENT = 2


class IndentationManager:
    @staticmethod
    def add_indentations(tokens: Iterable, lexer: Lexer) -> list:
        new_tokens = IndentationManager.identify_indentations(lexer, tokens)
        return IndentationManager.assign_indentations(new_tokens)

    @staticmethod
    def identify_indentations(lexer: Lexer, token_stream: Iterable) -> list:
        lexer.atLineStart = at_line_start = True
        indent = NO_INDENT

        new_token_list = []

        for token in token_stream:
            token.atLineStart = at_line_start

            if token.type == "COLON":
                at_line_start = False
                indent = MAY_INDENT
                token.must_indent = False

            elif token.type == "NEWLINE":
                at_line_start = True

                if indent == MAY_INDENT:
                    indent = MUST_INDENT

                token.must_indent = False

            elif token.type == "WHITESPACE":
                assert token.atLineStart is True

                at_line_start = True
                token.must_indent = False

            else:
                if indent == MUST_INDENT:
                    token.must_indent = True

                else:
                    token.must_indent = False

                at_line_start = False
                indent = NO_INDENT

            new_token_list.append(token)
            lexer.atLineStart = at_line_start

        return new_token_list

    @staticmethod
    def assign_indentations(token_stream: list) -> list:
        levels = [0]
        token = None
        depth = 0
        last_seen_whitespace = False

        new_token_list = []

        for token in token_stream:
            if token.type == "WHITESPACE":
                assert depth == 0
                depth = len(token.value)
                last_seen_whitespace = True
                continue

            if token.type == "NEWLINE":
                depth = 0

                if last_seen_whitespace or token.atLineStart:
                    continue

                new_token_list.append(token)
                continue

            last_seen_whitespace = False

            try:
                check_for_indentation(token, depth, levels, new_token_list)
            except ValueError:
                print(f"tokens so far{new_token_list}")
                print(f"failed on token: {token}")
                sys.exit()

        if len(levels) > 1:
            assert token is not None

            for _ in range(1, len(levels)):
                new_token_list.append(create_dedent(token.lineno))

        return new_token_list


def check_for_indentation(token: LexToken, depth: int
    , levels: list, new_token_list: list) -> None:
    if token.must_indent:
        if not (depth > levels[-1]):
            print(f"Indentation Error on must indent in line no { str(token.lineno) }")
            raise ValueError

        levels.append(depth)
        new_token_list.append(create_indent(token.lineno))

    elif token.atLineStart:
        if depth == levels[-1]:
            pass

        elif depth > levels[-1]:
            print(f"Indentation Error on line start in line no {str(token.lineno)} with depth greater than levels")

        else:
            try:
                i = levels.index(depth)
            except ValueError:
                print(f"Indentation Error on line start in line no {str(token.lineno)}")
                raise

            for _ in range(i + 1, len(levels)):
                new_token_list.append(create_dedent(token.lineno))
                levels.pop()
    new_token_list.append(token)


def create_indent(line_number: int) -> LexToken:
    return new_token("INDENT", line_number)


def create_dedent(line_number: int) -> LexToken:
    return new_token("DEDENT", line_number)


def new_token(new_type: str, line_number: int) -> LexToken:
    tok = lex.LexToken()

    tok.type = new_type
    tok.value = None
    tok.lineno = line_number
    tok.lexpos = -100

    return tok
