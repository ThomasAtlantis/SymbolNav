from itertools import batched
from typing import List
from symbolnav import ASTNode


table_template = \
"""
\\begin{{table}}
    \\centering
    \\begin{{tabular}}{{{column_spec}}}
    \\hline
{body}\\end{{tabular}}
\\end{{table}}
"""
table_row_template = \
"""     {latex_symbols} \\\\ \\hline\n"""

class Renderer:

    def to_latex_table(self, latex_symbols: List[str], num_cols: int = 8):
        body = ""
        for batch in batched(latex_symbols, num_cols):
            batch = list(batch)
            if len(batch) < num_cols:
                batch.extend([""] * (num_cols - len(batch)))
            body += table_row_template.format(latex_symbols=" & ".join(f"${latex_symbol}$" for latex_symbol in batch))
        latex = table_template.format(column_spec="l".join("|" for _ in range(num_cols + 1)), body=body)
        return latex

    def to_latex(self, symbol: ASTNode) -> str:
        return self._render_to_latex(symbol)

    def _render_to_latex(self, node: ASTNode | str | list | None) -> str:
        if isinstance(node, ASTNode):
            left = self._render_to_latex(node.attributes['left']) if 'left' in node.attributes else None
            right = self._render_to_latex(node.attributes['right']) if 'right' in node.attributes else None
            left_blank = " " if left else ""
            right_blank = " " if right else ""

            match node.node_type:
                case 'SymbolPostfix':
                    return (f"{self._render_to_latex(node.attributes['symbol'])}"
                            f"{self._render_to_latex(node.attributes['postfix'])}")
                case 'Symbol':
                    return node.attributes['symbol']
                case 'Format':
                    return (f"{node.attributes['format']}"
                            "{"
                            f"{self._render_to_latex(node.attributes['content'])}"
                            "}")
                case 'FormatOp':
                    return (f"{node.attributes['op']}"
                            "{"
                            f"{self._render_to_latex(node.attributes['content'])}"
                            "}")
                case 'GeneralPostfix':
                    return (f"{self._render_to_latex(node.attributes['content'])}"
                            f"{self._render_to_latex(node.attributes['postfix'])}")
                case 'Relation':
                    return (f"{left}"
                            f"{left_blank}{node.attributes['op']}{right_blank}"
                            f"{right}")
                case 'Additive':
                    return (f"{left}"
                            f"{left_blank}{node.attributes['op']}{right_blank}"
                            f"{right}")
                case 'Supscript':
                    return ("^{"
                            f"{self._render_to_latex(node.attributes['value'])}"
                            "}")
                case 'Subscript':
                    return ("_{"
                            f"{self._render_to_latex(node.attributes['value'])}"
                            "}")
                case 'List':
                    return node.attributes['separator'].join(self._render_to_latex(item) for item in node.attributes['items'])
                case 'MP':
                    return (f"{left}"
                            f"{left_blank}{node.attributes['op']}{right_blank}"
                            f"{right}")
                case 'Coated':
                    return (f"{node.attributes['coat_left']}"
                            f"{self._render_to_latex(node.attributes['content'])}"
                            f"{node.attributes['coat_right']}")
                case 'Fraction':
                    return ("\\frac{"
                            f"{self._render_to_latex(node.attributes['numerator'])}"
                            "}{"
                            f"{self._render_to_latex(node.attributes['denominator'])}"
                            "}")
                case _:
                    raise ValueError(f"Unknown node type: {node.node_type}")
        elif isinstance(node, str):
            return node
        elif isinstance(node, list):
            return "".join(self._render_to_latex(item) for item in node)
        else:
            return ""
        