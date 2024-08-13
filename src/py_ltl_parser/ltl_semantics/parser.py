from typing import Optional
from dataclasses import dataclass
import ply.yacc as yacc
from .lexer import LTLLexer, LTLTokensConfig
from .ltl import *


class LTLParser:
    def __init__(
        self,
        tokens_config: LTLTokensConfig,
        operators_mapping: Optional[dict[str, str]] = None,
    ) -> None:
        self.ltl_lexer = LTLLexer(tokens_config)
        self.operators_mapping = operators_mapping or {}
        self.lexer, self.tokens = self.ltl_lexer.lexer, self.ltl_lexer.tokens
        self.parser = yacc.yacc(module=self, debug=True)

    def parse(self, expr: str) -> Expr:
        try:
            Expr.__operators_mapping__ = self.operators_mapping
            return self.parser.parse(expr, lexer=self.lexer)
        finally:
            Expr.__operators_mapping__ = {}

    # https://docs.uppaal.org/grammar/#Query
    def p_symbolic_query(self, p):
        """
        SymbolicQuery : AE expression
        | AG expression
        | EG expression
        | EE expression
        | expression ARROW expression
        """
        # print(list(p))
        if len(p) == 3:
            p[0] = UnaryOperator(p[1], p[2])
        elif len(p) == 4:
            p[0] = BinaryOperator(p[1], p[2], p[3])
        else:
            raise NotImplementedError(p[:])
        # '''
        #     | expression ARROW expression Subjection
        #     | SUP COLON List Subjection
        #     | SUP LBRACE Predicate RBRACE COLON List Subjection
        #     | INF COLON List Subjection
        #     | INF LBRACE Predicate RBRACE COLON List Subjection
        #     | BOUNDS COLON List Subjection
        #     | BOUNDS LBRACE Predicate RBRACE COLON List Subjection
        # '''
        pass

    def p_List(self, p):
        """List : expression
        | expression COMMA List
        """
        match p:
            case [_, expr]:
                p[0] = [expr]
            case [_, expr, _, list]:
                p[0] = [expr] + list

    def p_EXPRESSION(self, p):
        """
        expression : bin_op_lv8

        """
        print("aa", p[:])
        match p[:]:
            case [_, Identifier() | Const()]:
                p[0] = p[1]
            case [_, BinaryOperator() | UnaryOperator()]:
                p[0] = p[1]
            case [_, "(", ex, ")"]:
                p[0] = ex
            case [_, l, op, r]:
                p[0] = BinaryOperator(l, op, r)
            case _:
                raise NotImplementedError(p[:])

    def p_binop_level_8(self, p):
        """bin_op_lv8 : bin_op_lv7
        | bin_op_lv7 IMPLIES bin_op_lv8
        """
        match p[:]:
            case [_, expr, "->", expr2]:
                p[0] = BinaryOperator(expr, "->", expr2)
            case [_, expr]:
                p[0] = expr
            case _:
                raise NotImplementedError(p[:])

    def p_binop_level_7(self, p):
        """bin_op_lv7 : bin_op_lv6
        | bin_op_lv6 UNION bin_op_lv7
        """
        match p[:]:
            case [_, expr, "U", expr2]:
                p[0] = BinaryOperator(expr, "U", expr2)
            case [_, expr]:
                p[0] = expr
            case _:
                raise NotImplementedError(p[:])

    # 逻辑连接词级别
    def p_binop_level_6(self, p):
        """bin_op_lv6 : bin_op_lv5
        | bin_op_lv5 XOR bin_op_lv6
        | bin_op_lv5 AND bin_op_lv6
        | bin_op_lv5 OR bin_op_lv6
        """
        match p[:]:
            case [_, expr, op, expr2]:
                p[0] = BinaryOperator(expr, op, expr2)
            case [_, expr]:
                p[0] = expr
            case _:
                raise NotImplementedError(p[:])

    # 比较级别
    def p_binop_level_5(self, p):
        """bin_op_lv5 : bin_op_lv4
        | bin_op_lv4 GT bin_op_lv5
        | bin_op_lv4 LE bin_op_lv5
        | bin_op_lv4 GE bin_op_lv5
        | bin_op_lv4 EQ bin_op_lv5
        | bin_op_lv4 NE bin_op_lv5
        | bin_op_lv4 LT bin_op_lv5
        """
        match p[:]:
            case [_, expr, op, expr2]:
                p[0] = BinaryOperator(expr, op, expr2)
            case [_, expr]:
                p[0] = expr
            case _:
                raise NotImplementedError(p[:])

    # 加减、左右移位级别
    def p_binop_level_4(self, p):
        """
        bin_op_lv4 : bin_op_lv3 PLUS bin_op_lv4
            | bin_op_lv3 MINUS bin_op_lv4
            | bin_op_lv3 LSHIFT bin_op_lv4
            | bin_op_lv3 RSHIFT bin_op_lv4
            | bin_op_lv3
        """
        match p[:]:
            case [_, expr, op, expr2]:
                p[0] = BinaryOperator(expr, op, expr2)
            case [_, expr]:
                p[0] = expr
            case _:
                raise NotImplementedError(p[:])
        # p [0] = BinaryOperator(p[1], p[2], p[3])

    # 乘除求余级别
    def p_binop_level_3(self, p):
        """
        bin_op_lv3 : sub_expression TIMES bin_op_lv3
            | sub_expression DIVIDE bin_op_lv3
            | sub_expression MOD bin_op_lv3
            | sub_expression
        """
        match p[:]:
            case [_, expr, op, expr2]:
                p[0] = BinaryOperator(expr, op, expr2)
            case [_, expr]:
                p[0] = expr
            case _:
                raise NotImplementedError(p[:])

    def p_SUB_expression(self, p):
        """
        sub_expression :  LPAREN expression RPAREN
            | NOT expression
            | primary
        """
        match p[:]:
            case [_, "(", expr, ")"]:
                p[0] = expr
            case [_, "!", expr]:
                p[0] = UnaryOperator("!", expr)
            case [_, expr]:
                p[0] = expr
            case _:
                raise NotImplementedError(p[:])

    def p_simple_expression(self, p):
        """
        primary : IDENTIFIER
            | POS_INTEGER
        """
        match p[:]:
            case [_, BinaryOperator()]:
                p[0] = p[1]
            case [_, Identifier() | Const()]:
                p[0] = p[1]
            case _:
                raise NotImplementedError(p[:])

    def p_error(self, p):
        print(p, p.lexpos)
        print(f"Syntax error at '{p.value}'")


def parse_ltl(ltl_string, parser: Optional[LTLParser] = None) -> Expr:
    if parser is None:
        parser = LTLParser(LTLTokensConfig())
    return parser.parse(ltl_string)
