from pathlib import Path

vars = {}
TRANSLATE_NUMBERS = {
    "𒐇": 9,
    "𒌋𒁹𒁹": 12,
    "𒌋𒌋": 20,
    "𒌋𒌋𒁹": 21
}
TRANSLATE_NUMBERS_LATIN = {value: key for key, value in TRANSLATE_NUMBERS.items()}

LATIN_TRANSLATE = {
    "𒋫": "ta",
    "𒌝": "um",
    "𒋗": "šu",
    "𒆠": "kī",
    "𒈠": "ma",
    "𒂵": "ga"
}

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
    print("PRINT: " + p + " (" + translated_p.strip() + ")")

def add_tokens(tokens, depth):
    # print("add function detected")
    a_val = vars[tokens[depth - 1]]
    b_val = vars[tokens[depth + 1]]
    return a_val + b_val

def equal_tokens(a_val, b_val):
    print(str(a_val) + " - " + str(b_val))
    if a_val in TRANSLATE_NUMBERS:
        a_val = TRANSLATE_NUMBERS[a_val]
    if b_val in TRANSLATE_NUMBERS:
        b_val = TRANSLATE_NUMBERS[b_val]
    if int(a_val) == int(b_val):
        return True
    else:
        return False

def run_function(function):
    prints = []
    line_split = function.split("\n")
    line_num = -1
    while line_num < len(line_split) - 1:
        line_num += 1
        tokens = []
        line = line_split[line_num]
        print("line: " + line.strip("    "))
        func_split = line.split("\n")
        for split in func_split:
            # print("split: " + split)
            if split.strip("\n") is "" or None:
                func_split.remove(split)
            for token in split.split(" "):
                if token is "" or None:
                    continue
                else:
                    tokens.append(token.strip("\n"))
        in_string = False
        depth = 0
        print("NEW LINE")
        print(tokens)
        for parsed_token in tokens:
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

                if parsed_token == "𒋗":
                    # print("equals function detected")
                    a_val = tokens[depth - 1]
                    if a_val[-1] != "𒌝":
                        print("ERROR: Invalid variable initialisation. "
                              "Please use correct Akkadian grammar and add 𒌝 to the end of the variable name.")
                        exit()
                    b_val = tokens[depth + 1]
                    if b_val in TRANSLATE_NUMBERS:
                        b_val = TRANSLATE_NUMBERS[b_val]
                    if tokens[len(tokens) - 1] == "𒉿𒍝𒁍":
                        print("𒉿𒍝𒁍 detected")
                        added_tokens = add_tokens(tokens, depth - 2)
                        vars.update({a_val: added_tokens})
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
                    print("tokens[max_depth - min_depth + 1] " + tokens[max_depth - min_depth + 1])
                    if tokens[max_depth - min_depth + 1] == "𒄿𒈾":
                        print("𒄿𒈾 detected")
                        print_var = tokens[max_depth - min_depth + 2]
                        print_val = vars[tokens[max_depth - min_depth + 4]]
                        if print_val in TRANSLATE_NUMBERS_LATIN:
                            print_val = TRANSLATE_NUMBERS_LATIN[print_val]
                        new_print = new_print.replace(print_var, str(print_val))

                    prints.append(new_print)

                # if
                if parsed_token == "𒋳𒈠":
                    print("parsed 𒋳𒈠 // if")
                    if tokens[len(tokens) - 1] == "𒄿𒈠𒊍𒊩":
                        bool_result = equal_tokens(vars[tokens[len(tokens) - 3]], tokens[len(tokens) - 2])
                        if bool_result is False:
                            print("if not bool_result")
                            line_num += 1
                        else:
                            print("if bool_result")
                            continue
            depth += 1
    print("")
    for p in prints:
        cunei_print(p)


if __name__ == '__main__':
    current_dir = Path(__file__).resolve().parent
    program_loc = current_dir / "program.txt"
    file = open(program_loc, "r")

    with open(program_loc, encoding="utf-8") as f:
        src = f.read()
        # print(src)
        src_split = src.split(" ")
        for token in src_split:
            if token == "𒀀𒁍𒌅":
                print("𒀀𒁍𒌅")
                print("")
                run_function(src.split("𒐕")[1])

    print("")
    print("VAR RESULTS:")
    for var, val in vars.items():
        if val in TRANSLATE_NUMBERS_LATIN:
            val = TRANSLATE_NUMBERS_LATIN[val]
        cunei_print(str(var) + " 𒋗 " + str(val))
