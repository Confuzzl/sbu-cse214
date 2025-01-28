import os
import re

DATA_STRUCTURE_TYPES = {
    "Array": "array",
    "Vector": "dynamic array",
    "Mat2": "2-D matrix",
    "SLL": "SinglyLinkedList",
    "CSLL": "CircularSinglyLinkedList",
    "DLL": "DoublyLinkedList",
    "Stack": "stack",
    "Queue": "queue",
    "Deque": "deque",
    "BST": "BalancedSearchTree",
    "Set": "hash set",
    "Map": "hash map",
    "MinHeap": "min-heap",
    "MaxHeap": "max-heap"
}
# BOLDED_WORDS = ("if", "then", "else", "for", "to", "downto",
#                 "print", "return", "increment", "decrement", "foreach")

# VAR_NAME_REGEX = r"\$(\w*)(\W)"
# FUNCTION_CALL_REGEX = r"!(\w*?)\("
# LEFT_BRACKET_REGEX = r"(\(|\[)"
# RIGHT_BRACKET_REGEX = r"(\)|\])"
# IF_AND_IF_ELSE_REGEX = r"\s*((?:else )*if)\s*\((.*)\)\s*{\s*((?:.*?\n*)*)\s*}"
# ELSE_REGEX = r"\s*else\s*{\s*((?:.*?\n*)*)\s*}"
# ASSIGNMENT_REGEX = r" *[^=]=[^=] *"
# EQUALITY_REGEX = r" *== *"
# COMPARISON_REGEX = r" *(<|<=|>|>=|!=) *"


TUPLE_BRACES = ("<<", ">>")
BRACE_TOKENS = ("[", "]", "(", ")", "{", "}")
BRACE_TOKENS_REGEX = ("\[", "\]", "\(", "\)",
                      "{", "}")
COMPARISON_TOKENS = ("==", "!=", "<", ">", "<=", ">=")
ARITHMETIC_ASSIGNMENT_TOKENS = ("+=", "-=", "*=", "/=")
ARITHMETIC_ASSIGNMENT_TOKENS_REGEX = (r"\+=", "-=", r"\*=", "/=")
SPLIT_TOKENS = (r"\${", "T{", r"\n", r"\.{3}", r"\.", *ARITHMETIC_ASSIGNMENT_TOKENS_REGEX,  *TUPLE_BRACES, *BRACE_TOKENS_REGEX, *COMPARISON_TOKENS,
                "=", ",", ";")


def splitTokenRegex():
    global SPLIT_TOKENS
    return f"({"|".join(SPLIT_TOKENS)})"


data = """Array $a[10]
afafja = afaa
// adada
"""
with open("test.txt") as t:
    data = t.read()

tokens: list[str] = []
for chunk in (chunk for chunk in re.split(r" +", data) if len(chunk) != 0):
    tokens += (token for token in re.split(
        splitTokenRegex(), chunk) if token not in ("", None))
if tokens[len(tokens) - 1] != "\n":
    tokens.append("\n")
print(tokens)

text = ""


def varToken(token: str):
    global text
    text += f"${token}$"


def assignmentToken():
    global text
    text += " $\leftarrow$ "


def numberLiteralToken(token: str):
    global text
    text += token


def tupleBraceToken(token: str):
    global text
    text += r"$\langle$" if token == "<<" else r"$\rangle$"


def comparisonToken(token: str):
    global text
    mappings = ("=", r"\not=", "<", ">", r"\leq", r"\geq")

    text += f" ${mappings[COMPARISON_TOKENS.index(token)]}$ "


def dataTypeToken(token: str):
    global text
    text += f"Create a {DATA_STRUCTURE_TYPES[token]} "


def braceToken(token: str):
    global text

    mappings = {"[": r"\left[", "]": r"\right]",
                "(": r"\left(", ")": r"\right)",
                "{": r"\left\{", "}": r"\right\}"}

    if BRACE_TOKENS.index(token) % 2 == 0:
        text += "$" + mappings[token] + r"\text{"
    else:
        text += r"}" + mappings[token] + "$"


def arithmeticAssignmentToken(var: str, token: str):
    global text
    text += f"$\leftarrow$ {var}$ ${token[0]}$ "


scope_list: list[str] = []

math_scope = 0
text_scope = 0

prev_token = None
for token in tokens:
    if token == "${":
        math_scope = 1
        text += "$"
        continue
    if token == "T{":
        text_scope = 1
        text += r"\text{"
        continue

    if math_scope > 0:
        if token == "{":
            math_scope += 1
        elif token == "}":
            math_scope -= 1
        if math_scope == 0:
            text += "$"
        else:
            text += token
        continue
    if text_scope > 0:
        if token == "{":
            text_scope += 1
        elif token == "}":
            text_scope -= 1
        text += token
        continue

    if (token in ARITHMETIC_ASSIGNMENT_TOKENS):
        arithmeticAssignmentToken(prev_token, token)
    elif (token.startswith("$")):
        varToken(token[1:])
    elif (token == "..."):
        text += r" $\ldots$ "
    elif (token == "="):
        assignmentToken()
    elif (token.isnumeric()):
        numberLiteralToken(token)
    elif (token in (",", ";")):
        text += token + " "
    elif (token in TUPLE_BRACES):
        tupleBraceToken(token)
    elif (token in COMPARISON_TOKENS):
        comparisonToken(token)
    elif (token in DATA_STRUCTURE_TYPES.keys()):
        dataTypeToken(token)
    elif (token in BRACE_TOKENS):
        braceToken(token)
    elif (token in ("&&", "||")):
        text += f" \\textbf{{{"and" if token == "&&" else "or"}}} "
    elif (token == "\n"):
        if text[len(text) - 1] != "\n":
            text += r"\\""\n"
    else:
        text += token

    prev_token = token

print(text)

# def parseIfBody(match: re.Match):
#     out = f"{match.group(1)} ({match.group(2)})\\\\\n"
#     out += "\\begin{tabular}{|l}\n"
#     body = match.group(3)
#     for match in re.finditer(r"\s*(.+)\n*", body):
#         out += f"\t{match.group(1)}\\\\\n"
#     out += "\\end{tabular}\\\\\n"
#     return out

# def parseElseBody(match: re.Match):
#     out = f"else\\\\\n"
#     out += "\\begin{tabular}{|l}\n"
#     body = match.group(1)
#     for match in re.finditer(r"\s*(.+)\n*", body):
#         out += f"\t{match.group(1)}\\\\\n"
#     out += "\\end{tabular}\\\\\n"
#     return out

# new = data
# new = re.sub(VAR_NAME_REGEX, r"$\g<1>$\g<2>", new)
# new = re.sub(ASSIGNMENT_REGEX, r" $\\leftarrow$ ", new)
# new = re.sub(EQUALITY_REGEX, r" $=$ ", new)
# new = re.sub(FUNCTION_CALL_REGEX, r"\\textsc{\g<1>}(", new)

# new = re.sub(r"^Array\s*", "Create an array", new)
# # for my_type, typename in DATA_STRUCTURE_TYPES.items():
# #     print(my_type)
# #     new = re.sub(rf"^{my_type}\s*", f"Create a {typename}", new)

# # new = re.sub(IF_AND_IF_ELSE_REGEX,
# #              parseIfBody, new)
# # new = re.sub(ELSE_REGEX,
# #              parseElseBody, new)

# new = re.sub(LEFT_BRACKET_REGEX,
#              r"$\\left\g<1>\\text{", new)
# new = re.sub(RIGHT_BRACKET_REGEX,
#              r"}\\right\g<1>$", new)

# new = re.sub(COMPARISON_REGEX,
#              r" $\g<1>$ ", new)
# new = re.sub(r"\s*;\s*", "\n", new)

# with open("tex/document.tex", "w") as tex:
#     tex.write(r"""\documentclass[letterpaper]{article}
# \usepackage{enumerate}
# \usepackage{amsmath}
# \usepackage{amssymb}

# \setlength{\parindent}{0pt}

# \begin{document}"""
#               f"{text}"
#               r"""\end{document}""")

# os.chdir("./tex")
# os.system("pdflatex document.tex")
