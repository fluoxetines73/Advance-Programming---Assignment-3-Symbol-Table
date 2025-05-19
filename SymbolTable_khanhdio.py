from StaticError import *
from Symbol import *
from functools import *

# Kiểm tra tên biến: bắt đầu bằng chữ thường, theo sau là chữ, số hoặc _
def is_valid_identifier(s):
    return (
        len(s) > 0 and
        s[0].islower() and
        all(c.islower() or c.isupper() or c.isdigit() or c == '_' for c in s)
    )

def find_symbol(state, name):
    total = len(state)
    result = list(filter(lambda pair: name in pair[1], enumerate(state)))
    return None if not result else (total - 1 - result[0][0], result[0][1][name])


def get_value_type(state, value, full_cmd):
    # Hằng số: tất cả là số
    if all(c.isdigit() for c in value):
        return "number"

    # Hằng chuỗi: bắt đầu và kết thúc bằng dấu '
    if (
        len(value) >= 2 and
        value[0] == "'" and value[-1] == "'" and
        all(c.isalnum() for c in value[1:-1])
    ):
        return "string"

    # Nếu không phải hằng, thì phải là danh hiệu đã khai báo
    if not is_valid_identifier(value):
        raise InvalidInstruction(full_cmd)

    symbol_info = find_symbol(state, value)
    if symbol_info is None:
        raise Undeclared(full_cmd)

    return symbol_info[1].typ


def simulate(list_of_commands):
    """
    Executes a list of commands and processes them sequentially.

    Args:
        list_of_commands (list[str]): A list of commands to be executed.

    Returns:
        list[str]: A list of return messages corresponding to each command.
    """

    print("list_of_commands = ", list_of_commands)
    
    def step(state_result, command):
        (state, output_list) = state_result
        try:
            new_state, result = handle_command(state, command)
            return (new_state, output_list + ([result] if result is not None else []))
        except StaticError as e:
            if isinstance(e, UnknownBlock):
                raise UnknownBlock()
            raise type(e)(f"{command}")

    final_state, result = reduce(step, list_of_commands, (initial_state(), []))
    if len(final_state) > 1:
        raise UnclosedBlock(len(final_state) - 1)
    return result


# Khởi tạo bảng ghi: danh sách các scope (block), mỗi block là dict
def initial_state():
    return [{}]  # scope level 0

# Xử lý từng lệnh cụ thể
def handle_command(state, command):
    tokens = command.split(" ")
    cmd = tokens[0]
    valid_commands = {"INSERT", "ASSIGN", "LOOKUP", "BEGIN", "END", "PRINT", "RPRINT"}
    # Check if command starts with a valid keyword
    print("cmd = ", cmd)
    if cmd not in valid_commands:
        print("cmd = ", cmd)
        raise InvalidInstruction("Invalid command")

    # Validate token count for each command
    if cmd in {"BEGIN", "END", "PRINT", "RPRINT"} and len(tokens) != 1:
        raise InvalidInstruction(f"Invalid: {command}")
    elif cmd == "LOOKUP" and len(tokens) != 2:
        raise InvalidInstruction(f"Invalid: {command}")
    elif cmd in {"INSERT", "ASSIGN"} and len(tokens) != 3:
        raise InvalidInstruction(f"Invalid: {command}")

    # Process valid commands
    if cmd == "INSERT":
        return handle_insert(state, tokens, command)
    elif cmd == "ASSIGN":
        return handle_assign(state, tokens, command)
    elif cmd == "LOOKUP":
        return handle_lookup(state, tokens, command)
    elif cmd == "BEGIN":
        return ([{}] + state, None)
    elif cmd == "END":
        if len(state) == 1:
            raise UnknownBlock()
        return (state[1:], None)
    elif cmd == "PRINT":
        return (state, print_scope(state))
    elif cmd == "RPRINT":
        return (state, rprint_scope(state))



def handle_insert(state, tokens, full_cmd):
    if len(tokens) != 3:
        raise InvalidInstruction(full_cmd)

    name, typ = tokens[1], tokens[2]


    if not is_valid_identifier(name):
        raise InvalidInstruction(full_cmd)

    if typ not in ["number", "string"]:
        raise InvalidInstruction(full_cmd)

    current_scope = state[0]

    if name in current_scope:
        raise Redeclared(full_cmd)

    new_symbol = Symbol(name, typ)
    new_scope = {**current_scope, name: new_symbol}
    return ([new_scope] + state[1:], "success")

def handle_assign(state, tokens, full_cmd):
    if len(tokens) != 3:
        raise InvalidInstruction(full_cmd)

    name, value = tokens[1], tokens[2]

    # Kiểm tra tên danh hiệu bên trái có hợp lệ không
    def is_valid_identifier(s):
        return (
            len(s) > 0 and
            s[0].islower() and
            all(c.islower() or c.isupper() or c.isdigit() or c == '_' for c in s)
        )

    if not is_valid_identifier(name):
        raise InvalidInstruction(full_cmd)
    
    def find_symbol(state, name):
        result = list(filter(lambda pair: name in pair[1], enumerate(state)))
        return None if not result else (result[0][0], result[0][1][name])

    # Tìm danh hiệu bên trái trong bảng ghi
    lhs_symbol_info = find_symbol(state, name)
    if lhs_symbol_info is None:
        raise Undeclared(full_cmd)

    lhs_symbol = lhs_symbol_info[1]  # Symbol object
    lhs_type = lhs_symbol.typ

    # Xác định kiểu của value
    value_type = get_value_type(state, value, full_cmd)

    if lhs_type != value_type:
        raise TypeMismatch(full_cmd)

    return (state, "success")

def handle_lookup(state, tokens, full_cmd):
    if len(tokens) != 2:
        raise InvalidInstruction(full_cmd)

    name = tokens[1]

    if not is_valid_identifier(name):
        raise InvalidInstruction(full_cmd)

    symbol_info = find_symbol(state, name)
    if symbol_info is None:
        raise Undeclared(full_cmd)

    level = symbol_info[0]
    return (state, str(level))

def print_scope(state):
    def collect(scopes, index, acc):
        return acc if index >= len(scopes) else collect(
            scopes,
            index + 1,
            reduce(
                lambda d, name: d | {name: len(state) - 1 - index} if name not in d else d,
                scopes[index].keys(),
                acc
            )
        )

    def print_level(level, max_level):
        return [] if level > max_level else print_symbols(level, 0) + print_level(level + 1, max_level)

    def print_symbols(level, index):
        keys = list(state[len(state) - 1 - level].keys())
        return [] if index >= len(keys) else (
            [f"{keys[index]}//{level}"] + print_symbols(level, index + 1)
            if name_to_level.get(keys[index], -1) == level else
            print_symbols(level, index + 1)
        )

    name_to_level = collect(state, 0, {})
    result = print_level(0, len(state) - 1)
    return " ".join(result) if result else ""

def rprint_scope(state):
    def collect_symbols_with_levels(scopes, level, seen_symbols):
        if level < 0:
            return []
        
        current_scope = scopes[len(scopes) - 1 - level]
        
        def process_names(names_list, seen, acc):
            if not names_list:
                return acc
            
            name = names_list[0]
            rest = names_list[1:]
            
            if name in seen:
                return process_names(rest, seen, acc)
            else:
                return process_names(rest, seen | {name}, acc + [(name, level)])
        
        names = list(current_scope.keys())
        current_level_symbols = process_names(names, seen_symbols, [])
        
        return collect_symbols_with_levels(scopes, level - 1, seen_symbols | set(name for name, _ in current_level_symbols)) + current_level_symbols
    
    symbol_info = collect_symbols_with_levels(state, len(state) - 1, set())
    
    def format_symbols(symbols):
        if not symbols:
            return []
        name, level = symbols[0]
        return [f"{name}//{level}"] + format_symbols(symbols[1:])
    
    reversed_symbols = list(reversed(symbol_info))
    result = format_symbols(reversed_symbols)
    
    return " ".join(result) if result else ""


