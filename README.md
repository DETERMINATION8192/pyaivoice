# pyaivoice

<p align="right"><a href="./README.en.md">English</a></p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A.I.VOICE Talk EditorをPythonからシンプルに操作するライブラリ

## Requirements

- Windows OS
- Python 3.10+
- A.I.VOICE Talk Editor (v1.3.0以降)

## Installation 

```sh
pip install git+https://github.com/DETERMINATION8192/pyaivoice.git
```

## Quickstart

```python
from pyaivoice import AIVoice, Style

# A.I.VOICEコントローラーを初期化します。
# `start_host=True`を指定すると、エディタが自動で起動します。
aivoice = AIVoice(start_host=True)

# --- 基本的な音声合成 ---
text = "こんにちは、世界。"
aivoice.synthesis(text)

# --- 感情を適用した音声合成 ---
text = "感情を表現するのは、とっても楽しいな！"
aivoice.synthesis(text, style=Style.JOY)

# --- 音声のダイレクト再生 ---
text = "この音声はファイルに保存されず、直接再生されます。"
aivoice.synthesis(text, play=True)

# --- 再生完了を待機する ---
# play=Trueは非同期です。
# スクリプトが再生完了を待つ必要がある場合は、wait()メソッドを使用します。
text = "この文章の再生が終わるまで待ちます。"
aivoice.synthesis(text, play=True)
print("再生を開始しました。完了を待ちます...")
aivoice.wait()
print("再生が完了しました。")
```

## Contributing

Pull RequestやIssue等お気軽にどうぞ

## License

このプログラムはMITライセンスで利用できます- 詳細は[LICENSE](LICENSE)をご覧ください