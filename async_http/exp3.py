"""Make 150 requests using requests"""

import requests
import time
import numpy as np

start_time = time.perf_counter()

result = []
time_used = []
for number in range(1, 151):
    url = f'https://pokeapi.co/api/v2/pokemon/{number}'
    # url = "https://google.com"
    tstart = time.perf_counter()
    resp = requests.get(url)
    # pokemon = resp.json()
    _ = resp.text
    tused = time.perf_counter() - tstart
    result.append("haha")
    time_used.append(tused)


tused = time.perf_counter() - start_time
print(f"--- {tused} seconds ---")

print(f"RPS = {len(result) / tused:.3f}")


total_times = np.array(time_used)
quantiles = [0, 0.1, 0.5, 0.95, 0.99, 1]
quantiles_times = np.quantile(total_times, quantiles)
for quant, val in zip(quantiles, quantiles_times):
    print(f"{quant*100:.0f} quantile: {val*1000 :.2f} milliseconds")
