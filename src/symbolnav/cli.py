from typing import Annotated, Literal, Optional, OrderedDict

from rich.text import Text
from symbolnav import LaTeXMathExtractor
from symbolnav import SymbolExtractor
from symbolnav import Renderer
import tyro

from rich.style import Style
from rich.console import Console

console = Console(highlight=False)
style_marks = Style(color="#E285B5", bold=True)
style_context = Style(color="#888888")
style_value = Style(color="#77BCF1")

def main(
    file: Optional[str] = None, 
    /, 
    list_symbols: Annotated[bool, tyro.conf.arg(aliases=("-l",))] = False, 
    latex_table: Annotated[bool, tyro.conf.arg(aliases=("-t",))] = False,
    ignore_errors: Annotated[bool, tyro.conf.arg(aliases=("-i",))] = False,
    checkout: Annotated[int, tyro.conf.arg(aliases=("-c",))] = -1,
    latex: Optional[str] = None,
):
    symbol_extractor = SymbolExtractor()
    symbols = {}

    if file is None:
        assert latex is not None, "Either [file] or --latex must be provided"

        for symbol in symbol_extractor.extract_symbol(
            latex, file="input", line=1, column=1,
            ignore_errors=ignore_errors
        ):
            symbols[symbol] = (1, 1)
        for symbol in sorted(symbols.keys()):
            print(Renderer.to_latex(symbol))
    else:
        latex_math_extractor = LaTeXMathExtractor()
        latex_math = list(latex_math_extractor.analyze(file=file))
        for latex_math in latex_math:
            for symbol in symbol_extractor.extract_symbol(
                latex_math.value,
                file=file,
                line=latex_math.line,
                column=latex_math.column,
                ignore_errors=ignore_errors
            ):
                if symbol is None: continue
                if symbol not in symbols:
                    symbols[symbol] = OrderedDict()
                symbols[symbol][(latex_math.line, latex_math.column)] = latex_math
        sorted_symbols = list(sorted(symbols.keys()))
        latex_symbols = [Renderer.to_latex(symbol) for symbol in sorted_symbols]
        if list_symbols:
            for idx, (latex_symbol, symbol) in enumerate(zip(latex_symbols, sorted_symbols)):
                start_line, start_column = next(iter(symbols[symbol].keys()))
                print(f"[{idx:>3}] {latex_symbol:.<50}: in File {file}, line {start_line}, column {start_column}")
        if latex_table:
            print(Renderer.to_latex_table(latex_symbols, num_cols=6))
        
        if checkout != -1:
            latex_symbol = latex_symbols[checkout]
            symbol = sorted_symbols[checkout]
            console.print(Text(f"Checking out LaTeX Symbol [{checkout:>3}]: ") + Text(latex_symbol, style=style_value) + Text(", appears"))
            console.print()
            for line, column in symbols[symbol].keys():
                console.print(f"in File {file}, line {line}, column {column}", highlight=True)
                latex_math = symbols[symbol][(line, column)]
                console.print(latex_math.contexts[0], style=style_context, end="")
                console.print(latex_math.marks[0], style=style_marks, end="", )
                console.print(latex_math.value, style=style_value, end="")
                console.print(latex_math.marks[1], style=style_marks, end="")
                console.print(latex_math.contexts[1], style=style_context, end="")
                console.print("\n")

def run():
    tyro.cli(main)

if __name__ == "__main__":
    run()