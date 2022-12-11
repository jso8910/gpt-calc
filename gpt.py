def polish_calculator(expression):
  # We will use a stack to store the intermediate results of the calculation
  stack = []

  # We will loop through each character in the expression
  current_token = ''
  for char in expression:
    # If the character is a digit, we will add it to the current token
    if char.isdigit():
      current_token += char
    else:
      # If the character is an operator, we will push the current token
      # (which should be a number) onto the stack, and then push the
      # operator onto the stack as well
      if char in ['+', '-', '*', '/']:
        stack.append(int(current_token))
        stack.append(char)
        current_token = ''

  # After we have processed all the characters, we will push the
  # last token (which should be a number) onto the stack
  stack.append(int(current_token))

  # We will now loop through the stack and evaluate the Polish
  # notation expression
  while len(stack) > 1:
    # We will pop the last two values from the stack, perform the
    # operation, and push the result back onto the stack
    operand1 = stack.pop()
    operator = stack.pop()
    operand2 = stack.pop()

    if operator == '+':
      result = operand1 + operand2
    elif operator == '-':
      result = operand1 - operand2
    elif operator == '*':
      result = operand1 * operand2
    elif operator == '/':
      result = operand1 / operand2
    stack.append(result)

  # After we have processed all the tokens, the result will be the
  # only value remaining on the stack
  return stack[0]

# We can now use the input() function to allow the user to enter
# a Polish notation expression and pass it to our calculator function
expression = input('Enter a Polish notation expression: ')
result = polish_calculator(expression)
print('Result:', result)