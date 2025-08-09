"""マスターコントロールの操作サンプル"""

from pyaivoice import AIVoice, AIVoiceMasterControl


def main():
    aivoice = AIVoice(start_host=True)

    # --- 1. 現在のマスターコントロールを取得して表示 ---
    original_control = aivoice.master_control
    print("[1] 現在のマスターコントロール設定")
    print(f"- 全体音量: {original_control.Volume}")
    print(f"- 全体話速: {original_control.Speed}")
    print(f"- 全体ピッチ: {original_control.Pitch}")

    # --- 2. マスターコントロールの値を変更して設定 ---
    print("\n[2] マスターコントロールを変更します (音量: 0.8, 話速: 1.2)")
    new_control = AIVoiceMasterControl(Volume=0.8, Speed=1.2)
    aivoice.master_control = new_control

    # 変更後の設定で音声合成
    text_1 = "マスターコントロールを調整しました。少しゆっくり、小さく話します。"
    aivoice.synthesis(text_1, path="./output_master_control.wav")
    print("-> 変更後の音声 `output_master_control.wav` を保存しました。")
    # --- 3. マスターコントロールを元の設定に戻す ---
    print("\n[3] マスターコントロールを元の設定に戻します...")
    aivoice.master_control = original_control
    print("-> 設定を元に戻しました。")
    print("\n処理が完了しました。")


if __name__ == "__main__":
    main()
