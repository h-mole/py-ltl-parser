from ..ltl_semantics import Identifier, LTLParser, LTLTokensConfig, parse_ltl, LTLLexer


class UppaalLexer(LTLLexer):
    def __init__(self):
        super().__init__(LTLTokensConfig())
        self.t_IMPLIES = r"-->"

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

    def t_IDENTIFIER(self, t):
        r"\w+"
        t.value = Identifier(t.value)

        return t


class UppaalLTLParser(LTLParser):
    def __init__(self) -> None:
        super().__init__(UppaalLexer(), {"-->": "->"})


def parse_uppaal_ltl(ltl_string: str):
    parsed = parse_ltl(ltl_string, UppaalLTLParser())
    return parsed
