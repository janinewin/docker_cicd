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
            return self.compute(n - 1) + self.compute(n - 2)

    @functools.lru_cache(None)
    def compute_fast(self, n):
        if n < 2:
            return n
        return self.compute_fast(n - 1) + self.compute_fast(n - 2)


if __name__ == "__main__":
    fib = Fibonacci()
