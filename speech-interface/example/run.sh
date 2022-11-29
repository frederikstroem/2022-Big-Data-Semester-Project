#!/usr/bin/env bash

python mic_vad_streaming.py \
    -m ../model.tflite \
    -s ../huge-vocabulary.scorer
