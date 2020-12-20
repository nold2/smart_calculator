# Smart Calculator

[![Demo](https://imgur.com/vcqqLCu)]

A basic python REPL application to calculate simple mathematical equation 

### Architecture

The App is divided into:
1. The `main` interface
2. The `Validator`, to validate the inputs
3. The `Tokenizer`, to transform validated inputs into list of tokens
4. The `Calculator`, to calculate list of tokens
5. The `Command`, to call the built in commands from inputs
6. The `Exception`, to represent custom errors
7. The `Variable` to represent a variable
8. The `Digit` to represent the numeric operands
9. The `Operator` to represent the Operator
10. The `Memory` to represent as a store for numeric value of `Variable`