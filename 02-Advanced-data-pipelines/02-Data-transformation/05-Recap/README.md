# Recap - Serverless execution modes

In this recap, we'll take a serverless framework, like Google Cloud Run, and tweak the settings depending on our use cases.

We'll vary:

- Latency requirements (from < 1s to < 50ms)
  - Solution: Have at least one instance running to mitigate cold starts
- Large number of users (from 10 per minute to 10k per minute)
  - Solution: concurrency per instance, total number of instances
- Processing power required (from 20MB of RAM and 1vCPU to 2GB of RAM per call)
  - Solution: play with instance size and concurrency

And for some we'll write small Python apps to illustrate it.
