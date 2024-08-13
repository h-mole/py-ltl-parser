import ply.lex as lex
from typing import Callable, Optional, Union
from dataclasses import dataclass, field
from .ltl import Const, Identifier


@dataclass
class LTLTokensConfig:
    tokens_mapping: list[tuple[str, Union[str, Callable[[object], object]]]] = field(
        default_factory=list
    )

    def update_variables_scope(self, scope: object):
        for token_name, token_value in self.tokens_mapping:
            assert hasattr(scope, token_name), f"Token {token_name} not in scope."
            match token_value:
                case str() | _ if callable(token_value):
                    setattr(scope, token_name, token_value)
                case _:
                    raise ValueError(f"Invalid token value: {token_value}")


class LTLLexer:
    def __init__(self, config: Optional[LTLTokensConfig] = None):

        self.t_SUP = r"sup"
        self.t_INF = r"inf"
        self.t_BOUNDS = r"bounds"
        self.t_LBRACKET = r"\["
        self.t_RBRACKET = r"\]"
        self.t_LBRACE = r"\{"
        self.t_RBRACE = r"\}"
        self.t_LPAREN = r"\("
        self.t_RPAREN = r"\)"
        self.t_COLON = r"\:"
        self.t_COMMA = r","
        self.t_ARROW = r"-->"
        self.t_UNDER = r"under"
        self.t_FALSE = r"false"
        self.t_TRUE = r"true"

        self.t_QUOTED_TEXT = r"\".*?\""
        self.t_PLUSPLUS = r"\+\+"
        self.t_MINUSMINUS = r"--"
        self.t_IMPLIES = r"->"
        self.t_DOT = r"\."
        self.t_LOCATION = r"location"
        self.t_MINUS_2147483648 = r"-2147483648"
        self.t_DEADLOCK = r"deadlock"
        self.t_STRING_LITERAL = r"\'.*?\'"
        # self.# t_DYNAMICE_EXPRESSION = r'\w+?D/ynamicExpression'
        self.t_MITL_EXPRESSION = r"\w+?MITLExpression"
        self.t_ASSIGNMENT = r"\w+?Assignment"
        self.t_ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
        self.t_TYPE = r"\w+?Type"
        self.t_LT = r"<"
        self.t_LE = r"<="
        self.t_EQ = r"=="
        self.t_NE = r"!="
        self.t_GT = r">"
        self.t_GE = r">="
        self.t_PLUS = r"\+"
        self.t_MINUS = r"-"
        self.t_TIMES = r"\*"
        self.t_DIVIDE = r"/"
        self.t_MOD = r"%"
        self.t_POW = r"\*\*"
        self.t_AMPERSAND = r"&"
        self.t_PIPE = r"\|"
        self.t_CARET = r"\^"
        self.t_LSHIFT = r"<<"
        self.t_RSHIFT = r">>"
        self.t_AND = r"&&"
        self.t_OR = r"\|\|"
        self.t_XOR = r"\^"
        self.t_QUESTION = r"\?"
        self.t_AND_OP = r"and"
        self.t_OR_OP = r"or"
        self.t_XOR_OP = r"xor"
        self.t_ignore = " \t\n"
        self.t_NOT = r"!"
        self.tokens = (
            "AG",  # All paths, Always satisfy
            "EG",  # Exists a path, Always satisfy
            "AE",  # All paths, Eventually satisfy
            "EE",  # Exists a path, Eventually satisfy
            "SUP",
            "INF",
            "BOUNDS",
            # "STRATEGYNAME",
            "LBRACKET",
            "RBRACKET",
            "LBRACE",
            "RBRACE",
            "COLON",
            "COMMA",
            "ARROW",
            "UNDER",
            "IDENTIFIER",
            "LPAREN",
            "RPAREN",
            "FALSE",
            "TRUE",
            "POS_INTEGER",
            "DECIMAL_NUMBER",
            "QUOTED_TEXT",
            "BUILTIN_FUNCTION1",
            "BUILTIN_FUNCTION2",
            "BUILTIN_FUNCTION3",
            "PLUSPLUS",
            "MINUSMINUS",
            "DOT",
            "NOT",
            "UNION",
            "LOCATION",
            "NON_TYPE_ID",
            "ARG_LIST",
            "ASSIGNMENT",
            "STRING_LITERAL",
            "DYNAMIC_EXPRESSION",
            "MITL_EXPRESSION",
            "ID",
            "TYPE",
            "LT",
            "LE",
            "EQ",
            "NE",
            "GT",
            "GE",
            "PLUS",
            "MINUS",
            "TIMES",
            "DIVIDE",
            "MOD",
            "POW",
            "AMPERSAND",
            "PIPE",
            "CARET",
            "LSHIFT",
            "RSHIFT",
            "AND",
            "OR",
            "XOR",
            "QUESTION",
            "IMPLIES",
            "AND_OP",
            "OR_OP",
            "XOR_OP",
            "MINUS_2147483648",
            "DEADLOCK",
            # "EXPRESSION",
        )
        self.config = config or LTLTokensConfig()
        self.config.update_variables_scope(self)
        self.lexer = lex.lex(module=self)

    # The token parsing order
    # could be seen from
    # https://ply.readthedocs.io/en/latest/ply.html#specification-of-tokens
    # The function-defined tokens first, then string-defined tokens.
    def t_AG(self, t):
        r"A\[\]"
        return t

    def t_EG(self, t):
        r"E\[\]"
        return t

    def t_EE(self, t):
        r"E<>"
        return t

    def t_AE(self, t):
        r"A<>"
        return t

    def t_POS_INTEGER(self, t):
        r"\d+"
        t.value = Const(t.value, "int")
        return t

    def t_IDENTIFIER(self, t):
        r"\w+"
        if t.value == "U":
            t.type = "UNION"
        else:
            t.value = Identifier(t.value)

        return t

    def t_DECIMAL_NUMBER(self, t):
        r"\d+(\.\d+)?"
        t.value = Const(t, "float")
        return t

    def t_error(self, t):
        print(t.value)
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)
