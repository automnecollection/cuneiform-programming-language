from pathlib import Path

from cuneiform_script import *

vars = {}

FUNCTIONS = [
    "𒉿𒍝𒁍"  # to write
]

def cunei_print(p):
    translated_p = ""
    tokens = p.split(" ")
    word_num = 0
    for word in tokens:
        if word in TRANSLATE_NUMBERS:
            tokens[word_num] = str(TRANSLATE_NUMBERS[word])
        word_num += 1
    for word in tokens:
        for letter in word:
            if letter in LATIN_TRANSLATE:
                translated_p += LATIN_TRANSLATE[letter]
            else:
                translated_p += letter
        translated_p += " "
    print("   " + p + " (" + translated_p.strip() + ")")

def math_tokens(a_val, b_val, math_type):
    if a_val in vars:
        a_val = vars[a_val]
    if b_val in vars:
        b_val = vars[b_val]
    if math_type == "add":
        return int(a_val) + int(b_val)
    if math_type == "sub":
        return int(a_val) - int(b_val)

def equal_tokens(a_val, b_val):
    print(str(a_val) + " - " + str(b_val))
    if a_val in vars:
        a_val = vars[a_val]
    if b_val in vars:
        b_val = vars[b_val]
    if a_val in TRANSLATE_NUMBERS:
        a_val = TRANSLATE_NUMBERS[a_val]
    if b_val in TRANSLATE_NUMBERS:
        b_val = TRANSLATE_NUMBERS[b_val]
    if int(a_val) == int(b_val):
        return True
    else:
        return False

def run_function(function):
    line_split = function.split("\n")
    line_num = -1
    while line_num < len(line_split) - 1:
        line_num += 1
        tokens = []
        line = line_split[line_num]
        print("new line: " + line.strip("    "))
        func_split = line.split("\n")
        for split in func_split:
            if split.strip("\n") is "" or None:
                func_split.remove(split)
            for token in split.split(" "):
                if token is "" or None:
                    continue
                else:
                    tokens.append(token)

        run_tokens(tokens, function, line_num)

def run_tokens(tokens, function, line_num):
    prints = []
    in_string = False
    depth = 0
    # print(tokens)
    for parsed_token in tokens:
        if parsed_token == " ":
            continue
        # print("TOKEN: " + str(parsed_token) + ", DEPTH: " + str(depth))
        # TODO: Construct the string here
        if parsed_token == "𐏐".strip(" "):
            in_string = True
        if parsed_token == "𒀺".strip(" "):
            # print("we are now not in string")
            in_string = False

        if not in_string:
            # if parsed_token == "𒉿𒍝𒁍":
            # a_val, b_val = add_tokens(tokens, depth)
            # tokens[depth] = a_val + b_val
            if parsed_token == "#":
                continue

            # free var
            if parsed_token == "𒉿𒍑𒋗𒊒𒌝":
                if tokens[depth - 1][-1] != "𒄠":
                    print(f"Line {line_num}: {tokens} - ERROR: Expected accusative case")
                    exit()
                else:
                    vars.__delitem__(tokens[depth - 1].replace("𒄠", "𒌝"))
            if parsed_token == "𒋗":
                # print("equals function detected")
                # print("tokens[depth] " + tokens[depth])
                a_val = tokens[depth - 1]
                if a_val[-1] != "𒌝":
                    print("A_VAL: " + a_val)
                    print("ERROR: Invalid variable initialisation. "
                          "Please use correct Akkadian grammar and add 𒌝 to the end of the variable name.")
                    exit()
                b_val = tokens[depth + 1]
                if b_val in TRANSLATE_NUMBERS:
                    b_val = TRANSLATE_NUMBERS[b_val]
                if tokens[len(tokens) - 1] == "𒉿𒍝𒁍":
                    # print("𒉿𒍝𒁍 detected")
                    added_tokens = math_tokens(tokens[depth - 4], tokens[depth - 3], "add")
                    vars.update({a_val: added_tokens})
                    continue
                elif tokens[len(tokens) - 1] == "sub":
                    # print("sub detected")
                    subbed_tokens = math_tokens(tokens[depth - 4], tokens[depth - 3], "sub")
                    vars.update({a_val: subbed_tokens})
                    continue
                else:
                    vars.update({a_val: b_val})

            if parsed_token == "𒋗𒇬":
                new_print = ""
                # print("print function detected")
                # printed_val = vars[tokens[depth - 2]]
                new_depth = 1
                sep_found = False
                while not sep_found:
                    if tokens[depth - new_depth] != "𐏐":
                        new_depth += 1
                    else:
                        sep_found = True
                min_depth = depth - new_depth
                max_depth = 1
                max_found = False
                while not max_found and max_found < len(tokens) - 1:
                    if tokens[min_depth + max_depth] != "𒀺":
                        max_depth += 1
                    else:
                        # print("max_found")
                        max_found = True
                    # if not max_found:
                    #     print("ERROR: Expected '𒀺'")
                    #     exit()
                print_depth = 1
                done_printing = False
                while not done_printing:
                    # print(print_depth)
                    # if tokens[scnd_min_depth + print_depth] in vars:
                    # tokens[scnd_min_depth + print_depth] = vars[tokens[scnd_min_depth + print_depth]]
                    new_print += str(tokens[min_depth + print_depth])
                    if tokens[min_depth + print_depth + 1] != "𒀺":
                        new_print += " "
                    else:
                        done_printing = True
                    print_depth += 1
                    # print(new_print)

                # print("what")
                # print("tokens[max_depth - min_depth + 1] " + tokens[max_depth - min_depth + 1])
                if tokens[max_depth - min_depth + 1] == "𒄿𒈾":
                    # print("𒄿𒈾 detected")
                    print_var = tokens[max_depth - min_depth + 2]
                    print_val = vars[tokens[max_depth - min_depth + 4].replace("𒅎", "𒌝")]
                    if print_val in TRANSLATE_NUMBERS_LATIN:
                        print_val = TRANSLATE_NUMBERS_LATIN[print_val]
                    new_print = new_print.replace(print_var, str(print_val))

                prints.append(new_print)

            # while
            if parsed_token == "𒀀𒁲":
                # print("parsed 𒀀𒁲 // while")

                bool_line_depth = 0
                bool_result = False
                if tokens[len(tokens) - 1] == "𒄿𒈠𒊍𒊩":
                    if tokens[len(tokens) - 2] == "𒆷":
                        # print("parsed 𒆷 𒄿𒈠𒊍𒊩 // not equals")
                        bool_result = equal_tokens(tokens[len(tokens) - 4], tokens[len(tokens) - 3])
                        if bool_result:
                            bool_result = False
                        else:
                            bool_result = True
                    else:
                        # print("parsed 𒄿𒈠𒊍𒊩 // equals")
                        bool_result = equal_tokens(tokens[len(tokens) - 3], tokens[len(tokens) - 2])
                orig_line = line_num
                while bool_result:
                    # print("true bool_result")
                    # print("")
                    # print("FUNCTION SPLIT: ")
                    # print(bool_line_depth)
                    # print(len(function.split("\n")))
                    if line_num + bool_line_depth < int(len(function.split("\n")) - line_num + 2):
                        # print(function.split("\n")[line_num + bool_line_depth].replace("        ", ""))
                        run_tokens(function.split(" ")[line_num + bool_line_depth].replace("        ", ""),
                                   function, line_num)
                        bool_result = equal_tokens(tokens[len(tokens) - 3], tokens[len(tokens) - 2])
                        line_num += 1
                        bool_line_depth += 1
                        print(bool_result)
                        # print(bool_line_depth)
                    else:
                        line_num = orig_line
            # if
            if parsed_token == "𒋳𒈠":
                bool_result = None

                if tokens[len(tokens) - 1] == "𒄿𒈠𒊍𒊩":
                    # print("parsed 𒄿𒈠𒊍𒊩 // equals")
                    bool_result = equal_tokens(vars[tokens[len(tokens) - 3]], tokens[len(tokens) - 2])

                # print("parsed 𒋳𒈠 // if")
                if tokens[len(tokens) - 1] == "𒄿𒈠𒊍𒊩":
                    # print("parsed 𒄿𒈠𒊍𒊩 // equals")
                    bool_result = equal_tokens(vars[tokens[len(tokens) - 3]], tokens[len(tokens) - 2])
                if tokens[len(tokens) - 1] == "gr_than":
                    if vars[tokens[len(tokens) - 3]] > tokens[len(tokens) - 2]:
                        bool_result = True
                    else:
                        bool_result = False
                if tokens[len(tokens) - 1] == "ls_than":
                    if vars[tokens[len(tokens) - 3]] < tokens[len(tokens) - 2]:
                        bool_result = True
                    else:
                        bool_result = False

                if bool_result is False:
                    # print("if not bool_result")
                    line_num += 1
                elif bool_result is False:
                    # print("if bool_result")
                    continue
                elif bool_result is None:
                    print("ERROR: bool_result returned none")
                    exit()

            # if parsed_token == "𒀺":
            #     continue
        depth += 1
    # print("")
    for p in prints:
        cunei_print(p)


if __name__ == '__main__':
    current_dir = Path(__file__).resolve().parent
    program_loc = current_dir / "mesopotamian_city_simulator.txt"
    file = open(program_loc, "r")

    with open(program_loc, encoding="utf-8") as f:
        src = f.read()
        # print(src)
        src_split = src.split("\n")
        for token in src_split:
            if token == "𒀀𒁍𒋾𒅎 𒌨𒊑𒌓 𒐕":
                # print("got " + token)
                run_function(src.split("𒐕")[1])
            # else:
                # print("did not get " + token)

    print("")
    print("VAR RESULTS:")
    for var, val in vars.items():
        if val in TRANSLATE_NUMBERS_LATIN:
            val = TRANSLATE_NUMBERS_LATIN[val]
        cunei_print(str(var) + " 𒋗 " + str(val))
