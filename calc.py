import math
import sys

FUNCTIONS = ['log', 'ln', 'sin', 'cos', 'tan',
             'asin', 'acos', 'atan', 'sec', 'csc', 'cot']

COMMANDS = ['settings', 'quit', 'features']

SETTINGS = {'mode': 'norm', 'angles': 'deg'}


def polish_calculator(expression, prev=0, radians=False):
    # We will use a stack to store the intermediate results of the calculation
    stack = []
    expression = expression.lower()
    if expression.split()[0] in COMMANDS:
        match expression.split():
            case ['quit', *_]:
                sys.exit()
            case ['settings', *commands]:
                if commands[0] == 'get':
                    print("Current Settings")
                    print('\n'.join(
                        [f"{key.capitalize()}: {value.capitalize()}" for key, value in SETTINGS.items()]))
                elif commands[0] == 'set':
                    SETTINGS[commands[1].lower()] = commands[2].lower()
            case ['features', *_]:
                print(f"""
Features:
    - Addition, subtraction, division, multiplication, brackets, and exponents (+, -, /, *, ( ), ^)
    - log and ln
    - Trig functions (sin, cos, tan, asin, acos, atan, csc, sec, cot)
    - Constants (pi, e)
    - Previous answer (ans, defaults to 0 at start and if a command was run)
    - Commands (settings set [key] [value], settings get, features, quit)

Issues:
    - Doesn't support power towers (eg e^e^e which will eval as (e^e)^e with my calc instead of e^(e^e) as is done with BEDMAS)
        - Timeline for support: never. I'm lazy
    - sqrt function doesn't exist
        - Timeline for suppport: never, just use ^(1/2)
                """)

        return
    expression = expression.replace(' ', '')

    # We will loop through each character in the expression
    current_token = ''
    p_level = 0
    for char in expression:
        if char not in ['+', '-', '*', '/', '^', '(', ')']:
            current_token += char
        else:
            # If the character is an operator, we will push the current token
            # (which should be a number) onto the stack, and then push the
            # operator onto the stack as well
            if char in ['+', '-', '*', '/', '^']:
                if current_token:
                    if current_token.replace('.', '', 1).isdigit():
                        stack.append(float(current_token))
                    else:
                        stack.append(current_token)
                    current_token = ''
                stack.append(char)

            if char in ['(', ')']:
                if current_token:
                    if current_token.replace('.', '', 1).isdigit():
                        stack.append(float(current_token))
                    else:
                        stack.append(current_token)
                    current_token = ''
                stack.append(char)

    # After we have processed all the characters, we will push the
    # last token (which should be a number) onto the stack
    if current_token:
        if current_token.replace('.', '', 1).isdigit():
            stack.append(float(current_token))
        else:
            stack.append(current_token)

    p_level = 0
    idx = 0
    while True:
        if idx >= len(stack):
            break
        if stack[idx] == '(':
            p_level += 1
            idx += 1
        elif stack[idx] == ')' and p_level > 1:
            p_level -= 1
            idx += 1
        elif stack[idx] == ')' and p_level == 1:
            p_index = stack.index('(')
            stack[p_index] = polish_calculator(
                ''.join([str(item) for item in stack[p_index + 1:idx]]))
            to_del_len = len(stack[p_index + 1:idx + 1])
            del stack[p_index + 1:idx + 1]
            """
            -1 because len is not an index and minus another 1 because we don't 
            want to end up back on the number result which we placed in stack[p_index]
            """
            idx -= to_del_len - 2
            p_level -= 1
        else:
            idx += 1
    for ops in [FUNCTIONS, ["^"], ["*", "/"], ["+", "-"]]:
        idx = 0
        # p_level = 0
        while True:
            if idx >= len(stack):
                break
            if stack[idx] in ops and ops != FUNCTIONS:
                operand1 = stack.pop(idx-1)
                operator = stack.pop(idx-1)
                operand2 = stack.pop(idx-1)
                match operand1:
                    case 'pi':
                        operand1 = math.pi
                    case 'e':
                        operand1 = math.e
                    case 'ans':
                        operand1 = prev
                match operand2:
                    case 'pi':
                        operand2 = math.pi
                    case 'e':
                        operand2 = math.e
                    case 'ans':
                        operand2 = prev
                match operator:
                    case '+':
                        stack.insert(idx-1, operand1 + operand2)
                    case '-':
                        stack.insert(idx-1, operand1 - operand2)
                    case '*':
                        stack.insert(idx-1, operand1 * operand2)
                    case '/':
                        stack.insert(idx-1, operand1 / operand2)
                    case '^':
                        stack.insert(idx-1, operand1 ** operand2)
            elif stack[idx] in ops:
                operator = stack.pop(idx)
                operand1 = stack.pop(idx)
                match operand1:
                    case 'pi':
                        operand1 = math.pi
                    case 'e':
                        operand1 = math.e
                    case 'ans':
                        operand1 = prev
                match operator:
                    case 'ln':
                        stack.insert(idx, math.log(operand1, math.e))
                    case 'log':
                        stack.insert(idx, math.log(operand1, 10))
                    case _:
                        if SETTINGS['angles'] == 'deg':
                            operand1 = math.radians(operand1)
                        match operator:
                            case 'sin':
                                stack.insert(idx, round(
                                    math.sin(operand1), 10))
                            case 'cos':
                                stack.insert(idx, round(
                                    math.cos(operand1), 10))
                            case 'tan':
                                stack.insert(idx, round(
                                    math.tan(operand1), 10))
                            case 'asin':
                                stack.insert(idx, round(
                                    math.asin(operand1), 10))
                            case 'acos':
                                stack.insert(idx, round(
                                    math.acos(operand1), 10))
                            case 'atan':
                                stack.insert(idx, round(
                                    math.atan(operand1), 10))
                            case 'sec':
                                stack.insert(idx, 1/round(
                                    math.cos(operand1), 10))
                            case 'csc':
                                stack.insert(idx, 1/round(
                                    math.sin(operand1), 10))
                            case 'cot':
                                stack.insert(idx, 1/round(
                                    math.tan(operand1), 10))
            else:
                idx += 1

    # After we have processed all the tokens, the result will be the
    # only value remaining on the stack
    match stack[0]:
        case 'pi':
            stack[0] = math.pi
        case 'e':
            stack[0] = math.e
        case 'ans':
            stack[0] = prev
        case _:
            if isinstance(stack[0], str):
                raise TypeError()
    return stack[0]


# We can now use the input() function to allow the user to enter
# a Polish notation expression and pass it to our calculator function

result = 0.0
while True:
    expression = input('Enter a Polish notation expression: ')
    try:
        result = polish_calculator(expression, prev=result)
        if result is not None:
            print(result)
        else:
            result = 0.0
    except ZeroDivisionError:
        print("Undefined (DIV/0)")
    except TypeError:
        print("Invalid equation. Run the command 'features' to get a list of all supported features.")
    except OverflowError:
        print("Answer too large")
