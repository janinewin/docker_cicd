import functools

__all__ = [
    "Fibonacci",
]


class Fibonacci:
    def compute(self, n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return Fibonacci(n - 1) + Fibonacci(n - 2)

    @functools.lru_cache(None)
    def compute_fast(self, n):
        if n < 2:
            return n
        return self.astFib(n - 1) + self.fastFib(n - 2)


if __name__ == "__main__":
    fib = Fibonacci()
