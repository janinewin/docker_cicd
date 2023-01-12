import functools

__all__ = [
    "Fibonacci",
]


class Fibonacci:
    async def compute(self, n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return await self.compute(n - 1) + await self.compute(n - 2)

    # Add a `compute_fast` method to improve the performance of this computation
    


if __name__ == "__main__":
    fib = Fibonacci()
