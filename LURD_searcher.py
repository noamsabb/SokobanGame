import re


def found_LURD(fileName):
    string_builder = []

    first_move_skipped = False
    move_pattern = re.compile(r"move\s*=\s*(.*)")
    p_move_pattern = re.compile(r"p_(.*)")

    with open(fileName, "r") as file:
        for line in file:

            if '-- Loop starts here' in line:
                break
            # Search for the move pattern in the current line
            match = move_pattern.search(line)
            if match:
                # Skip the first move
                if not first_move_skipped:
                    first_move_skipped = True
                    continue
                # Extract the move part
                move = match.group(1).strip()

                # Check if the move matches 'p_*' pattern
                p_match = p_move_pattern.match(move)
                if p_match:
                    # Extract only the '*' part from 'p_*'
                    move = p_match.group(1).strip()

                # Add the move to the list
                string_builder.append(move)

    LURD_str = "{" + ','.join(string_builder) + "}"

    return LURD_str
