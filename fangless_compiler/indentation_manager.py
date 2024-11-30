from ply.lex import Lexer, LexToken
from collections.abc import Iterable
import sys
from common import new_token, VERBOSE_INDENTATION
from exceptions import IndentationMismatchError

NO_INDENT = 0
MAY_INDENT = 1
MUST_INDENT = 2


def create_indent(line_number: int) -> LexToken:
    return new_token("INDENT", line_number, -100)


def create_dedent(line_number: int) -> LexToken:
    return new_token("DEDENT", line_number, -100)


class FanglessIndentationManager:
    @staticmethod
    def add_indentations(tokens: Iterable, lexer: Lexer) -> list:
        if VERBOSE_INDENTATION:
            print("----INDENTATION MANAGER DEBUG START----")
        new_tokens = FanglessIndentationManager.identify_indentations(lexer, tokens)
        new_tokens = FanglessIndentationManager.assign_indentations(new_tokens)
        if VERBOSE_INDENTATION:
            print("----INDENTATION MANAGER DEBUG END----")
        return new_tokens

    @staticmethod
    def identify_indentations(lexer: Lexer, token_stream: Iterable) -> list:
        lexer.atLineStart = at_line_start = True
        indent = NO_INDENT

        new_token_list = []
        if VERBOSE_INDENTATION:
            print("--ORIGINAL TOKEN LIST--\n")
        for token in token_stream:
            token.atLineStart = at_line_start
            if VERBOSE_INDENTATION:
                print(token)

            match token.type:
                case "COLON":
                    at_line_start = False
                    # we may indent, for must indent we need COLON NEWLINE
                    indent = MAY_INDENT
                    token.must_indent = False

                case "NEWLINE":
                    at_line_start = True
                    # is last token was a COLON and this one is a COLON,
                    # we must indent
                    if indent == MAY_INDENT:
                        indent = MUST_INDENT

                    token.must_indent = False

                case "WHITESPACE":
                    assert token.atLineStart is True
                    # all whitespace is at the start of the line
                    at_line_start = True
                    token.must_indent = False

                case _:  # for all other tokens
                    # if the 2 tokens before us we COLON NEWLINE
                    # we must indent here
                    if indent == MUST_INDENT:
                        token.must_indent = True
                    else:
                        token.must_indent = False

                    at_line_start = False
                    indent = NO_INDENT

            new_token_list.append(token)
            lexer.atLineStart = at_line_start
        if VERBOSE_INDENTATION:
            print("\n--ORIGINAL TOKEN LIST END--")
        return new_token_list

    @staticmethod
    def assign_indentations(token_stream: list) -> list:
        # Initialize the levels list with a single element 0,
        # representing the base indentation level
        levels = [0]
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
                    # Reset depth to 0 at the start of a new line
                    depth = 0
                    if not last_seen_whitespace and not token.atLineStart:
                        new_token_list.append(token)
                    continue

                case _:
                    pass

            # Reset the last_seen_whitespace flag
            last_seen_whitespace = False

            # Check for indentation and update the token list accordingly
            FanglessIndentationManager.check_for_indentation(
                token,
                depth,
                levels,
                new_token_list,
            )

        # If there are remaining levels, create dedent tokens for each level
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

    @staticmethod
    def check_for_indentation(
        token: LexToken,
        depth: int,
        levels: list,
        new_token_list: list,
    ) -> None:
        # levels[-1] has the current level of indentation
        # depth has the depth of indentation of current token.

        if token.must_indent:
            if not (depth > levels[-1]):
                error = (
                    "Indentation Error on must indent "
                    f"in line no {token.lineno}"
                )
                raise IndentationMismatchError(error)

            if VERBOSE_INDENTATION:
                print(f"---Token must indent: {token}---")

            levels.append(depth)
            new_token_list.append(create_indent(token.lineno))

        elif token.atLineStart:
            if depth == levels[-1]:  # token at same depth level than  last one
                pass

            # If the depth is greater than the last level, it's an error
            elif depth > levels[-1]:
                error = (
                    "Indentation Error on line start "
                    f"in line no {token.lineno}"
                    " with depth greater than levels"
                )
                raise IndentationMismatchError(error)

            # If the depth is less than the last level, we just dedented
            try:
                i = levels.index(depth)
            except ValueError:
                error = (
                    "Indentation Error on line start"
                    f"in line no {token.lineno}"
                )
                raise IndentationMismatchError(error)

            # Pop levels and create dedent tokens until the current depth is reached
            for _ in range(i + 1, len(levels)):
                temp = new_token_list.pop()
                # we add dedent before the newline, to ease parsing
                new_token_list.extend((create_dedent(token.lineno - 1), temp))
                levels.pop()

        new_token_list.append(token)

        if VERBOSE_INDENTATION:
            print(new_token_list[-1])
