# OpenVoiceOS STT Plugin - Sherpa ONNX

An OpenVoiceOS Speech-to-Text plugin that uses [Sherpa-ONNX](https://github.com/k2-fsa/sherpa-onnx), the Kaldi-based speech recognition toolkit from k2-fsa. The plugin runs fully offline and supports Transducer, Whisper, Moonshine, Paraformer, and several CTC model architectures.

## Description

This plugin lets OpenVoiceOS run offline speech recognition with models compatible with the ONNX runtime. If you give it a model ID, it downloads the model from the `k2-fsa` repository. If you give it local file paths, it uses those instead.

## Install

```bash
pip install ovos-stt-plugin-sherpa-onnx
```

## Models

Find available models on the [sherpa-onnx releases page](https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models).

The `model` key usually matches the name of the release archive, for example `sherpa-onnx-nemo-fast-conformer-transducer-en-de-es-fr-14288`.

## Configuration

Add the following to your `mycroft.conf`. The configuration keys depend on the `model_type` you choose.

### Basic usage (Transducer)

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

### Supported model types and examples

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

## Advanced: using local models

If you do not set the `model` key, the plugin does not download anything. Instead, give it absolute paths to the model files in the specific keys, such as `encoder`, `decoder`, or `model_file`.

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

## Related projects

- [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx): the speech recognition toolkit this plugin wraps.
- [TigreGotico/ovos-stt-plugin-onnx-asr](https://github.com/TigreGotico/ovos-stt-plugin-onnx-asr): a sibling offline OVOS STT plugin built on the `onnx-asr` runtime.
- [TigreGotico/ovos-stt-plugin-fasterwhisper](https://github.com/TigreGotico/ovos-stt-plugin-fasterwhisper): a sibling offline OVOS STT plugin for Whisper models.
- [OpenVoiceOS/ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager): discovers and loads this plugin through the `opm.stt` entry point.

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for the full text.
