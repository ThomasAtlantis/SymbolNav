# SymbolNav

SymbolNav is an extractor/navigator for math symbols defined in LaTeX.

## TODO

- CLI tools to display/analyze results in terminal
    - show positions (lines and cols)
    - show latex context of given symbol
    - sort symbols
- Algorithm to sort symbols by their AST

## Features

- Basic arithmetic operators: `+`, `-`, `*`, `/`, `\times`, `\cdot`, `\div`, `:`
- Relational operators: `=`, `<`, `>`, `\leq`, `\geq`, `\triangleq`, `\approx`, `\in`, `\circ`, `\to`, `\setminus`, `\subset`
- Superscripts and subscripts: `x^2`, `x_i`, `x^{n+1}_{i+1}`, `x'`, `\prime`
- Formatting commands: `\mathbf`, `\text`, `\mathbb`, `\mathit`, `\bm`, `\mathcal`, `\hat`, `\tilde`, `\mathrm`
- Format-like operators: `\sqrt`
- Text mode support with `\text{...}` command
- Coated group with brackets: `{...}`, `(...)`, `\{...\}`, `[...]`, `\begin{bmatrix}...\end{bmatrix}`
- List separators: `,` (comma), `.` (period)
- Symbol types: numbers, letters, Greek letters, and other symbols


## Installation

Install dependencies:
```bash
pip install ply
```

Clone the project (installing is not supported currently):
```bash
git clone git@github.com:ThomasAtlantis/SymbolNav.git
```
## Usage

### Basic Parsing

```python
from symbol_nav.interpreter.interpreter import LaTeXMathInterpreter
from symbol_nav.interpreter.mast import to_dict
import json

# Create parser instance
interpreter = LaTeXMathInterpreter()

# Parse LaTeX expression
latex = r'x^2 + y^2'
ast = interpreter.parse(latex)

# Convert AST to dictionary
ast_dict = to_dict(ast, recursive=True)
print(json.dumps(ast_dict, indent=2))
```

### Symbol Extraction

```python
from symbol_nav.interpreter.interpreter import LaTeXMathInterpreter
from symbol_nav.extractor import Extractor

interpreter = LaTeXMathInterpreter()
extractor = Extractor()

# Parse LaTeX expression
latex = r'\mathbf{H}^\text{in} \in \mathbb{R}^{N \times d}'
ast = interpreter.parse(latex)

# Extract symbols from AST
symbols = []
for symbol in extractor.extract_symbol(ast):
    symbols.append(symbol)

print(symbols)
```

### Rendering AST to LaTeX

```python
from symbol_nav.renderer import Renderer

renderer = Renderer()

# Render any AST node back to LaTeX
latex_code = renderer.to_latex(ast_node)
print(latex_code)
```

### Extracting from LaTeX Documents

```python
from symbol_nav.extractor import Extractor
from symbol_nav.interpreter.interpreter import LaTeXMathInterpreter
from symbol_nav.renderer import Renderer

interpreter = LaTeXMathInterpreter()
extractor = Extractor()
renderer = Renderer()

# Read LaTeX document
with open("document.tex", "r") as f:
    latex_doc = f.read()

# Extract document structure
document = extractor.extract_document(latex_doc)

# Extract all math expressions
latex_math_list = extractor.extract_latex_math(document)

# Process each math expression
latex_symbols = {}
for pos, latex_math in latex_math_list:
    try:
        ast = interpreter.parse(latex_math)
        for symbol_postfix in extractor.extract_symbol(ast):
            symbol_latex = renderer.to_latex(symbol_postfix)
            # Use LaTeX as key for deduplication
            latex_symbols[symbol_latex] = pos
    except Exception as e:
        print(f"Error parsing: {latex_math}")
        print(e)

print(latex_symbols)
```

### Render the List of Symbols in LaTeX
```python
# Generate LaTeX table
table_latex = renderer.to_latex_table(list(latex_symbols.keys()), num_cols=8)
print(table_latex)
```

## Case Study

Download the source code of the paper **Efficient Distributed Retrieval-Augmented Generation for
Enhancing Language Model Performance** from [here](https://arxiv.org/src/2504.11197). It's a preprint version of paper among my publications. Run the following program:

```python
from symbol_nav.latex_math_extractor.extractor import LaTeXMathExtractor
from symbol_nav.symbol_extractor.extractor import SymbolExtractor
from symbol_nav.renderer import Renderer
import time


renderer = Renderer()
symbol_extractor = SymbolExtractor()
latex_math_extractor = LaTeXMathExtractor()
time_start = time.time()
latex_math = list(latex_math_extractor.analyze(file="reference/main.tex"))
latex_math_1 = set(item.value for item in latex_math)
latex_symbols = {}
for latex_math in latex_math:
    for symbol in symbol_extractor.extract_symbol(latex_math.value):
        if symbol is None: continue
        symbol = renderer.to_latex(symbol)
        latex_symbols[symbol] = latex_math
print(renderer.to_latex_table(list(latex_symbols.keys()), num_cols=6))
```

It will throw an exception:

```
(1-\eta^r_t\delta)-\sum \bm p^l_t\bm p_t=\eta^l_t(1-\sum\bm (p_t^l)^2)+\eta^r_t\sum(\min(\bm p_t^l,\bm p_t^r)-\bm p_t^l\bm p^r_t)
                                                            ^
MathSyntaxError: Syntax error when parsing L_PAREN at position 60
```

This message indicates that a `{` is missing after `\bm`. If the parser interprets the parenthesis `(` as the content for `\bm`, there will be no matching closing parenthesis, leading to an unmatched `)`.

After this message, there would be a latex definition of the list of symbols:
```latex
\begin{table}[h]
    \centering
    \begin{tabular}{|l|l|l|l|l|l|}
    \hline
     $n$ & $x_{< M}$ & $V$ & $N$ & $d$ & $\mathcal{D}$ \\ \hline
     $k$ & $x_{< t}$ & $D^{\text{device}}$ & $\bm{P}^{\text{device}}_{t}$ & $\mathcal{M}^{\text{device}}$ & $\bm{P}^{\text{cloud}}_{t}$ \\ \hline
     $D$ & $D^{\text{cloud}}$ & $\bm{P}_{t}$ & $\bm{\omega}_{t}$ & $\mathcal{R}$ & $x_{t - 1}$ \\ \hline
     $t$ & $\bm{P}_{t}^{\text{device}}$ & $\bm{P}_{t}^{\text{cloud}}$ & $x_{t}$ & $\mathcal{F}^{\text{device}}$ & $\mathcal{F}^{\text{cloud}}$ \\ \hline
     $x$ & $\bm{p}_{t}$ & $A_{t}$ & $x^{*}_{t}$ & $C$ & $\mathcal{F}$ \\ \hline
     $\lambda$ & $s$ & $x^{s}_{t}$ & $\tilde{\bm{\omega}}_{t}$ & $D^{s}$ & $\bm{p}^{s}_{t}$ \\ \hline
     $x_{t}^{\text{device}}$ & $x_{t}^{\text{cloud}}$ & $\bm{p}_{t}^{\text{device}}$ & $\bm{p}_{t}^{\text{cloud}}$ & $l$ & $r$ \\ \hline
     $\eta^{s}_{t}$ & $h^{s}_{t}$ & $h^{l}_{t}$ & $h^{r}_{t}$ & $\bm{p}_{t}^{l}$ & $\bm{p}_{t}^{r}$ \\ \hline
     $h$ & $\eta^{l}_{t}$ & $\eta^{r}_{t}$ & $x^{l}_{t}$ & $\tilde{x}^{l}_{t}$ & $\tilde{x}_{t}^{l}$ \\ \hline
     $x^{r}_{t}$ & $\tilde{x}^{r}_{t}$ & $\tilde{x}_{t}^{r}$ & $x_{t}^{s}$ & $\bm{p}_{t}^{s}$ & $\mathcal{S}^{l}$ \\ \hline
     $\mathcal{S}^{r}$ & $\bm{p}^{a}$ & $\bm{p}^{b}$ & $\eta$ & $\tilde{x}$ & $x^{s}_{t + 1}$ \\ \hline
     $\beta^{s}_{t}$ & $\bm{p}^{l}_{t}$ & $\tilde{\bm{p}}^{r}_{t}$ & $\gamma^{l}$ & $\gamma^{r}$ & $\bm{p}^{r}_{t}$ \\ \hline
     $\alpha^{l}_{t}$ & $\delta$ & $x^{l}_{t - 1}$ & $x^{r}_{t - 1}$ & $Z_{t}$ & $c^{s}_{\text{dec}}$ \\ \hline
     $c^{s}_{\text{trans}}$ & $T_{\text{total}}$ & $u$ & $T_{\text{begin}}$ & $T_{\text{now}}$ & $Z^{s}_{t}$ \\ \hline
     $\varphi$ & $Z^{l}_{t}$ & $Z^{r}_{t}$ & $c^{l}_{\text{dec}}$ & $c^{r}_{\text{dec}}$ & $c^{l}_{\text{trans}}$ \\ \hline
     $\alpha^{r}_{t}$ & $\text{rtt}$ & $c^{r}_{\text{trans}}$ & $j$ & $c_{\text{dec}}$ & $c^{\text{device}}_{\text{trans}}$ \\ \hline
     $c^{\text{cloud}}_{\text{trans}}$ & $\alpha$ & $M$ & $\bm{c}^{s}_{\text{dec}}$ & $\bm{t}$ & $k^{s}_{a}$ \\ \hline
     $k^{s}_{b}$ & $k^{s}_{c}$ & $g$ & $L^{s}$ & $B^{s}$ & $\hat{c}^{\text{device}}_{\text{trans}}$ \\ \hline
     $\hat{c}^{\text{cloud}}_{\text{trans}}$ & $L^{\text{device}}$ & $L^{\text{cloud}}$ & $\hat{c}^{s}_{\text{dec}}$ & $\zeta$ & $\tilde{Z}_{t}$ \\ \hline
     $S_{t}$ & $\text{device}$ & $\text{cloud}$ & $\bm{p}^{\text{device}}_{t}$ & $\bm{p}^{\text{cloud}}_{t}$ & $p$ \\ \hline
     $\alpha^{l}_{0}$ & $\alpha^{r}_{0}$ & $B$ & $x^{l}$ & $x^{r}$ & $x^{r}_{1}$ \\ \hline
     $x^{r}_{t + 1}$ & $$ & $$ & $$ & $$ & $$ \\ \hline
\end{tabular}
\end{table}
```
which will be rendered as below:

![The List of Symbols](ListofSymbols.png)

## AST Node Types

The parser generates AST nodes with the following types:

- `Relation`: Relational expressions (e.g., `x = y`, `x \leq y`, `x \in A`, `x \approx y`, `x \subset B`)
- `Additive`: Addition and subtraction operations (e.g., `x + y`, `x - y`)
- `MP`: Multiplication and division operations (e.g., `x * y`, `x \times y`, `x / y`, `x \div y`, `x : y`, `x | y`)
- `Unary`: Unary operators (`+`, `-`)
- `SymbolPostfix`: Symbols with postfix operations (subscripts/superscripts)
- `Supscript`: Superscript expressions (e.g., `x^2`, `x'`)
- `Subscript`: Subscript expressions (e.g., `x_i`)
- `Format`: Formatted content (e.g., `\mathbf{H}`, `\mathbb{R}`, `\text{in}`, `\hat{x}`, `\sqrt{x}`)
- `Bracket`: Grouped expressions with brackets (e.g., `(x+y)`, `\{x\}`, `[x]`)
- `List`: List of relations separated by commas or periods (e.g., `x, y, z` or `x. y. z`)

## LaTeX Math Examples

### Simple Expression
```python
latex = r'x + y'
# AST: Additive(op='+', left=..., right=...)
```

### Superscripts and Subscripts
```python
latex = r'x^2 + y_i + z\''
# AST includes Supscript and Subscript nodes, including prime
```

### Formatting Commands
```python
latex = r'\mathbf{H}^\text{out} \in \mathbb{R}^{N \times d}'
# AST includes Format nodes with different formatting types
```

### Relational Expressions
```python
latex = r'x \leq y + 1'
# AST: Relation(op='\\leq', left=..., right=...)

latex = r'A \subset B \approx C'
# AST: Relation nodes with different operators
```

### Brackets and Grouping
```python
latex = r'(x + y)'
# AST: Bracket(bracket_left='L_PAREN', content=..., bracket_right='R_PAREN')

latex = r'\{x, y\}'
# AST: Bracket with L_BRACE_TEXT and R_BRACE_TEXT

latex = r'[a, b]'
# AST: Bracket with L_BRACKET and R_BRACKET
```

### Lists
```python
latex = r'x, y, z'
# AST: List(items=[...], separator='COMMA')

latex = r'a. b. c'
# AST: List(items=[...], separator='PERIOD')
```

## Project Structure

The `symbol_nav` package contains:

### Core Components

- `interpreter/interpreter.py`: Main parser class `LaTeXMathInterpreter`
- `interpreter/lexer.py`: Lexical analyzer (tokenizer) - defines tokens and tokenization rules
- `interpreter/parser.py`: Syntax parser (grammar rules) - defines grammar and AST construction
- `interpreter/mast.py`: AST node definition (`ASTNode` class and `to_dict` function)
- `interpreter/exceptions.py`: Custom exception classes (`MathSyntaxError`, `MathValueError`)

### Utility Modules

- `extractor.py`: Symbol extraction from AST and LaTeX documents
  - `extract_symbol()`: Extract `SymbolPostfix` nodes from AST
  - `extract_document()`: Extract document structure from LaTeX source
  - `extract_latex_math()`: Extract all math expressions from LaTeX document

- `renderer.py`: AST to LaTeX rendering
  - `to_latex()`: Render AST node to LaTeX source code
  - `to_latex_table()`: Generate LaTeX table from list of symbols

## Error Handling

The parser raises `MathSyntaxError` exceptions for syntax errors, which include:
- Error message
- Token information
- Cursor position indicator

```python
from symbol_nav.interpreter.exceptions import MathSyntaxError, MathValueError

# set debug=True will generate `parser.out` file
interpreter = LaTeXMathInterpreter(debug=True)

try:
    ast = interpreter.parse(latex)
except (MathSyntaxError, MathValueError) as e:
    print(latex)
    print(e.cursor)
    print(e)

    # refer to state definition in `parser.out` for analysis
    print(interpreter.parser.symstack)
    print(interpreter.parser.statestack)
```

### Error Handling

The parser provides detailed error information:

```python
from symbol_nav.interpreter.exceptions import MathSyntaxError, MathValueError

try:
    ast = interpreter.parse(latex)
except MathSyntaxError as e:
    print(f"Syntax error: {e}")
    print(f"Position: {e.cursor}")  # Shows cursor position in source
except MathValueError as e:
    print(f"Value error: {e}")
    print(f"Position: {e.cursor}")
```

## Dependencies

- Python 3.x
- PLY (Python Lex-Yacc)

## License

This project follows MIT License. See LICENSE file for details.