from operator import itemgetter

ARGUMENT_PREFIX = '--'

def parse_arguments(arguments, argument_list):
    parse_stack = []
    parsed = {}
    argument_order = {argument: index
                      for index, argument in enumerate(argument_list)}
    for argument in arguments:
        if argument.startswith(ARGUMENT_PREFIX):
            tokenized_argument = argument[len(ARGUMENT_PREFIX):]
            if tokenized_argument in argument_list:
                parse_stack.append(tokenized_argument)
        elif len(parse_stack) > 0:
            key = parse_stack.pop()
            parsed[key] = (argument, argument_order[key])
    if len(parsed) < len(argument_list):
        needed_arguments = set(argument_list) - set(parsed.keys())
        initialized = {k: (v, argument_order[k])
                       for k, v in zip(
                               needed_arguments,
                               [None for _ in range(len(needed_arguments))])}
        parsed.update(initialized)
    in_sorted_order = sorted(parsed.values(), key=itemgetter(1))
    return [parsed_value[0] for parsed_value in in_sorted_order]
