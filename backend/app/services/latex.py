import re
from pathlib import Path

def replace_after_anchor(tex: str, anchor: str, new_line: str) -> str:
    # replace the first non-empty line after the anchor comment
    pattern = rf"(%==ANCHOR:{re.escape(anchor)}==\s*\n)([^\n]*\n)"
    return re.sub(pattern, rf"\1{new_line}\n", tex, count=1)

def replace_block(tex: str, start_anchor: str, end_anchor: str, new_block: str) -> str:
    pattern = rf"(%==ANCHOR:{re.escape(start_anchor)}==\s*\n)(.*?)(%==ANCHOR:{re.escape(end_anchor)}==)"
    return re.sub(pattern, rf"\1{new_block}\n\3", tex, flags=re.S)

def inject_projects(tex: str, slots: list[dict]) -> str:
    # slots: [{title_line:str, bullets:[str,str,str]}, ...]
    for idx, slot in enumerate(slots, start=1):
        tex = replace_after_anchor(tex, f"PROJ:SLOT{idx}:TITLE", slot["title_line"])
        for b_idx, bullet in enumerate(slot["bullets"], start=1):
            tex = replace_after_anchor(tex, f"PROJ:SLOT{idx}:B{b_idx}", rf"\resumeItem{{{bullet}}}")
    return tex
