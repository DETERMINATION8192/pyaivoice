import win32com.client
from enum import Enum
import json
from typing import Callable, TypeVar, ParamSpec, TypedDict, Literal, Concatenate, Optional
from dataclasses import dataclass, asdict, field
from functools import wraps
import time


P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class AIVoiceMasterControl():
    """A.I.VOICEのマスターコントロール設定"""
    Volume: float = 1.0
    Speed: float = 1.0
    Pitch: float = 1.0
    PitchRange: float = 1.0
    MiddlePause: int = 150
    LongPause: int = 378
    SentencePause: int = 800


class AIVoiceStyle(TypedDict):
    """ボイススタイル設定"""
    Name: Literal["J", "A", "S"]
    Value: float


class AIVoiceMergedVoice(TypedDict):
    """フュージョン先ボイス"""
    VoiceName: str


class AIVoiceMergedVoiceContainer(TypedDict):
    """ボイスフュージョン設定"""
    BasePitchVoiceName: str
    MergedVoices: list[AIVoiceMergedVoice]


@dataclass
class AIVoiceVoicePreset():
    """A.I.VOICEのボイスプリセット設定"""
    VoiceName: str  # VoiceNameだけは必須要素なので一番上に
    PresetName: str = "Python"
    Volume: float = 1.0
    Speed: float = 1.0
    Pitch: float = 1.0
    PitchRange: float = 1
    MiddlePause: int = 150
    LongPause: int = 370
    Styles: list[AIVoiceStyle] = field(default_factory=lambda: [{'Name': 'J', 'Value': 0}, {'Name': 'A', 'Value': 0}, {'Name': 'S', 'Value': 0}])
    MergedVoiceContainer: AIVoiceMergedVoiceContainer = field(default_factory=lambda: {"BasePitchVoiceName": "", "MergedVoices": []})


class Style(Enum):
    """スタイル"""
    NORMAL = 0
    JOY = 1
    ANGRY = 2
    SAD = 3


class HostStatus(Enum):
    """ホストプログラムの状態を表します"""
    NOT_RUNNING = 0
    NOT_CONNECTED = 1
    IDLE = 2
    BUSY = 3


def startup(main_func: Callable[Concatenate["AIVoice", P], R]) -> Callable[Concatenate["AIVoice", P], R]:
    """ホストプログラムの起動と接続を自動的に処理するデコレータ"""
    @wraps(main_func)
    def wrapper(self: "AIVoice", *args: P.args, **kwargs: P.kwargs) -> R:
        try:
            if self._tts_control.Status == HostStatus.NOT_RUNNING.value:    # pyright: ignore[reportPrivateUsage]
                self._tts_control.StartHost()                               # pyright: ignore[reportPrivateUsage]
            if self._tts_control.Status == HostStatus.NOT_CONNECTED.value:  # pyright: ignore[reportPrivateUsage]
                self._tts_control.Connect()                                 # pyright: ignore[reportPrivateUsage]
        except Exception as e:
            raise RuntimeError(f"ホストに接続できませんでした: {e}")
        try:
            returned = main_func(self, *args, **kwargs)
            return returned
        except AttributeError:
            raise
        except Exception as e:
            raise RuntimeError(
                f"{main_func.__name__}の実行中にエラーが発生しました: {e}"
            )

    return wrapper


class AIVoice():
    """A.I.VOICE Talk Editor APIを操作するためのメインクラス"""
    def __init__(self: "AIVoice", start_host: bool = False):
        """
        AIVoiceクラスのインスタンスを初期化します

        Args:
            start_host (bool, optional): 初期化時にホストを起動するかどうか、デフォルトはFalse
        """
        try:
            self._tts_control = win32com.client.Dispatch("AI.Talk.Editor.Api.TtsControl")
        except Exception:
            raise Exception("A.I.VOICE Talk Editor APIに接続できませんでした")
        current_host = self._tts_control.GetAvailableHostNames()[0]
        self._tts_control.Initialize(current_host)
        if start_host:
            self._tts_control.StartHost()

    @property
    @startup
    def version(self: "AIVoice"):
        """ホストプログラムのバージョンを取得します。"""
        return self._tts_control.Version

    @property
    @startup
    def voices(self: "AIVoice") -> dict[str, str]:
        """利用可能なすべてのボイスプリセットとボイス名のマッピングを取得します"""
        voice_names: tuple[str] = self._tts_control.VoiceNames
        return {
            preset.PresetName: preset.VoiceName
            for preset in [
                self.get_voice_preset(voice_name)
                for voice_name in voice_names
            ]
        }

    @startup
    def get_voice_preset(self: "AIVoice", preset_name: str = "Python") -> AIVoiceVoicePreset:
        """引数で指定された名称のボイスプリセットの各値を取得します。"""
        return AIVoiceVoicePreset(**json.loads(self._tts_control.GetVoicePreset(preset_name)))

    @startup
    def set_voice_preset(self: "AIVoice", voice_preset: AIVoiceVoicePreset):
        """ボイスプリセットの値を設定します"""
        try:
            self._tts_control.SetVoicePreset(json.dumps(asdict(voice_preset)))
        except Exception:
            self._tts_control.AddVoicePreset(json.dumps(asdict(voice_preset)))

    @property
    @startup
    def master_control(self: "AIVoice") -> AIVoiceMasterControl:
        """マスターコントロールの各値を取得または設定します。"""
        return AIVoiceMasterControl(**json.loads(self._tts_control.MasterControl))

    @master_control.setter
    @startup
    def master_control(self: "AIVoice", master_contrl: AIVoiceMasterControl):
        self._tts_control.MasterControl = json.dumps(asdict(master_contrl))

    @property
    def status(self: "AIVoice") -> HostStatus:
        """ホストプログラムの状態を取得します。"""
        return HostStatus(self._tts_control.Status)

    def start(self: "AIVoice"):
        """ホストプログラムを起動します"""
        self._tts_control.StartHost()

    def terminate(self: "AIVoice"):
        """ホストプログラムを終了します"""
        self._tts_control.TerminateHost()

    @startup
    def wait(self: "AIVoice"):
        while self._tts_control.Status == HostStatus.BUSY.value:
            time.sleep(0.01)

    @startup
    def synthesize(
        self: "AIVoice",
        text: str,
        voice: str = "",
        style: Style = Style.NORMAL,
        merged_voice_container: Optional[AIVoiceMergedVoiceContainer] = None,
        voice_preset: Optional[AIVoiceVoicePreset] = None,
        path: str = "./voice.wav",
        play: bool = False
    ):
        """
        指定されたテキストを音声に合成します

        Args:
            text (str): 合成するテキスト
            voice (str, optional): 使用するボイスの名前、デフォルトは利用可能な最初のボイス
            style (Style, optional): 感情スタイル、デフォルトは Style.NORMAL
            merged_voice_container (Optional[AIVoiceMergedVoiceContainer], optional): 使用するボイスフュージョンの設定
            voice_preset (Optional[AIVoiceVoicePreset], optional): 使用するボイスプリセット、選択された場合はvoice, style, merged_voice_containerのパラメータを無視してこれに設定された値を使用する
            path (str, optional): 音声ファイルの保存先パス、デフォルトは "./voice.wav"
            play (bool, optional): 合成した音声を即座に再生するかどうか、Trueの場合ファイルに保存されない、デフォルトは False
        """
        if not voice:
            voices = list(self.voices.values())
            voice = voices[0]
        if not voice_preset:
            voice_preset = AIVoiceVoicePreset(VoiceName=voice)
            if merged_voice_container:
                voice_preset.MergedVoiceContainer = merged_voice_container
            match style:
                case Style.NORMAL:
                    pass
                case Style.JOY:
                    voice_preset.Styles[0]["Value"] = 1.0
                case Style.ANGRY:
                    voice_preset.Styles[1]["Value"] = 1.0
                case Style.SAD:
                    voice_preset.Styles[2]["Value"] = 1.0
        self.set_voice_preset(voice_preset)
        self._tts_control.CurrentVoicePresetName = voice_preset.PresetName
        self._tts_control.Text = text
        if play:
            self._tts_control.Play()
            return
        self._tts_control.SaveAudioToFile(path)
