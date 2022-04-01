# Asynchronous HTTP Requests

## Useful information

- [aiohttp](https://docs.aiohttp.org/en/latest/client_quickstart.html)

- [Asynchronous HTTP Requests in Python with aiohttp and asyncio](https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp)


### How to do X?

- Measure the client response time

  - Do it "synchronously" (see [exp3.py](exp3.py))

- Send high requests-per-seconds

  - Use `aiohttp` + `asyncio` (see [exp4.py](exp4.py))

  - However, in this case, we will not be able to measure the response time reliably. This is because by using async, it messed up with the time measurement. And unfortunately, `aiohttp` does not have a built-in time measurement.

  - So in this case, we will have to measure the performance metric on the server side and not on the client side. For example, most server has performance monitor (e.g., datadog) in place. We can use [exp4.py](exp4.py) to generate a very high RPS and see how does the server react.

  - When using [exp4.py](exp4.py), we need to be careful as the server side `may` implement some rate limiting. So if we send too high RPS, it may trigger the rate limiting.

  - [exp2.py](exp2.py) is a slower version of using aiohttp. While it is slower than [exp4.py](exp4.py), it is more flexible (in some situations). But we want to send very high RPS, then [exp4.py](exp4.py) is a better approach.
