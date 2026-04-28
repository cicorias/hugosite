---
title: "Keras Tensor flow CUBLAS_STATUS_NOT_INITIALIZED"
date: 2018-12-13T22:10:59+0000
lastmod: 2018-12-13T22:10:59+0000
slug: "keras-tensor-flow-cublas_status_not_initialized"
feature_image: "https://www.cicoria.com/content/images/2018/12/image-4.png"
aliases:
  - /keras-tensor-flow-cublas_status_not_initialized/
---

I have an older Razer Blade with a 970 NVidia 0 so, not much memory relative to the 10x series.

Was seeing the error in the logs

```
totalMemory: 6.00GiB freeMemory: 5.02GiB
2018-12-13 21:56:56.358056: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1511] Adding visible gpu devices: 0
2018-12-13 21:56:59.233889: I tensorflow/core/common_runtime/gpu/gpu_device.cc:982] Device interconnect StreamExecutor with strength 1 edge matrix:
2018-12-13 21:56:59.265182: I tensorflow/core/common_runtime/gpu/gpu_device.cc:988]      0
2018-12-13 21:56:59.285922: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1001] 0:   N
2018-12-13 21:56:59.306705: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 4780 MB memory) -> physical GPU (device: 0, name: GeForce GTX 970M, pci bus id: 0000:01:00.0, compute capability: 5.2)
2018-12-13 21:57:02.270346: E tensorflow/stream_executor/cuda/cuda_blas.cc:464] failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED
2018-12-13 21:57:02.309705: E tensorflow/stream_executor/cuda/cuda_blas.cc:464] failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED
2018-12-13 21:57:02.341990: E tensorflow/stream_executor/cuda/cuda_blas.cc:464] failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED
2018-12-13 21:57:02.383201: E tensorflow/stream_executor/cuda/cuda_blas.cc:464] failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED
2018-12-13 21:57:02.412766: E tensorflow/stream_executor/cuda/cuda_blas.cc:464] failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED
2018-12-13 21:57:02.443575: E tensorflow/stream_executor/cuda/cuda_blas.cc:464] failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED
2018-12-13 21:57:02.473450: E tensorflow/stream_executor/cuda/cuda_blas.cc:464] failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED
2018-12-13 21:57:02.502777: E tensorflow/stream_executor/cuda/cuda_blas.cc:464] failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED
2018-12-13 21:57:02.545734: E tensorflow/stream_executor/cuda/cuda_blas.cc:464] failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED
2018-12-13 21:57:02.575651: W tensorflow/stream_executor/stream.cc:2127] attempting to perform BLAS operation using StreamExecutor without BLAS support

```

What it took was a simple insertion of lower level TensorFlow configuration like the following:

Just before you build or load your model:

```python
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
config.log_device_placement = True  # to log device placement (on which device the operation ran)
                                    # (nothing gets printed in Jupyter, only if you run it standalone)
sess = tf.Session(config=config)
set_session(sess)  # set this TensorFlow session as the default session for Keras

```
