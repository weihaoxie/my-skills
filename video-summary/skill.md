---
name: video-summary
description: Summarize YouTube videos into atomic note points with clickable timestamps. Use when user asks to summarize a YouTube video and write to a markdown note file. Handles: (1) Reading video link from markdown frontmatter or direct URL, (2) Downloading transcript with timestamps (tries zh-TW, zh-CN, en), (3) Converting Traditional Chinese to Simplified Chinese, (4) Summarizing into independent Zettelkasten-style points, (5) Writing summary back to file preserving frontmatter. Each point includes: title, clickable timestamp link, and detailed summary.
---

# Video Summary

## Quick Start

Get a YouTube video URL and summarize it into atomic note points with clickable timestamps.

**Input options:**
- Markdown file path with `link` field in frontmatter containing YouTube URL
- Direct YouTube URL (youtube.com/watch?v=xxx or youtu.be/xxx)

**Output format:**
```markdown
## 视频信息
- **讲师**: XXX
- **时长**: 约X小时
- **主题**: XXX

---

## 要点1：标题

**时间戳**: [MM:SS](https://www.youtube.com/watch?v=VIDEO_ID&t=XXXs)

### 详细总结

内容段落...

- 列表项1
- 列表项2

更多段落...

---
```

## Workflow

### Step 1: Get Video URL

If input is a markdown file, read it and extract YouTube URL from frontmatter `link` field. Otherwise use the provided URL directly.

Extract video ID from URL patterns:
- `youtube.com/watch?v=VIDEO_ID`
- `youtu.be/VIDEO_ID`
- `youtube.com/embed/VIDEO_ID`

### Step 2: Download Transcript

Use the transcript fetch script in `scripts/fetch_transcript.py`:

```bash
cd scripts && python fetch_transcript.py "VIDEO_ID"
```

The script tries multiple languages in order: `zh-TW`, `zh-CN`, `en`. Outputs to `transcripts/VIDEO_ID.txt` with timestamps in `[MM:SS]` or `[HH:MM:SS]` format.

### Step 3: Summarize Content

IMPORTANT: Videos can be very long (50k+ tokens). **Always use an agent** for summarization to handle large transcript files.

Launch agent with this prompt template:

```
你需要总结一个YouTube视频的字幕文件。

字幕文件位于：[TRANSCRIPT_PATH]

视频ID是：VIDEO_ID
视频URL是：https://www.youtube.com/watch?v=VIDEO_ID
视频标题：[VIDEO_TITLE]
演讲者：[SPEAKER]

这是关于[TOPIC]的视频。

**重要说明**：
- 字幕是繁体中文，你需要将输出转换为简体中文
- 这是一个长视频，字幕文件很大，请完整阅读后进行总结

请按照以下要求进行总结：
1. 完整阅读字幕文件（请使用Read工具分段读取，确保读完整个文件）
2. 将内容拆解成多个独立的要点
3. 每个要点给出相应的时间戳链接（格式：https://www.youtube.com/watch?v=VIDEO_ID&t=XXXs，其中XXX是秒数）
4. 每个要点要进行详细总结，让读者只看笔记就能理解视频在讲什么
5. 每个要点要独立，遵从原子化原则，可以用于卡片盒笔记法
6. 最终输出必须使用简体中文

输出格式要求：
## 视频信息
- **讲师**: [演讲者姓名]
- **时长**: 约X小时/分钟
- **主题**: [视频主题]

---

## 要点1：标题

**时间戳**: [MM:SS](https://www.youtube.com/watch?v=VIDEO_ID&t=XXXs)

### 详细总结

第一段内容...

- 要点列表1
- 要点列表2
- 要点列表3

第二段内容...

更多详细说明...

---

## 要点2：标题

（同上格式）

请直接输出最终的总结内容，使用简体中文。确保总结完整覆盖视频的主要内容。
```

### Step 4: Convert to Simplified Chinese (if needed)

If transcript is Traditional Chinese (zh-TW), convert output to Simplified Chinese using OpenCC or equivalent method.

### Step 5: Write to File

Read original file to preserve frontmatter, then write new content with:
1. Original YAML frontmatter (unchanged)
2. Updated `modified` timestamp
3. Video information section (讲师, 时长, 主题)
4. Summary content with atomic points
5. Each point section ends with `---` separator

## Output Format Details

### 视频信息 Section
Add this section after frontmatter and before the first point:
```markdown
## 视频信息
- **讲师**: [演讲者姓名/机构]
- **时长**: 约1.5小时 / 约60分钟
- **主题**: [视频主题概述]
```

### Each Point Section
```markdown
## 要点X：标题

**时间戳**: [MM:SS](https://www.youtube.com/watch?v=VIDEO_ID&t=XXXs)

### 详细总结

内容应该：
- 使用段落分段，不要写成一大段文字
- 使用列表（- 或 1.）来列举要点
- 保持详细但清晰，让读者能理解视频内容
- 每个要点相对独立，可用于卡片盒笔记法

---
```

## Scripts

### `scripts/fetch_transcript.py`

Fetches YouTube transcript with timestamps. Usage:

```bash
python fetch_transcript.py VIDEO_ID
```

Features:
- Tries multiple languages: zh-TW, zh-CN, en
- Outputs with timestamps in `[HH:MM:SS]` format
- Saves to `transcripts/VIDEO_ID.txt`
