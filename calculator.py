
class Calculator:
    def __init__(self) -> None:
        pass

    def summation(self, numbers: [int]) -> int:
        # Calculate the sum of all numbers
        return sum(numbers)

    def product(self, numbers: [int]) -> int:
        # Calculate the product of all numbers
        product = 1
        for number in numbers:
            product *= number
        return product

    def minimum(self, numbers: [int]) -> int:
        # Find the minimum number
        return min(numbers)

    def maximum(self, numbers: [int]) -> int:
        # Find the maximum number
        return max(numbers)