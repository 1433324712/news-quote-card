# news-quote-card

把一段采访或新闻视频做成双语社交素材：三张竖版引用图卡，外加一条烧录字幕的短视频。引号里只用真实转写，不编造、不改写。

Turn an interview or news video into a bilingual social pack: vertical quote cards and a short video with burned-in subtitles. Quotes inside quotation marks come only from the real transcript.

- 图卡 **1080×1440**（中文 + 英文）
- 短视频 **6 秒**、**1080×1920**，烧录双语字幕

- Quote cards **1080×1440** (Chinese + English)
- A **6s** **1080×1920** video with burned-in bilingual subtitles

## 依赖 / Dependencies

- python3
- ffmpeg（含 ffprobe）
- Pillow
- numpy
- faster-whisper
- Noto Sans CJK SC（`/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc` 与 `NotoSansCJK-Regular.ttc`，index 2 = SC）
- yt-dlp（可选；非直链 `.mp4` 时用来下载，例如 X 帖子）

## 用法 / Usage

示例取自 `SKILL.md`。

### 1. 提取与转写 / Extract and transcribe

```bash
python3 extract.py --url <X post or .mp4 URL> --outdir /workspace/raw/<slug> [--lang en] [--frames 5,30,92]
```

中文音频用 `--model medium`（`small` 会把专有名词听错，例如 Q-Day→QAIS）。先核对成片是否覆盖帖子声称的要点；对不上就停，不要继续做图。

For Chinese audio use `--model medium` (`small` garbles terms, e.g. Q-Day→QAIS). First check the clip actually covers the post's claimed points; if not, stop and report the mismatch.

### 2. 图卡 1080×1440 / Quote cards

```bash
python3 render_card.py --frame F.png --tag '人物 媒体 专访 | NAME' --headline '中文\n标题' --headline_en '...' --quote '“…”' --quote_en '"…"' --out 01.png [--frame-y 420]
```

常见一套三张：钩子 / 关键引语 / 结论。

Typical pack: hook / key quote / takeaway.

### 3. 短视频 1080×1920 / Short video

```bash
python3 make_video.py --video V.mp4 --start 89.7 --end 96.95 --duration 6 --fit --title '中文标题' --title_en '...' --subs '1.6|“我不认同那些|"I don'\''t approve of' --subs '3.95|…|…' --subs '0|…|…' --out 04.mp4
```

用 `words.txt` 定 `--start` / `--end`。`--subs` 里的 `t_end` 是成片时间。`--fit` 在引语长于 `--duration` 时用 `atempo`（保持音高），并打印速度。

Use `words.txt` for `--start` / `--end`. Sub `t_end` is in output time. `--fit` applies `atempo` (pitch kept) when the quote is longer than `--duration`, and prints the speed.

源片已有烧录字幕时，给 `render_card.py` 和 `make_video.py` 都加上 `--crop w:h:x:y`（16:9，裁在字幕带上方），例如 720p 用 `1067:600:0:0`。

If the source has burned-in subs, pass `--crop w:h:x:y` (16:9, above the sub band) to both `render_card.py` and `make_video.py`, e.g. `1067:600:0:0` for 720p.
