#!/usr/bin/env bash

model_url="https://coqui.gateway.scarf.sh/english/coqui/v1.0.0-huge-vocab/model.tflite"
scorer_url="https://coqui.gateway.scarf.sh/english/coqui/v1.0.0-huge-vocab/huge-vocabulary.scorer"

# https://stackoverflow.com/a/48972723
# Verify SHA256 checksums
sha256sum --status -c SHA256SUM
if [ $? -ne 0 ]; then
    echo "Checksums do not match. Downloading model and scorer."
    wget -O model.tflite $model_url
    wget -O huge-vocabulary.scorer $scorer_url
    sha256sum --status -c SHA256SUM
    if [ $? -ne 0 ]; then
        echo "Checksums still do not match. Exiting."
        exit 1
    fi
else
    echo "Checksums match. We good. 🚀"
fi
