"""カスタムボイスプリセットの作成と利用サンプル"""

from pyaivoice import AIVoice, AIVoiceVoicePreset


def main():
    aivoice = AIVoice(start_host=True)
    voices = aivoice.voices
    if not voices:
        print("利用可能なボイスがありません。")
        return

    # 使用するボイスを選択 (最初のボイスを利用)
    target_voice = list(voices.values())[0]
    print(f"使用するボイス: {target_voice}")

    # --- 1. カスタムボイスプリセットを作成 ---
    print("\n[1] カスタムボイスプリセットのパラメータを定義します。")
    custom_preset = AIVoiceVoicePreset(
        PresetName="MyCustomPreset",
        VoiceName=target_voice,
        Volume=1.2,       # 音量
        Speed=0.9,        # 話速
        Pitch=1.1,        # 高さ
        PitchRange=1.2,   # 抑揚
        MiddlePause=200,  # 短ポーズ
        LongPause=500     # 長ポーズ
    )
    print(f"- プリセット名: {custom_preset.PresetName}")
    print(f"- パラメータ: Volume={custom_preset.Volume}, Speed={custom_preset.Speed}, Pitch={custom_preset.Pitch}")

    # --- 2. 作成したプリセットで音声合成 ---
    print("\n[2] 作成したプリセットを使って音声合成します。")
    text = "これは、詳細なパラメータを設定したカスタムプリセットのテストです。"

    # synthesisの引数に直接voice_presetを渡します
    aivoice.synthesis(
        text,
        voice_preset=custom_preset,
        path="./output_custom_preset.wav"
    )
    print("-> カスタムプリセットの音声 `output_custom_preset.wav` を保存しました。")
    print("\n処理が完了しました。")


if __name__ == "__main__":
    main()
