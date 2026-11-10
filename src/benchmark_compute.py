"""
Hardware Acceleration Benchmark: CPU vs GPU Matrix Computation
==============================================================
Developed at Central Research & Training Laboratory (CRTEL), NCSM
Author: Arafat Ali Mondal

Description:
    Benchmarks matrix operations on CPU vs GPU to evaluate edge hardware
    throughput for real-time computer vision inference.
"""

import time
import numpy as np


def benchmark_numpy_cpu(size: int = 1500, iterations: int = 5) -> float:
    """
    Measures CPU execution time using NumPy optimized BLAS.
    """
    times = []
    for _ in range(iterations):
        a = np.random.randn(size, size).astype(np.float32)
        b = np.random.randn(size, size).astype(np.float32)
        start = time.perf_counter()
        _ = np.dot(a, b)
        times.append(time.perf_counter() - start)
    return float(np.mean(times))


def benchmark_gpu_tensorflow(size: int = 1500) -> None:
    """
    Attempts GPU computation if TensorFlow is installed and GPU is available.
    """
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        if not gpus:
            print("[INFO] No dedicated TensorFlow GPU detected. Running on CPU.")
            return

        with tf.device('/GPU:0'):
            a = tf.random.normal((size, size))
            b = tf.random.normal((size, size))
            start = time.perf_counter()
            _ = tf.matmul(a, b)
            gpu_time = time.perf_counter() - start
            print(f"[BENCHMARK] TensorFlow GPU Time: {gpu_time * 1000:.2f} ms")
    except ImportError:
        print("[INFO] TensorFlow not installed. Skipping GPU matrix benchmark.")


def main() -> None:
    size = 1500
    print(f"=== CRTEL Lab Compute Benchmark (Matrix Size: {size}x{size}) ===")
    cpu_ms = benchmark_numpy_cpu(size=size) * 1000.0
    print(f"[BENCHMARK] CPU (NumPy/BLAS) Average Latency: {cpu_ms:.2f} ms")
    benchmark_gpu_tensorflow(size=size)


if __name__ == "__main__":
    main()
