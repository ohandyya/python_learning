# Python Profiling

## Execution time

### Good reading resources

- [Python Timer Functions: Three ways to monitor your code](https://realpython.com/python-timer/)

### How to

- [Time a single function](time_a_single_function.ipynb)

- Use cProfile to find the bottleneck of the code.

  - Package the code in to a single python script
    - Example: [my_code.py](my_code.py)

  - Run cProfile on teh code

    ```bash
    python -m cProfile -o my_code.prof my_code.py 
    ```

  - Launch p[stats module on `my_code.prof` to open an interactive profile statistics browser.

    ```bash
    python -m pstats my_code.prof
    ```

    - Find the functions that uses the most time (including sub-function call)

        ```bash
        my_code.prof% sort cumtime
        my_code.prof% stats 10
        Fri Apr  1 09:49:02 2022    my_code.prof

                87138 function calls (84396 primitive calls) in 9.225 seconds

        Ordered by: cumulative time
        List reduced from 1159 to 10 due to restriction <10>

        ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            453/1    0.002    0.000    9.226    9.226 {built-in method builtins.exec}
                1    0.000    0.000    9.226    9.226 my_code.py:1(<module>)
                1    0.000    0.000    9.032    9.032 my_code.py:26(main)
                6    9.010    1.502    9.010    1.502 {built-in method time.sleep}
                5    0.000    0.000    5.008    1.002 my_code.py:19(func2)
                1    0.000    0.000    4.002    4.002 my_code.py:22(func3)
            163/2    0.001    0.000    0.194    0.097 <frozen importlib._bootstrap>:986(_find_and_load)
            163/2    0.001    0.000    0.194    0.097 <frozen importlib._bootstrap>:956(_find_and_load_unlocked)
            152/2    0.001    0.000    0.193    0.096 <frozen importlib._bootstrap>:650(_load_unlocked)
            119/2    0.000    0.000    0.192    0.096 <frozen importlib._bootstrap_external>:837(exec_module)
        ```

        - We can see that `func2()` was called 5 times. The total time is `5.008` seconds. Each time it takes `1.002` seconds.

    - Find the functions that uses the most time (excluding sub-function call)

        ```bash
        my_code.prof% sort tottime
        my_code.prof% stats 10
        Fri Apr  1 09:49:02 2022    my_code.prof

                87138 function calls (84396 primitive calls) in 9.225 seconds

        Ordered by: internal time
        List reduced from 1159 to 10 due to restriction <10>

        ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            6    9.010    1.502    9.010    1.502 {built-in method time.sleep}
          157    0.029    0.000    0.029    0.000 {built-in method io.open_code}
        30/28    0.024    0.001    0.028    0.001 {built-in method _imp.create_dynamic}
            5    0.019    0.004    0.019    0.004 {method 'randn' of 'numpy.random.mtrand.RandomState' objects}
           57    0.016    0.000    0.016    0.000 {built-in method posix.getcwd}
          316    0.015    0.000    0.015    0.000 {built-in method builtins.compile}
          119    0.013    0.000    0.013    0.000 {built-in method marshal.loads}
          700    0.007    0.000    0.007    0.000 {built-in method posix.stat}
            1    0.004    0.004    0.004    0.004 {method 'read' of '_io.TextIOWrapper' objects}
        261/260    0.004    0.000    0.008    0.000 {built-in method builtins.__build_class__}
        ```

        - When excluding subfunction call, we can see that that the most time consuming function is `time.sleep`, which was called 6 times in total with a total used time = `9.010` seconds.

        - This is especially in identify if there is any build-in function that takes the most execution time. In practice, this ios usually network access or IO access.
    \

    - Find the time of a particular function/class/module

        ```bash
        my_code.prof% stats func1
        Fri Apr  1 09:49:02 2022    my_code.prof

                87138 function calls (84396 primitive calls) in 9.225 seconds

        Ordered by: internal time
        List reduced from 1159 to 1 due to restriction <'func1'>

        ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            5    0.000    0.000    0.019    0.004 my_code.py:14(func1)
        ```

      - We can see that `fun1` was executed 5 times with a total time of `0.019` seconds.

        - When to use this feature:
          - This is most effective if you want to study the execution time of a particular function.

- Use [line_profiler](https://github.com/pyutils/line_profiler) to find the execution time for each line

  - Installation

    ```bash
    pip install line_profiler
    ```

  - Create a python script and decorate the function that you want to profile with `@profile`
    - See [my_code_line_profiler.py](my_code_line_profiler.py) for example.

  - Run line profiler

    ```bash
    kernprof -l my_code_line_profiler.py
    ```

  - See the execution time report

    ```bash
    (p38) atseng@ATLMBP725 profiling % python -m line_profiler my_code_line_profiler.py.lprof

    Timer unit: 1e-06 s

    Total time: 2.55139 s
    File: my_code_line_profiler.py
    Function: func1 at line 15

    Line #      Hits         Time  Per Hit   % Time  Line Contents
    ==============================================================
        15                                           @profile
        16                                           def func1():
        17         5      21767.0   4353.4      0.9      x = np.random.randn(100000)
        18        10       6391.0    639.1      0.3      y = pd.DataFrame(
        19         5          8.0      1.6      0.0          {
        20         5       1822.0    364.4      0.1              'a': np.random.randn(10000),
        21         5       1816.0    363.2      0.1              'b': np.random.randn(10000),
        22         5       1819.0    363.8      0.1              'c': np.random.randn(10000),
        23                                                   }
        24                                               )
        25         5    2517737.0 503547.4     98.7      time.sleep(0.5)
        26         5         35.0      7.0      0.0      return x

    ```

    - From the `Timer unit`, we know that the `Time` unit is `1e-6` seconds.

    - From the `% Time`, we can know which line takes the most of the function execution. In this example, it is clear line 25 (`time.sleep(0.5)`) takes `98.7%` of the total execution time of this function.

    - In practice, it is most effective to optimize the line that takes the most time.


## Memory usage

### How do

- Use [memory-profiler](https://pypi.org/project/memory-profiler/)
  - TBD
