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
    # $DELETE_BEGIN
    @functools.lru_cache(None)
    def compute_fast(self, n):
        if n < 2:
            return n
        return self.compute_fast(n - 1) + self.compute_fast(n - 2)
    #DELETE_END


if __name__ == "__main__":
    fib = Fibonacci()
