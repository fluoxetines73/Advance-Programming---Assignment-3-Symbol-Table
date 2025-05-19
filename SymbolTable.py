from StaticError import *
from Symbol import *
from functools import *

def invalid_command(sym_table, lst_of_commands, command):
    """
    Hàm chỉ được gọi khi không tìm thấy lệnh nào trong danh sách lệnh đã định nghĩa.

    Args:
        sym_table (list[dict]): Danh sách các scope. (dummy)
        lst_of_commands (list[str]): Danh sách các lệnh. (dummy)

    Raises:
        Invalid: Invalid command
    """
    raise StaticError(InvalidInstruction("Invalid command"))

def is_identifier_name(name):
    """
    Kiểm tra xem tên biến có hợp lệ hay không.

    Args:
        name (str): Tên biến cần kiểm tra.

    Returns:
        bool: True nếu tên biến hợp lệ, False nếu không.
    """
    return (len(name) > 0 
            and (name[0] >= 'a' and name[0] <= 'z') 
            and not any(not(c.isalpha() or c.isdigit() or c == "_") for c in name[1:]))

def is_valid_type(typ):
    """
    Kiểm tra xem kiểu biến có hợp lệ hay không.

    Args:
        typ (str): Kiểu biến cần kiểm tra.

    Returns:
        bool: True nếu kiểu biến hợp lệ, False nếu không.
    """
    return typ in ["number", "string"]

def extract_vars_clean(sym_table):
    def reducer(acc, tup):
        i, scope = tup                   # i: thứ tự của scope trong reversed(sym_table)
        block_index = len(sym_table) - i - 1  # chuyển về index gốc
        # Với mỗi biến trong scope nếu chưa có thì thêm vào kết quả
        new_entries = [(var, block_index) 
                       for var in scope.keys() if var not in [entry[0] for entry in acc]]
        return new_entries + acc  # thêm entry mới phía trước, đảm bảo inner override outer
    
    return reduce(reducer, enumerate(reversed(sym_table)), [])

def get_type(sym_table, name):
    """
    Trả về kiểu của biến với tên 'name' bằng cách dùng generator expression và next,
    theo phong cách lập trình hàm.

    Args:
        sym_table (list[dict]): Danh sách các scope.
        name (str): Tên của biến cần tra cứu.

    Returns:
        str: Kiểu của biến nếu tìm thấy. Nếu không tìm thấy biến trong bất kỳ scope nào thì trả về None.
    """
    type_found = next((scope[name] for scope in reversed(sym_table) if name in scope), None)
    
    return type_found

def get_block(sym_table, name):
    """
    Trả về thứ tự block của biến với tên 'name'

    Args:
        sym_table (list[dict]): Danh sách các scope.
        name (str): Tên của biến cần tra cứu.

    Returns:
        int: Thứ tự block của biến nếu tìm thấy. Nếu không tìm thấy biến trong bất kỳ scope nào thì trả về None.
    """
    block_found = next((i for i, scope in enumerate(reversed(sym_table)) if name in scope), None)
    if block_found is not None:
        return len(sym_table) - 1 - block_found
    
    return block_found

def is_string(value):
    """
    Kiểm tra xem giá trị đầu vào có phải là chuỗi hay không.

    Args:
        value (str): Giá trị đầu vào.

    Returns:
        bool: True nếu giá trị là chuỗi hợp lệ, False nếu không.
    """
    if (not (len(value) >= 2 and value[0] == "'" and value[-1] == "'")):
        return False
    value_content = value[1:-1]
    return not any(c for c in value_content if not (c.isalpha() or c.isdigit()))

def get_type_of_value(value, sym_table):
    """
    Dự đoán kiểu của giá trị đầu vào.

    Args:
        value (str): Giá trị đầu vào.

    Returns:
        str: Kiểu của giá trị đầu vào.
    """
    if value.isdigit():
        return "number"
    elif is_string(value):
        return "string"
    elif is_identifier_name(value):
        typ = get_type(sym_table, value)
        return typ
    else:
        return "invalid <command>"

def INSERT(cur_sym_table, lst_of_commands, command):
    if len(lst_of_commands) != 3:
        raise StaticError(InvalidInstruction(command))
    if not is_identifier_name(lst_of_commands[1]):
        raise StaticError(InvalidInstruction(command))
    if not is_valid_type(lst_of_commands[2]):
        raise StaticError(InvalidInstruction(command))
    
    var = Symbol(lst_of_commands[1], lst_of_commands[2])

    # Check if the variable already exists in the current symbol table

    if cur_sym_table[-1].get(var.name) is not None:
        raise StaticError(Redeclared(command))
    
    new_sym_table = cur_sym_table.copy()
    new_sym_table[-1][var.name] = var.typ
    return new_sym_table, "success"

def ASSIGN(cur_sym_table, lst_of_commands, command):
    if len(lst_of_commands) != 3:
        raise StaticError(InvalidInstruction(command))
    
    name = lst_of_commands[1]
    if not is_identifier_name(name):
        raise StaticError(InvalidInstruction(command))
    
    value = lst_of_commands[2]
    typ_in_table = get_type(cur_sym_table, name)
    typ = get_type_of_value(value, cur_sym_table)

    if typ == "invalid <command>":
        raise StaticError(InvalidInstruction(command))

    # Check if the variable exists in the current symbol table
    if typ_in_table == None or typ == None:
        raise StaticError(Undeclared(command))

    # Check for type mismatch
    if typ_in_table != typ:
        raise StaticError(TypeMismatch(command))

    return cur_sym_table, "success"

def BLOCK(sym_table, lst_of_commands, command):
    if len(lst_of_commands) != 1:
        raise StaticError(InvalidInstruction(command))
    
    if lst_of_commands[0] == "BEGIN":
        new_sym_table = sym_table.copy()
        return new_sym_table + [{}], None
    else: # lst_of_commands[0] == "END"
        if len(sym_table) == 1:
            # print("sym_table", sym_table)
            raise StaticError(UnknownBlock())
        else:
            return sym_table[:-1], None
        
def LOOKUP(sym_table, lst_of_commands, command):
    if len(lst_of_commands) != 2:
        raise StaticError(InvalidInstruction(command))
    
    if not is_identifier_name(lst_of_commands[1]):
        raise StaticError(InvalidInstruction(command))
    
    name = lst_of_commands[1]
    block = get_block(sym_table, name)
    # print("block", block)
    if block is None:
        raise StaticError(Undeclared(command))
    return sym_table, str(block)

def PRINT(sym_table, lst_of_commands, command):
    if len(lst_of_commands) != 1:
        raise StaticError(InvalidInstruction(command))
    
    lst_of_var = extract_vars_clean(sym_table)

    if lst_of_commands[0] == "PRINT":
        # if len(lst_of_var) == 0:
        #     return sym_table, ""
        # else:
            return sym_table, " ".join([f"{k}//{v}" for k, v in lst_of_var])
        
    else: # lst_of_commands[0] == "RPRINT"
        # if len(lst_of_var) == 0:
        #     return sym_table, ""
        # else:
            return sym_table, " ".join([f"{k}//{v}" for k, v in reversed(lst_of_var)])


    return sym_table, None

def simulate(list_of_commands):
    """
    Executes a list of commands and processes them sequentially.

    Args:
        list_of_commands (list[str]): A list of commands to be executed.

    Returns:
        list[str]: A list of return messages corresponding to each command.
    """

    switch = {
        "INSERT" : INSERT,
        "ASSIGN" : ASSIGN,
        "BEGIN" : BLOCK,
        "END" : BLOCK,
        "LOOKUP" : LOOKUP,
        "PRINT" : PRINT,
        "RPRINT" : PRINT,
    }

    def process_command(state, command):
        # print("command", command)
        sym_table, results = state

        command_parts = command.split(" ")

        new_table, result = switch.get(command_parts[0], invalid_command)(sym_table, command_parts, command)
        # print("new_table", new_table)
        # print("new_table", new_table)
        return new_table, results + [result] if result is not None else results

    sym_table, results = reduce(process_command, list_of_commands, ([{}], []))
    if len(sym_table) > 1:
        raise StaticError(UnclosedBlock(len(sym_table) - 1))
    # print("results", results)
    return results
