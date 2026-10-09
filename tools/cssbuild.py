"""Builds the single inline stylesheet: landing CSS (tools/home.css) + the reader subset of assets/css/quran.min.css."""
import re

DROP = re.compile(r"\.(hero|btn|foot|wm)\b")  # widget parts the in-page reader does not use


def _strip(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S).replace("\r", "")


def split_blocks(text):
    out, depth, start = [], 0, 0
    for i, ch in enumerate(text):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append(text[start:i + 1].strip())
                start = i + 1
    return [x for x in out if x]


def filter_rule(block):
    head, body = block.split("{", 1)
    if head.strip().startswith("@media"):
        if "print" in head:
            return ""
        inner = "".join(filter_rule(b) for b in split_blocks(body.rsplit("}", 1)[0]))
        return head + "{" + inner + "}" if inner else ""
    sels = [s for s in head.split(",") if not DROP.search(s)]
    return ",".join(sels) + "{" + body if sels else ""


def mini(css):
    css = re.sub(r"\s*\n\s*", "", _strip(css))
    return re.sub(r"\s*([{};,>])\s*", r"\1", css).replace(";}", "}")


def build(home_css_path, widget_css_path):
    home = open(home_css_path, encoding="utf8").read()
    w = _strip(open(widget_css_path, encoding="utf8").read())
    w = "".join(filter_rule(b) for b in split_blocks(w))
    old = 'font-family:"Amiri","Traditional Arabic",serif;text-align:right;font-weight:600'
    assert old in w, "widget .arab rule changed; update cssbuild.py"
    # only Amiri Regular is shipped, so never ask for a synthetic bold
    w = w.replace(old, "font-family:var(--ar);text-align:right;font-weight:400")
    return mini(home) + mini(w)
