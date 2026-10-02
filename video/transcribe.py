import os
import sys
import time
import datetime
import wave
import numpy as np
import mlx_whisper

def format_timestamp_srt(seconds: float) -> str:
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def format_timestamp_readable(seconds: float) -> str:
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

def is_hallucination(text: str) -> bool:
    t = text.strip()
    hallucinations = [
        "ご視聴ありがとうございました",
        "チャンネル登録よろしくお願いします",
        "チャンネル登録をお願いします",
        "最後までご視聴いただき",
        "サブタイトル:",
        "視聴ありがとうございました",
    ]
    for h in hallucinations:
        if h in t and len(t) < len(h) + 10:
            return True
    return False

def main():
    audio_path = "video/audio_16k_mono.wav"
    output_base = "video/GMT20260922-111227_transcript"
    
    if not os.path.exists(audio_path):
        print(f"Error: {audio_path} not found.", flush=True)
        sys.exit(1)
        
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 音声データを読み込んでいます...", flush=True)
    with wave.open(audio_path, "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        
        # 冒頭の無音区間 (0:00〜18:15) をスキップ
        # 音声開始は18:20頃なので、18:10 (1090秒) から読み込む
        offset_sec = 1090
        offset_frames = offset_sec * framerate
        wf.setpos(offset_frames)
        frames = wf.readframes(n_frames - offset_frames)
        
    total_duration_sec = n_frames / framerate
    active_duration_sec = len(frames) / (framerate * sampwidth)
    print(f"  全体長: {total_duration_sec/60:.1f}分, 文字起こし対象(18:10以降): {active_duration_sec/60:.1f}分", flush=True)
    
    # 16bit PCM to float32 (-1.0 to 1.0)
    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 高精度文字起こしを開始します (M3 Pro MLX GPU加速)...", flush=True)
    print("モデル: mlx-community/whisper-large-v3-turbo (言語: 日本語, 無音スキップ&ループ防止有効)", flush=True)
    
    start_time = time.time()
    
    initial_prompt = "大学院マクロ経済学の講義。ニューケインジアン、動学的一般均衡モデル、DSGE、IS曲線、フィリップス曲線、金融政策、テイラールール、カリブレーション、最適化。"
    
    # condition_on_previous_text=False でハルシネーション・リピートループを完全防止
    result = mlx_whisper.transcribe(
        audio,
        path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
        language="ja",
        initial_prompt=initial_prompt,
        condition_on_previous_text=False,
        verbose=False
    )
    
    elapsed = time.time() - start_time
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 文字起こし完了! 所要時間: {elapsed/60:.2f} 分", flush=True)
    
    raw_segments = result.get("segments", [])
    valid_segments = []
    
    # タイムスタンプを動画全体の時間に補正 (offset_sec を加算)
    for seg in raw_segments:
        text = seg["text"].strip()
        if not text or is_hallucination(text):
            continue
        valid_segments.append({
            "start": seg["start"] + offset_sec,
            "end": seg["end"] + offset_sec,
            "text": text
        })
        
    print(f"有効セグメント数: {len(valid_segments)} / {len(raw_segments)}", flush=True)
    
    # 1. タイムスタンプ付き Markdown の保存
    md_path = f"{output_base}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 講義動画 文字起こし\n\n")
        f.write(f"- 対象ファイル: `video/GMT20260922-111227_Recording_1680x892.mp4`\n")
        f.write(f"- 処理日時: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- 動画の長さ: {total_duration_sec/60:.1f}分 (無音区間 0:00〜18:10 を除く講義本編: {active_duration_sec/60:.1f}分)\n")
        f.write(f"- 処理時間: {elapsed/60:.2f}分 (M3 Pro MLX GPU加速)\n")
        f.write(f"- 使用モデル: `mlx-community/whisper-large-v3-turbo`\n\n")
        f.write("## タイムライン付き文字起こし\n\n")
        
        for seg in valid_segments:
            start_str = format_timestamp_readable(seg["start"])
            end_str = format_timestamp_readable(seg["end"])
            text = seg["text"]
            f.write(f"**[{start_str} - {end_str}]** {text}\n\n")
            
    print(f"Markdown保存完了: {md_path}", flush=True)
    
    # 2. SRT 字幕ファイルの保存
    srt_path = f"{output_base}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(valid_segments, 1):
            start_str = format_timestamp_srt(seg["start"])
            end_str = format_timestamp_srt(seg["end"])
            text = seg["text"]
            f.write(f"{i}\n{start_str} --> {end_str}\n{text}\n\n")
            
    print(f"SRT字幕保存完了: {srt_path}", flush=True)
    
    # 3. プレーンテキストの保存
    txt_path = f"{output_base}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        for seg in valid_segments:
            f.write(seg["text"] + "\n")
            
    print(f"テキスト保存完了: {txt_path}", flush=True)
    print("すべての出力が完了しました。", flush=True)

if __name__ == "__main__":
    main()
