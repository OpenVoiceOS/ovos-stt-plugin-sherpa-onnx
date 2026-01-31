# OpenVoiceOS STT Plugin - Sherpa ONNX

An OpenVoiceOS Speech-to-Text plugin that uses [Sherpa-ONNX](https://github.com/k2-fsa/sherpa-onnx), the next-generation Kaldi-based speech recognition toolkit. This plugin runs completely offline and supports a wide variety of state-of-the-art architectures including Transducer, Whisper, Moonshine, Paraformer, and various CTC models.

## Description

This plugin allows OpenVoiceOS to perform offline speech recognition using models compatible with the ONNX runtime. It automatically handles downloading models from the `k2-fsa` repository if a model ID is provided, or uses local files if preferred.

## Install

```bash
pip install ovos-stt-plugin-sherpa-onnx
```

## Models

You can find available models in the [sherpa-onnx releases page](https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models).

When configuring the plugin, the `model` key typically corresponds to the name of the release archive (e.g., `sherpa-onnx-nemo-fast-conformer-transducer-en-de-es-fr-14288`).

## Configuration

Add the following to your `mycroft.conf`. The configuration keys change depending on the `model_type` you select.

### Basic Usage (Transducer)

This is the standard configuration for Zipformer and Conformer transducer models.

```json
{
  "stt": {
    "module": "ovos-stt-plugin-sherpa-onnx",
    "ovos-stt-plugin-sherpa-onnx": {
      "model": "sherpa-onnx-zipformer-en-libriheavy-20230830-large-punct-case",
      "model_type": "transducer",
      "encoder": "encoder-epoch-16-avg-2.int8.onnx",
      "decoder": "decoder-epoch-16-avg-2.int8.onnx",
      "joiner": "joiner-epoch-16-avg-2.int8.onnx",
      "tokens": "tokens.txt"
    }
  }
}

```

### Supported Model Types & Examples

The plugin supports many architectures. Below are configuration examples for the most common ones.

#### Whisper

```json
{
  "model": "sherpa-onnx-whisper-turbo",
  "model_type": "whisper",
  "encoder": "turbo-encoder.int8.onnx",
  "decoder": "turbo-decoder.int8.onnx",
  "tokens": "turbo-tokens.txt"
}

```

#### Moonshine

```json
{
  "model": "sherpa-onnx-moonshine-base-en-int8",
  "model_type": "moonshine",
  "encoder": "encode.int8.onnx",
  "uncached_decoder": "uncached_decode.int8.onnx",
  "cached_decoder": "cached_decode.int8.onnx",
  "preprocessor": "preprocess.onnx",
  "tokens": "tokens.txt"
}

```

#### Paraformer

```json
{
  "model": "sherpa-onnx-paraformer-en-2024-03-09",
  "model_type": "paraformer",
  "model_file": "model.int8.onnx",
  "tokens": "tokens.txt"
}

```

#### Generic CTC (Zipformer, NeMo, WeNet, TeleSpeech, etc.)

For `model_type` values like `zipformer-ctc`, `nemo-ctc`, `wenet-ctc`, `telespeech-ctc`, `tdnn-ctc`:

```json
{
  "model": "sherpa-onnx-zipformer-ctc-en-2023-10-02",
  "model_type": "zipformer-ctc",
  "model_file": "model.int8.onnx",
  "tokens": "tokens.txt"
}

```

#### Sense Voice

```json
{
  "model": "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09",
  "model_type": "sense-voice",
  "model_file": "model.int8.onnx",
  "tokens": "tokens.txt"
}

```

#### FireRed ASR

```json
{
  "model": "sherpa-onnx-fire-red-asr-large-zh_en-2025-02-16",
  "model_type": "fire-red-asr",
  "encoder": "encoder.int8.onnx",
  "decoder": "decoder.int8.onnx",
  "tokens": "tokens.txt"
}

```

#### FunASR Nano

```json
{
  "model": "sherpa-onnx-funasr-nano-int8-2025-12-30",
  "model_type": "funasr-nano",
  "llm": "llm.int8.onnx",
  "embedding": "embedding.int8.onnx",
  "encoder_adaptor": "encoder_adaptor.int8.onnx",
  "tokenizer": "Qwen3-0.6B"
}

```

## Advanced: Using Local Models

If you do not provide the `model` key (which triggers the download), you can provide absolute paths to the files on your system directly in the specific keys (e.g., `encoder`, `decoder`, `model_file`).

```json
{
  "stt": {
    "module": "ovos-stt-plugin-sherpa-onnx",
    "ovos-stt-plugin-sherpa-onnx": {
      "model_type": "transducer",
      "encoder": "/path/to/encoder.onnx",
      "decoder": "/path/to/decoder.onnx",
      "joiner": "/path/to/joiner.onnx",
      "tokens": "/path/to/tokens.txt"
    }
  }
}

```