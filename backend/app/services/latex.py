import re

def replace_after_anchor(tex: str, anchor: str, new_line: str) -> str:
    # Find the anchor line, then replace the *next* line after it
    pattern = rf"(^.*{re.escape(anchor)}.*\n)([^\n]*\n)"
    return re.sub(
        pattern,
        lambda m: m.group(1) + new_line + "\n",
        tex,
        count=1,
        flags=re.MULTILINE,
    )

def inject_projects(tex: str, slots: list[dict]) -> str:
    for idx, slot in enumerate(slots, start=1):
        tex = replace_after_anchor(tex, f"PROJ:SLOT{idx}:TITLE", slot["title_line"])
        for bidx, bline in enumerate(slot["bullet_lines"], start=1):
            # Wrap bullet in \resumeItem{} command for proper formatting
            formatted_bullet = r"\resumeItem{" + bline + "}"
            tex = replace_after_anchor(tex, f"PROJ:SLOT{idx}:B{bidx}", formatted_bullet)
    return tex

def build_final_tex(base_tex: str, patches: list) -> str:
    """Build final LaTeX from patches with user decisions"""
    from collections import defaultdict
    
    # Group patches by project
    project_patches = defaultdict(list)
    for patch in patches:
        # Handle both dict and Pydantic model
        if hasattr(patch, 'project_key'):
            project_patches[patch.project_key].append(patch)
        else:
            project_patches[patch.get("project_key", "")].append(patch)
    
    # Build slots from patches
    slots = []
    slot_idx = 1
    for proj_key, patch_list in project_patches.items():
        if not patch_list:
            continue
        
        # Get project info from first patch
        first_patch = patch_list[0]
        if hasattr(first_patch, 'project_title'):
            project_title = first_patch.project_title
            date_range = getattr(first_patch, 'project_date_range', '')
        else:
            project_title = first_patch.get("project_title", "")
            date_range = first_patch.get("project_date_range", "")
        
        # Build title line
        title_line = r"{\textbf{" + project_title + r": }}\hfill \textit{\textbf{" + date_range + r"}}"
        
        bullet_lines = []
        for patch in patch_list:
            # Determine which text to use
            if hasattr(patch, 'accepted'):
                accepted = patch.accepted
                edited_text = getattr(patch, 'edited_text', None)
                original = patch.original
                rewritten = patch.rewritten
            else:
                accepted = patch.get("accepted")
                edited_text = patch.get("edited_text")
                original = patch.get("original", "")
                rewritten = patch.get("rewritten", "")
            
            if accepted is False:
                # Rejected - use original
                bullet_lines.append(original)
            elif edited_text:
                # Manually edited
                bullet_lines.append(edited_text)
            elif accepted is True:
                # Accepted rewritten version
                bullet_lines.append(rewritten)
            else:
                # Default to rewritten if no decision
                bullet_lines.append(rewritten)
        
        slots.append({
            "slot_idx": slot_idx,
            "title_line": title_line,
            "bullet_lines": bullet_lines
        })
        slot_idx += 1
    
    # Inject into template
    tex = base_tex
    for slot in slots:
        idx = slot["slot_idx"]
        tex = replace_after_anchor(tex, f"PROJ:SLOT{idx}:TITLE", slot["title_line"])
        for bidx, bline in enumerate(slot["bullet_lines"], start=1):
            # Wrap bullet in \resumeItem{} command for proper formatting
            formatted_bullet = r"\resumeItem{" + bline + "}"
            tex = replace_after_anchor(tex, f"PROJ:SLOT{idx}:B{bidx}", formatted_bullet)
    
    return tex
