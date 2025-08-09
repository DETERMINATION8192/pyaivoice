# pyaivoice

<p align="right"><a href="./README.md">日本語</a></p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple library to control A.I.VOICE Talk Editor from Python.

## Requirements

- Windows OS
- Python 3.10+
- A.I.VOICE Talk Editor (v1.3.0 or later)

## Installation

```sh
pip install git+https://github.com/DETERMINATION8192/pyaivoice.git
```

## Quickstart

## Quickstart

```python
from pyaivoice import AIVoice, Style

# Initialize the A.I.VOICE controller.
# `start_host=True` will automatically launch the editor.
aivoice = AIVoice(start_host=True)

# --- Basic Synthesis ---
text = "こんにちは、世界。"
aivoice.synthesis(text)

# --- Synthesis with Emotion ---
text = "感情を表現するのは、とっても楽しいな！"
aivoice.synthesis(text, style=Style.JOY)

# --- Direct Playback ---
text = "この音声はファイルに保存されず、直接再生されます。"
aivoice.synthesis(text, play=True)

# --- Waiting for Playback to Finish ---
# The play=True option is non-blocking.
# If you need to wait for playback to complete before your script exits, use the wait() method.
text_to_wait = "この文章の再生が終わるまで待ちます。"
aivoice.synthesis(text_to_wait, play=True)
print("Playback started. Waiting for it to finish...")
aivoice.wait()
print("Playback finished.")
```

## Contributing

Pull Requests and Issues are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
