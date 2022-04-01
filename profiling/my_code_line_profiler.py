import os
import logging
import time
import numpy as np
import pandas as pd


logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    level=os.getenv("LOG_LEVEL", "INFO")
)
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

@profile
def func1():
    x = np.random.randn(100000)
    y = pd.DataFrame(
        {
            'a': np.random.randn(10000),
            'b': np.random.randn(10000),
            'c': np.random.randn(10000),
        }
    )
    time.sleep(0.5)
    return x


def func2():
    time.sleep(1)

def func3():
    time.sleep(4)


def main():
    for i in range(5):
        logger.info("Start running func 1")
        x = func1()

        logger.info("Start running func 2")
        func2()

    logger.info("Start func 3")
    func3()
    logger.info("Finish")

if __name__ == "__main__":
    main()
