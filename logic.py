def extract_card_block(lines, name, type_, slot):
    start_line = f'<CARD Name="{name}" Type="{type_}" Bus="R" Slot="{slot}">'
    start_idx = -1
    end_idx = -1

    for i, line in enumerate(lines):
        if start_line in line:
            start_idx = i
            break

    if start_idx == -1:
        return None  # not found

    for j in range(start_idx + 1, len(lines)):
        if '<CARD Name="' in lines[j] and j != start_idx:
            end_idx = j
            break

    if end_idx == -1:
        end_idx = len(lines)

    return lines[start_idx:end_idx]

def replace_card_block(dest_lines, name, type_, slot, new_block):
    start_line = f'<CARD Name="{name}" Type="{type_}" Bus="R" Slot="{slot}">'
    start_idx = -1
    end_idx = -1

    for i, line in enumerate(dest_lines):
        if start_line in line:
            start_idx = i
            break

    if start_idx == -1:
        return None

    for j in range(start_idx + 1, len(dest_lines)):
        if '<CARD Name="' in dest_lines[j] and j != start_idx:
            end_idx = j
            break

    if end_idx == -1:
        end_idx = len(dest_lines)

    return dest_lines[:start_idx] + new_block + dest_lines[end_idx:]
