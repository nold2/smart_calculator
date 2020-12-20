# Smart Calculator

![Demo](https://i.imgur.com/vcqqLCu.gif)

A basic python REPL application to calculate simple mathematical equation 

### Architecture

The App is divided into:
1. The `main` interface
2. The `Validator`, to validate the inputs
3. The `Tokenizer`, to transform validated inputs into list of tokens
4. The `Calculator`, to calculate tokenize equation into digit
5. The `Command`, to call the built in commands from inputs
6. The `Exception`, to represent custom errors
7. The `Variable` to represent a variable
8. The `Digit` to represent the numeric operands
9. The `Operator` to represent the Operator
10. The `Memory` to represent as a store for numeric value of `Variable`


### Feature 
1. Store and use variables in your equation!
2. Parenthesis, Multiplication, Division, Exponentiation, Addition, Subtraction and Assignment!
3. Stuck? use help! (/help)

### How it works
```bash
python calculator/calculator.py
```
```bash
> 8 * 3 + 12 * (4 - 2)
48
> 2 - 2 + 3
3
> 4 * (2 + 3
Invalid expression
> -10
-10
> a=4
> b=5
> c=6
> a*2+b*3+c*(2+3)
53
> 1 +++ 2 * 3 -- 4
11
> 3 *** 5
Invalid expression
> 4+3)
Invalid expression
> /command
Unknown command
> /exit
Bye!
```

### Requirements

Tested to work and run properly on python 3.8.5
