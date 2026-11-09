"""把 BreezyVoice（鍾孟修的聲音）做好的字卡旁白轉成 mp3，寫進 index.html 的 NARR 對照表。
用法：python3 voice-src/build_voice.py   （已完成幾句就接幾句，可重跑）
旁白稿：voice-src/narr.json（x＝字卡上的文字、s＝實際唸的句子），narr.txt 給 say_batch.py 用。
"""
import json, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTS = pathlib.Path("/Users/matt/居家社區健身/voice-clone/output/poker_narr_parts")
lines = json.loads((ROOT / "voice-src/narr.json").read_text())
(ROOT / "voice").mkdir(exist_ok=True)

narr = {}
for i, line in enumerate(lines):
    wav = PARTS / f"{i:02d}.wav"   # say_batch.py numbers parts from 00
    if not wav.exists():
        continue
    mp3 = ROOT / f"voice/n{i:02d}.mp3"
    if not mp3.exists() or mp3.stat().st_mtime < wav.stat().st_mtime:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af", "loudnorm=I=-16:TP=-1.5",
                        "-ac", "1", "-ar", "24000", "-b:a", "64k", str(mp3)], check=True)
    narr[line["x"]] = f"voice/n{i:02d}.mp3"

html = (ROOT / "index.html").read_text()
html = re.sub(r"const NARR = \{.*?\};", "const NARR = " + json.dumps(narr, ensure_ascii=False) + ";", html, count=1, flags=re.S)
(ROOT / "index.html").write_text(html)
print(f"{len(narr)} / {len(lines)} 句旁白已接上")
