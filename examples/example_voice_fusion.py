"""ボイスフュージョン機能のサンプル"""

from pyaivoice import AIVoice, AIVoiceMergedVoice, AIVoiceMergedVoiceContainer


def main():
    aivoice = AIVoice(start_host=True)
    voices = aivoice.voices

    # --- 1. ボイスフュージョンが利用可能かチェック ---
    if len(voices) < 2:
        print("ボイスフュージョンを利用するには、少なくとも2種類以上のボイスが必要です。")
        return
    voice_list = list(voices.values())
    base_voice = voice_list[0]
    fusion_voice = voice_list[1]

    print("[1] ボイスフュージョンの設定を定義します。")
    print(f"- ベースボイス (高さ): {base_voice}")
    print(f"- フュージョンボイス (声質): {fusion_voice}")

    # --- 2. ボイスフュージョンの設定を作成 ---
    # BasePitchVoiceName: 声の高さ（ピッチ）のベースになるボイス
    # MergedVoices: 声質のベースになるボイス（複数指定可能）
    fusion_setting = AIVoiceMergedVoiceContainer(
        BasePitchVoiceName=base_voice,
        MergedVoices=[
            AIVoiceMergedVoice(VoiceName=fusion_voice)
        ]
    )

    # --- 3. 作成した設定で音声合成 ---
    print("\n[2] ボイスフュージョンを使って音声合成します。")
    text = "これは、ボイスフュージョンのテストです。二人の声を混ぜ合わせています。"

    # synthesisの引数にmerged_voice_containerを渡します
    aivoice.synthesis(
        text,
        merged_voice_container=fusion_setting,
        path="./output_voice_fusion.wav"
    )
    print("-> ボイスフュージョンの音声 `output_voice_fusion.wav` を保存しました。")
    print("\n処理が完了しました。")


if __name__ == "__main__":
    main()
