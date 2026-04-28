---
title: "Tensorflow - Suppressing FutureWarning numpy messages in Jupyter Notebooks"
date: 2019-08-12T11:55:41+0000
lastmod: 2019-08-12T11:55:41+0000
slug: "tensorflow-suppressing-futurewarning-numpy-messages-in-jupyter-notebooks"
feature_image: "https://www.cicoria.com/content/images/2019/08/jupyter-squashed.jpg"
aliases:
  - /tensorflow-suppressing-futurewarning-numpy-messages-in-jupyter-notebooks/
---

You get these annoying errors first on a cold kernel in Jupyter notebooks when using Tensorflow and their Keras abstraction.

```python
/Users/cicorias/.pyenv/versions/3.7.3/envs/tf-nb-373/lib/python3.7/site-packages/tensorflow/python/framework/dtypes.py:516: FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
  _np_qint8 = np.dtype([("qint8", np.int8, 1)])
/Users/cicorias/.pyenv/versions/3.7.3/envs/tf-nb-373/lib/python3.7/site-packages/tensorflow/python/framework/dtypes.py:517: FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
  _np_quint8 = np.dtype([("quint8", np.uint8, 1)])

```

To suppress these the following snippet works well.

```python
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.preprocessing.text import Tokenizer

print('ready')

```

of course you won't see any [FutureWarning](https://docs.python.org/3/library/exceptions.html#FutureWarning) - but this is Notebooks and if this is production, well, that's a different issue.
