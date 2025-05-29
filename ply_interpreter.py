import ply.lex as lex
import ply.yacc as yacc

# Reserved keywords
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'def': 'DEF',
    'print': 'PRINT'
}

# Tokens
tokens = (
    'IDENTIFIER', 'NUMBER', 'EQUALS', 'COLON', 'LPAREN', 'RPAREN',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'COMMA', 'STRING', 'EQ'
) + tuple(reserved.values())

# Regular expressions for simple tokens
t_EQ = r'=='
t_EQUALS = r'='
t_COLON = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_COMMA = r','

def t_STRING(t):
    r'"([^\\"]|\\.)*"'
    t.value = t.value[1:-1]  # Strip quotes
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Symbol and function tables
symbol_table = {}
function_table = {}

# Precedence
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'EQ'),
)

# Grammar rules
def p_program(p):
    'program : statement_list'
    for stmt in p[1]:
        if stmt is not None:
            execute(stmt)

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_statement(p):
    '''statement : assignment
                 | conditional
                 | while_loop
                 | function_def
                 | print_statement
                 | expression'''
    p[0] = p[1]

def p_assignment(p):
    'assignment : IDENTIFIER EQUALS expression'
    p[0] = ('assign', p[1], p[3])

def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN'
    p[0] = ('print', p[3])

def p_conditional(p):
    '''conditional : IF LPAREN expression RPAREN COLON statement
                   | IF LPAREN expression RPAREN COLON statement ELSE COLON statement'''
    if len(p) == 7:
        p[0] = ('if', p[3], p[6], None)
    else:
        p[0] = ('if-else', p[3], p[6], p[9])

def p_while_loop(p):
    'while_loop : WHILE LPAREN expression RPAREN COLON statement'
    p[0] = ('while', p[3], p[6])

def p_function_def(p):
    '''function_def : DEF IDENTIFIER LPAREN param_list RPAREN COLON statement
                    | DEF IDENTIFIER LPAREN RPAREN COLON statement'''
    params = p[4] if len(p) == 8 else []
    body = p[7] if len(p) == 8 else p[6]
    p[0] = ('function', p[2], params, body)

def p_param_list(p):
    '''param_list : IDENTIFIER
                  | param_list COMMA IDENTIFIER'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_expression(p):
    '''expression : comparison_expr
                  | arithmetic_expr
                  | STRING
                  | function_call'''
    p[0] = p[1]

def p_comparison_expr(p):
    'comparison_expr : arithmetic_expr EQ arithmetic_expr'
    p[0] = ('eq', p[1], p[3])

def p_function_call(p):
    '''function_call : IDENTIFIER LPAREN argument_list RPAREN
                     | IDENTIFIER LPAREN RPAREN'''
    args = p[3] if len(p) == 5 else []
    p[0] = ('call', p[1], args)

def p_argument_list(p):
    '''argument_list : expression
                     | argument_list COMMA expression'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_arithmetic_expr(p):
    '''arithmetic_expr : term
                       | arithmetic_expr PLUS term
                       | arithmetic_expr MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])

def p_factor(p):
    '''factor : NUMBER
              | IDENTIFIER
              | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = ('var', p[1]) if isinstance(p[1], str) else p[1]
    else:
        p[0] = p[2]  # parenthesized expression

def p_error(p):
    print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOF")

parser = yacc.yacc()

# --- Execution Engine ---

def execute(node):
    if node is None:
        return
    
    if isinstance(node, tuple) and len(node) > 0:
        if node[0] == 'assign':
            var, val_expr = node[1], node[2]
            symbol_table[var] = evaluate(val_expr)
        elif node[0] == 'print':
            print(evaluate(node[1]))
        elif node[0] == 'if':
            cond, then_stmt = node[1], node[2]
            if evaluate(cond):
                execute(then_stmt)
        elif node[0] == 'if-else':
            cond, then_stmt, else_stmt = node[1], node[2], node[3]
            if evaluate(cond):
                execute(then_stmt)
            else:
                execute(else_stmt)
        elif node[0] == 'while':
            cond, body = node[1], node[2]
            while evaluate(cond):
                execute(body)
        elif node[0] == 'function':
            name, params, body = node[1], node[2], node[3]
            function_table[name] = (params, body)
        elif node[0] == 'call':
            name, args = node[1], node[2]
            if name not in function_table:
                print(f"Undefined function: {name}")
                return
            params, body = function_table[name]
            if len(args) != len(params):
                print("Argument count mismatch")
                return
            saved = symbol_table.copy()
            for param, arg in zip(params, args):
                symbol_table[param] = evaluate(arg)
            execute(body)
            symbol_table.clear()
            symbol_table.update(saved)

def evaluate(expr):
    if isinstance(expr, int) or isinstance(expr, str):
        return expr
    elif isinstance(expr, tuple) and len(expr) > 0:
        if expr[0] == 'var':
            name = expr[1]
            return symbol_table.get(name, 0)
        elif expr[0] == 'binop':
            op, left, right = expr[1], expr[2], expr[3]
            l, r = evaluate(left), evaluate(right)
            if op == '+':
                return l + r
            elif op == '-':
                return l - r
            elif op == '*':
                return l * r
            elif op == '/':
                if r == 0:
                    print("Error: Division by zero")
                    return 0
                return l / r
        elif expr[0] == 'eq':
            left, right = expr[1], expr[2]
            return evaluate(left) == evaluate(right)
        elif expr[0] == 'call':
            name, args = expr[1], expr[2]
            execute(('call', name, args))
            return None  # No return handling
    return expr

# --- Interactive Loop ---

print("Enter code (type 'exit' to stop):")
while True:
    try:
        user_input = input(">>> ")
        if user_input.lower() == 'exit':
            break
        parser.parse(user_input)
    except Exception as e:
        print(f"Error: {e}")
