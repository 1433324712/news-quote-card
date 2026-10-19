---
name: news-quote-card
description: Turn a news/interview video (X or any URL) into a bilingual ZH+EN social pack — 3 vertical quote cards + a short 1080x1920 subtitle video — using only real transcribed quotes.
---
# news-quote-card

## 1. Extract & analyze
`python3 extract.py --url <X post or .mp4 URL> --outdir /workspace/raw/<slug> [--lang en] [--frames 5,30,92]`
→ transcript.txt (segment timestamps), words.txt (word timestamps), frames/, contact.jpg. Read transcript + contact sheet.
FIRST check the clip actually covers the post's claimed points (posts often summarize a longer full interview); if not, stop and report the mismatch before making anything.
For zh audio use --model medium (small garbles terms, e.g. Q-Day→QAIS). Pick quotes ONLY from transcript; never invent or paraphrase inside quote marks. Interpretive framing goes in headlines only. Translate EN→ZH faithfully.

## 2. Cards (1080x1440)
`python3 render_card.py --frame F.png --tag '人物 媒体 专访 | NAME' --headline '中文\n标题' --headline_en '...' --quote '“…”' --quote_en '"…"' --out 01.png [--frame-y 420]`
Design: BG #0A0A0C, 8px #76B900 top bar, green tag Bold34, white ZH headline Bold78, grey EN Regular38, 16:9 frame 1080x608 centered, yellow #FFD600 ZH quote Bold52, EN Regular36. Noto Sans CJK SC. Typical pack: hook / key quote / takeaway.

## 3. Short video (1080x1920)
`python3 make_video.py --video V.mp4 --start 89.7 --end 96.95 --duration 6 --fit --title '中文标题' --title_en '...' --subs '1.6|“我不认同那些|"I don'\''t approve of' --subs '3.95|…|…' --subs '0|…|…' --out 04.mp4`
Use words.txt for start/end; sub t_end in OUTPUT time (source offset / speed). --fit = atempo (keeps pitch) when quote is longer than duration; report speed.

If the source has burned-in subs, pass --crop w:h:x:y (16:9, above the sub band) to both render_card.py and make_video.py, e.g. 1067:600:0:0 for 720p.

## 4. Verify & caption
ffprobe duration; Read cards + 3 video frames. Write bilingual caption + hashtags. Report quotes with timestamps.
