import time
from concurrent.futures import ProcessPoolExecutor
from integrate import integrate
import math
import multiprocessing

CPU_NUM = multiprocessing.cpu_count()


def next_range_generator(a, b, per_job):
    intervals = []
    left = a
    while left < b:
        next_cur = left + per_job
        intervals.append([left, min(next_cur, b)])
        left = next_cur
    return intervals


def integration_async(f, a, b, *, n_jobs=1, n_iter=1000, log):
    if log:
        print("\tIntegration interval: [{}, {:.6f}].\t Using {} jobs with {} intervals.".format(a, b, n_jobs, n_iter))
    number_of_values = (b - a) / n_iter
    per_job = (b - a) / n_jobs

    intervals = next_range_generator(a, b, per_job)
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        for j in range(len(intervals)):
            future = executor.submit(integrate, f, number_of_values, intervals[j], False)
        return future.result()


def medium_task():
    print("Comparing time...")
    res = []
    for jobs in range(1, CPU_NUM):
        start_time = time.time()
        integration_async(math.cos, 0, math.pi / 2, n_jobs=jobs, log=True)
        t = time.time() - start_time
        res.append((jobs, t))
    with open("artifacts/medium.txt", "w") as file:
        for i in res:
            file.write("Jobs={}.\t|\tTime={:.6f}\n".format(i[0], i[1]))
    print("------ DONE ------")
