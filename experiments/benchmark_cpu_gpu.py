import tensorflow as tf
import time

# Create random matrices
size = 1000
matrix1 = tf.random.normal((size, size))
matrix2 = tf.random.normal((size, size))

# Run computation on CPU
start_time_cpu = time.time()
result_cpu = tf.matmul(matrix1, matrix2)
end_time_cpu = time.time()
cpu_time = end_time_cpu - start_time_cpu

# Run computation on GPU if available
if tf.config.experimental.list_physical_devices('GPU'):
    start_time_gpu = time.time()
    with tf.device('/GPU:0'):
        result_gpu = tf.matmul(matrix1, matrix2)
    end_time_gpu = time.time()
    gpu_time = end_time_gpu - start_time_gpu
else:
    print("GPU not available")
    gpu_time = None

print("CPU time:", cpu_time)
print("GPU time:", gpu_time)
