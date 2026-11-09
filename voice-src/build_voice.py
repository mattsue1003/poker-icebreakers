"""字卡旁白：用 edge-tts 台灣男聲（zh-TW-YunJheNeural）唸，寫進 index.html 的 NARR 對照表。
用法：python3 voice-src/build_voice.py   （已做好的會跳過，可重跑）
旁白稿：voice-src/narr.json（x＝字卡上的文字、s＝實際唸的句子）。
"""
import json, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
EDGE = str(pathlib.Path.home() / "Library/Python/3.14/bin/edge-tts")
VOICE, RATE = "zh-TW-YunJheNeural", "+0%"
lines = json.loads((ROOT / "voice-src/narr.json").read_text())
(ROOT / "voice").mkdir(exist_ok=True)

narr = {}
for i, line in enumerate(lines):
    mp3 = ROOT / f"voice/n{i:02d}.mp3"
    stamp = ROOT / f"voice/n{i:02d}.txt"
    if not mp3.exists() or not stamp.exists() or stamp.read_text() != VOICE + line["s"]:
        subprocess.run([EDGE, "--voice", VOICE, f"--rate={RATE}", "--text", line["s"], "--write-media", str(mp3)], check=True, capture_output=True)
        stamp.write_text(VOICE + line["s"])
    narr[line["x"]] = f"voice/n{i:02d}.mp3"

html = (ROOT / "index.html").read_text()
html = re.sub(r"const NARR = \{.*?\};", "const NARR = " + json.dumps(narr, ensure_ascii=False) + ";", html, count=1, flags=re.S)
html = html.replace("// NARR: 字卡文字 → 語音檔，見 voice-src/ 與 build_voice.py", "// NARR: 字卡文字 → 語音檔（edge-tts 台灣男聲），見 voice-src/build_voice.py")
html = html.replace("/* ---- voice: 字卡旁白（鍾孟修的聲音）與喊名字 ---- */", "/* ---- voice: 字卡旁白與喊名字 ---- */")
(ROOT / "index.html").write_text(html)
print(f"{len(narr)} / {len(lines)} 句旁白已接上")
