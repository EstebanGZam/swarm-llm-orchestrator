#!/bin/sh
# Ollama server used for the V4.0 experiment (port 11435, next to a default server on 11434).
# Every model must run 100% on the GPU with num_ctx = 8192 on a 4 GB card: flash attention and an
# 8-bit KV cache make llama3.2:3b fit (it ran only 90% on GPU without them). One model is loaded and
# one request is served at a time, so no two models compete for the GPU.
export OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11435}"
export OLLAMA_MODELS="${OLLAMA_MODELS:-/usr/share/ollama/.ollama/models}"   # default model store of a Linux install
export OLLAMA_FLASH_ATTENTION=1
export OLLAMA_KV_CACHE_TYPE=q8_0
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_KEEP_ALIVE=60m
exec ollama serve
