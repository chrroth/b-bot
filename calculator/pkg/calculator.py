# calculator/pkg/calculator.py

import sys
from collections import deque

class Calculator:
    def __init__(self):
        self.operators = {
            "+": (2, lambda a, b: a + b), # Lower precedence for addition
            "-": (2, lambda a, b: a - b), # Lower precedence for subtraction
            "*": (3, lambda a, b: a * b), # Higher precedence for multiplication
            "/": (3, lambda a, b: a / b), # Higher precedence for division
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)
    
    def _evaluate_infix(self, tokens):
        values = deque()
        ops = deque()

        def apply_op():
            op = ops.pop()
            right = values.pop()
            left = values.pop()
            values.append(self.operators[op][1](left, right))

        for token in tokens:
            if token in self.operators:
                while (
                    ops
                    and ops[-1] in self.operators
                    and self.operators[ops[-1]][0] >= self.operators[token][0]
                ):
                    apply_op()
                ops.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")
                
        while ops:
            apply_op()

        if len(values) != 1:
            raise ValueError("invalid expression")
        
        return values[0]
