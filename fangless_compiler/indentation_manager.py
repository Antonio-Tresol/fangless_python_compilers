from ply.lex import Lexer, LexToken
from collections.abc import Iterable
import sys
from common import new_token, VERBOSE_INDENTATION

NO_INDENT = 0
MAY_INDENT = 1
MUST_INDENT = 2


class FanglessIndentationManager:
    @staticmethod
    def add_indentations(tokens: Iterable, lexer: Lexer) -> list:
        if VERBOSE_INDENTATION:
            print("----INDENTATION MANAGER DEBUG----")
        new_tokens = FanglessIndentationManager.identify_indentations(lexer, tokens)
        return FanglessIndentationManager.assign_indentations(new_tokens)

    @staticmethod
    def identify_indentations(lexer: Lexer, token_stream: Iterable) -> list:
        lexer.atLineStart = at_line_start = True
        indent = NO_INDENT

        new_token_list = []

        for token in token_stream:
            token.atLineStart = at_line_start

            match token.type:
                case "COLON":
                    at_line_start = False
                    indent = MAY_INDENT
                    token.must_indent = False

                case "NEWLINE":
                    at_line_start = True

                    if indent == MAY_INDENT:
                        indent = MUST_INDENT

                    token.must_indent = False

                case "WHITESPACE":
                    assert token.atLineStart is True

                    at_line_start = True
                    token.must_indent = False

                case _:
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
            match token.type:
                case "WHITESPACE":
                    assert depth == 0
                    depth = len(token.value)
                    last_seen_whitespace = True
                    continue

                case "NEWLINE":
                    depth = 0

                    if not last_seen_whitespace and not token.atLineStart:
                        new_token_list.append(token)
                    continue

                case _:
                    pass

            last_seen_whitespace = False

            try:
                check_for_indentation(token, depth, levels, new_token_list)
            except ValueError:
                print(f"tokens so far{new_token_list}")
                print(f"failed on token: {token}")
                sys.exit()

        if len(levels) > 1:
            assert token is not None
            new_token_list.extend(
                create_dedent(token.lineno)
                for _ in range(
                    1,
                    len(levels),
                )
            )

        return new_token_list


def check_for_indentation(
    token: LexToken,
    depth: int,
    levels: list,
    new_token_list: list,
) -> None:
    if token.must_indent:
        if not (depth > levels[-1]):
            print(f"Indentation Error on must indent in line no {token.lineno}")
            raise ValueError

        if VERBOSE_INDENTATION:
            print(f"---Token must indent: {token}---")

        levels.append(depth)
        new_token_list.append(create_indent(token.lineno))

    elif token.atLineStart:
        if depth == levels[-1]:
            pass

        elif depth > levels[-1]:
            print(
                f"Indentation Error on line start in line no {token.lineno}"
                " with depth greater than levels",
            )
            raise ValueError

        # if token depth is less that levels[-1] i dedented
        try:
            i = levels.index(depth)
        except ValueError:
            print(f"Indentation Error on line start in line no {token.lineno}")
            raise

        for _ in range(i + 1, len(levels)):
            temp = new_token_list.pop()
            new_token_list.extend((create_dedent(token.lineno - 1), temp))
            levels.pop()

    new_token_list.append(token)

    if VERBOSE_INDENTATION:
        print(new_token_list[-1])


def create_indent(line_number: int) -> LexToken:
    return new_token("INDENT", line_number, -100)


def create_dedent(line_number: int) -> LexToken:
    return new_token("DEDENT", line_number, -100)
