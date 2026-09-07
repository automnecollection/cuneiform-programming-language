from pathlib import Path

from cuneiform_script import *

vars = {}
struct_vars = [{}]
struct_vars_num = 0

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
        word_len = len(word)

        for letter_index, letter in enumerate(word):
            if letter in LATIN_TRANSLATE:
                translated_p += LATIN_TRANSLATE[letter]
            else:
                translated_p += letter
            if letter_index < word_len - 1:
                translated_p += "-"
        translated_p += " "
    latin_translation = translated_p.strip()
    latin_translation = latin_translation.replace("aa", "a")
    latin_translation = latin_translation.replace("ii", "i")
    latin_translation = latin_translation.replace("uu", "u")
    # print("   " + p + " (" + latin_translation + ")")
    print(p + " (" + latin_translation + ")")

def math_tokens(a_val, b_val, math_type):
    if a_val in vars:
        a_val = vars[a_val]
    else:
        print("    " + a_val + " is NOT IN VARS VITCH")
    if b_val in vars:
        b_val = vars[b_val]
    if math_type == "add":
        print("    " + a_val + " + " + b_val)
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
    tok_dicts = []
    prints = []
    line_split = function.split("\n")
    line_num = -1
    while line_num < len(line_split) - 1:
        line_num += 1
        tokens = []
        # nominative, accusative, genitive
        previous_unparsed_token_type = ""
        line = line_split[line_num]
        print("new line: " + line.strip("    "))
        func_split = line.split("\n")
        for split in func_split:
            if not split.__contains__("#"):
                if split.strip("\n") is "" or None:
                    func_split.remove(split)
                for token in split.split(" "):
                    if token is "" or None:
                        continue
                    else:
                        tokens.append(token)
            else:
                func_split.remove(split)

        new_dict = None
        if tokens is not []:
            new_dict, prints, line_num = create_token_dictionaries(tokens, function, line_num)
        for dict in new_dict:
            tok_dicts.append(dict)
        print("")

    return tok_dicts, prints

def create_token_dictionaries(tokens, function, line_num):
    in_string = False
    depth = 0

    tok_dict = []

    new_print = ""
    nominative = ""
    nominative_depth_index = None

    scnd_nominative = ""
    accusative = ""

    searched_for_verb = False
    verb_found = False

    print("line num: " + str(line_num + 1) + ", TOKENS BEING RUN: " + str(tokens))
    for parsed_token in tokens:
        if parsed_token == " ":
            continue
        print("TOKEN: " + str(parsed_token) + ", DEPTH: " + str(depth))
        # print("new_print: " + new_print)
        # print("in_string: " + str(in_string))

        # string making
        if not in_string and new_print is not "":
            new_print = new_print[:-1]
            tok_dict.append({
                "verb": "print",
                "accusative": str(new_print)
            })
            print("    NEW PRINT:" + str(tok_dict))
            prints.append(new_print)
            new_print = ""
            depth += 1
            continue
        elif in_string:
            if parsed_token == "𒀺".strip(" "):
                in_string = False
                depth += 1
                continue
            new_print += str(tokens[depth]) + " "
            depth += 1
            continue
        elif parsed_token == "𐏐".strip(" "):
            in_string = True
            depth += 1
            continue
        # brok
        elif new_print is not "":
            print(f"ERROR: We have a print '{new_print}' and we do not know what the fuck to do with it.")

        if parsed_token[0] not in LATIN_TRANSLATE:
            depth += 1
            continue

        if len(parsed_token) > 1:
            if LATIN_TRANSLATE[parsed_token[-1]][-2:] == "um":
                if nominative is "":
                    nominative = parsed_token
                    nominative_depth_index = depth
                    print("    got nominative - " + nominative)
                elif scnd_nominative is "":
                    scnd_nominative = parsed_token
                    print("    got scnd_nominative - " + scnd_nominative)
                # else:
                    # print("    ERROR: Well what the fock is this then? A mystery nominative on our hands?")
                    # exit()

        print(f"depth, len tokens: {depth} {len(tokens) - 1}")
        if depth + 1 == len(tokens):
            searched_for_verb = True

        if searched_for_verb and not verb_found:
            if nominative and not scnd_nominative:
                print(tokens)
                print(parsed_token)
                print(depth)
                print(nominative_depth_index)
                scnd_nominative = tokens[nominative_depth_index + 1]
            new_var = {nominative: scnd_nominative}
            tok_dict.append({
                "verb": "var_equal",
                "nominative": str(nominative),
                "scnd_nominative": str(scnd_nominative)
            })
            vars.update(new_var)
            print("    NEW VAR: " + str(new_var))
            nominative, scnd_nominative = "", ""

        depth += 1

    return tok_dict, prints, line_num


if __name__ == '__main__':
    current_dir = Path(__file__).resolve().parent
    # "mesopotamian_city_simulator.txt", "fibonacci.txt", "simple.txt"
    program_loc = current_dir / "examples" / "simple.txt"
    file = open(program_loc, "r")

    tok_dicts = []
    prints = []
    with open(program_loc, encoding="utf-8") as f:
        src = f.read()
        # print(src)
        src_split = src.split("\n")
        for token in src_split:
            if token == "𒀀𒁍𒋾𒅎 𒌨𒊑𒌓 𒐕":
                # print("got " + token)
                tok_dicts, prints = run_function(src.split("𒐕")[1])
            # else:
                # print("did not get " + token)
    print("DICT RESULTS:")
    for d in tok_dicts:
        if d is {}:
            print("WTF????")
        else:
            print("    " + str(d))
    print("")
    print("PRINT RESULTS:")
    for p in prints:
        cunei_print("    " + p)
    print("")
    print("VAR RESULTS:")
    for var, val in vars.items():
        if val in TRANSLATE_NUMBERS_LATIN:
            val = TRANSLATE_NUMBERS_LATIN[val]
        cunei_print("    " + str(var) + " 𒋗 " + str(val))

    print("")
    print("STRUCT RESULTS:")
    for struct in struct_vars:
        for var, var_val in struct.items():
            for scnd_var, val in var_val.items():
                cunei_print(str(var).replace("𒌝", "𒅎") + " " + str(scnd_var) + " 𒋗 " + str(val))
