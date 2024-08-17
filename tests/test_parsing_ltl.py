import json
from py_ltl_parser import (
    parse_ltl,
    LTLParser,
    LTLTokensConfig,
    Identifier,
    Expr,
    parse_uppaal_ltl,
    parse_xstampp_ltl,
)


def test_parsing_ltl():
    ltl = "A[] ((((controlAction==IncreasePower))->(((!((controlAction==IncreasePower)))&&(((MyVar==Abnormal)))))))"
    # ltl = "[] (controlAction==IncreasePower) -> A U x"
    parsed = parse_ltl(ltl)
    print(json.dumps(parsed.to_dict(), indent=2))
    print(parsed.unparse())

    ltl = "A[] (((((ACE4==direct)&&(ACE3==direct)&&(ACE1==normal)&&(ACE2==normal)))->(!((controlAction==Providedisplacementandforcevariablesofthedrivingstick)))))"
    # ltl = "[] (controlAction==IncreasePower) -> A U x"
    parsed = parse_ltl(ltl)
    print(json.dumps(parsed.to_dict(), indent=2))
    print(parsed.unparse())


# def test_tokens_customization():

#     def t_AG(t):
#         r"G"
#         return t

#     def t_IDENTIFIER(t):
#         r"\w+"
#         if t.value == "G":
#             t.type = "AG"
#         else:
#             t.value = Identifier(t.value)

#         return t

#     ltl = "G a -> b"

#     parser = LTLParser(
#         LTLTokensConfig(
#             tokens_mapping=[("t_AG", t_AG), ("t_IDENTIFIER", t_IDENTIFIER)]
#         ),
#         operators_mapping={"G": "A[]"},
#     )
#     parsed = parse_ltl(ltl, parser)
#     print(parsed.unparse())


def test_parse_uppaal_ltl():
    parsed = parse_uppaal_ltl(
        "(((ACE4==0)&&(ACE3==0)&&(ACE1==0)&&(ACE2==2)))--> (!((s==0)))"
    )
    print(parsed.to_dict())
    # print(parsed.unparse({"-->"}))


def test_parse_xstampp_ltl():
    parsed = parse_xstampp_ltl("((controlAction==IncreasePower) -> A U x)")
    print(parsed.unparse())
    print("unparsed_to_uppaal", parsed.unparse({"->": "-->", "[]": "A[]"}))
