import os
from unittest.mock import MagicMock, patch

from huggingface_hub.utils import filter_repo_objects

import ovos_stt_plugin_sherpa_onnx as plugin
from ovos_stt_plugin_sherpa_onnx import SherpaOnnxSTT

FOURIER_REVISION = "3fda023e157ce7986f137f76fcf326ed6e08fa73"

ONNX_PACK_FILES = [
    "onnx/sherpa-int8/README.md",
    "onnx/sherpa-int8/SHA256SUMS",
    "onnx/sherpa-int8/conv_frontend.onnx",
    "onnx/sherpa-int8/decoder.int8.onnx",
    "onnx/sherpa-int8/decoder.int8.onnx.data",
    "onnx/sherpa-int8/encoder.int8.onnx",
    "onnx/sherpa-int8/encoder.int8.onnx.data",
    "onnx/sherpa-int8/tokenizer/config.json",
    "onnx/sherpa-int8/tokenizer/merges.txt",
    "onnx/sherpa-int8/tokenizer/tokenizer.json",
    "onnx/sherpa-int8/tokenizer/tokenizer_config.json",
    "onnx/sherpa-int8/tokenizer/vocab.json",
]

NON_ONNX_REPO_FILES = [
    ".gitattributes",
    "Fourier-2B-Q8_0.gguf",
    "README.md",
    "generation_config.json",
    "model.safetensors",
    "processor_config.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "examples/sherpa-onnx/README.md",
    "mlx/8bit/config.json",
]


def test_fourier_snapshot_download_includes_root_config_and_loads_onnx_pack(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(plugin, "XDG_CACHE_HOME", str(tmp_path))

    captured = {}

    def fake_snapshot_download(**kwargs):
        captured.update(kwargs)
        local_dir = kwargs["local_dir"]
        os.makedirs(os.path.join(local_dir, "onnx", "sherpa-int8", "tokenizer"), exist_ok=True)
        with open(os.path.join(local_dir, "config.json"), "w", encoding="utf-8") as handle:
            handle.write("{}\n")
        return local_dir

    fake_recognizer = MagicMock(name="OfflineRecognizer")
    with (
        patch("huggingface_hub.snapshot_download", side_effect=fake_snapshot_download),
        patch.object(
            plugin.so.OfflineRecognizer,
            "from_qwen3_asr",
            return_value=fake_recognizer,
        ) as mock_from_qwen3,
    ):
        stt = SherpaOnnxSTT(
            config={
                "model_type": "qwen3-asr",
                "model": "oruk/oruk-fourier-2b",
                "num_threads": 4,
            }
        )

    expected_local_dir = os.path.join(
        str(tmp_path), "sherpa-onnx", "oruk-fourier-2b", FOURIER_REVISION
    )
    assert captured["repo_id"] == "oruk/oruk-fourier-2b"
    assert captured["revision"] == FOURIER_REVISION
    assert captured["local_dir"] == expected_local_dir
    assert captured["allow_patterns"] == ["config.json", "onnx/sherpa-int8/*"]

    repo_files = ["config.json", *ONNX_PACK_FILES, *NON_ONNX_REPO_FILES]
    matched = list(
        filter_repo_objects(repo_files, allow_patterns=captured["allow_patterns"])
    )
    assert set(matched) == {"config.json", *ONNX_PACK_FILES}

    expected_model_dir = os.path.join(expected_local_dir, "onnx", "sherpa-int8")
    assert os.path.isfile(os.path.join(expected_local_dir, "config.json"))
    assert not os.path.exists(os.path.join(expected_model_dir, "config.json"))
    mock_from_qwen3.assert_called_once_with(
        conv_frontend=os.path.join(expected_model_dir, "conv_frontend.onnx"),
        encoder=os.path.join(expected_model_dir, "encoder.int8.onnx"),
        decoder=os.path.join(expected_model_dir, "decoder.int8.onnx"),
        tokenizer=os.path.join(expected_model_dir, "tokenizer"),
        provider="cpu",
        num_threads=4,
    )
    assert stt.recognizer is fake_recognizer


def test_qwen3_asr_local_model_dir_skips_hub_download(tmp_path):
    local_pack = tmp_path / "custom-qwen3-asr"
    local_pack.mkdir()
    fake_recognizer = MagicMock(name="OfflineRecognizer")

    with (
        patch("huggingface_hub.snapshot_download") as mock_snapshot,
        patch.object(
            plugin.so.OfflineRecognizer,
            "from_qwen3_asr",
            return_value=fake_recognizer,
        ) as mock_from_qwen3,
    ):
        stt = SherpaOnnxSTT(
            config={
                "model_type": "qwen3-asr",
                "model_dir": str(local_pack),
                "num_threads": 2,
            }
        )

    mock_snapshot.assert_not_called()
    mock_from_qwen3.assert_called_once_with(
        conv_frontend=os.path.join(str(local_pack), "conv_frontend.onnx"),
        encoder=os.path.join(str(local_pack), "encoder.int8.onnx"),
        decoder=os.path.join(str(local_pack), "decoder.int8.onnx"),
        tokenizer=os.path.join(str(local_pack), "tokenizer"),
        provider="cpu",
        num_threads=2,
    )
    assert stt.recognizer is fake_recognizer
