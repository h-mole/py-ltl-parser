from ..ltl_semantics import Identifier, LTLParser, LTLTokensConfig, parse_ltl, LTLLexer


class XSTAMPPLTLLexer(LTLLexer):
    def __init__(self):
        super().__init__(LTLTokensConfig())

    def t_AG(self, t):
        r"\[\]"
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
        if t.value == "U":
            t.type = "OR"
        else:
            t.value = Identifier(t.value)
        return t


class XSTAMPPLTLParser(LTLParser):
    def __init__(self) -> None:
        super().__init__(XSTAMPPLTLLexer(), {"U": "||", "U": '||', '[]': 'A[]'})


def parse_xstampp_ltl(ltl_string: str):
    parsed = parse_ltl(ltl_string, XSTAMPPLTLParser())
    return parsed
