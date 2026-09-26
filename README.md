# Content Creator Toolkit

A lightweight, extensible Python toolkit for turning content topics into structured social-media metadata.

The project is designed for creators who want a repeatable workflow for generating:
- SEO-friendly titles
- Short descriptions
- Hashtag sets
- Search tags
- CSV content plans

It is intentionally dependency-free so it can run on Windows, macOS, Linux, or a basic Python environment.

## Features

- Simple command-line interface
- Batch processing from a plain-text topic list
- CSV export for content planning
- Configurable title and metadata templates
- Automatic hashtag normalization
- Slug generation for content identifiers
- Deterministic output that is easy to review and edit
- Unit tests using Python's built-in `unittest`
- No API key required

## Project structure

```text
content-creator-toolkit/
├── content_creator/
│   ├── __init__.py
│   └── generator.py
├── data/
│   └── topics.txt
├── output/
│   └── .gitkeep
├── tests/
│   └── test_generator.py
├── .gitignore
├── config.json
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- No third-party packages are required

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/jagirpatimone1/content-creator-toolkit.git
cd content-creator-toolkit
```

### 2. Add topics

Edit `data/topics.txt` and put one topic per line:

```text
World Cup 2026
NBA
NFL
Premier League
Hip Hop Music
R&B Music
```

### 3. Generate a content plan

```bash
python main.py
```

The generated CSV will be saved to:

```text
output/content_plan.csv
```

### 4. Run tests

```bash
python -m unittest discover -s tests -v
```

## Configuration

Edit `config.json` to change the templates.

Available placeholders:
- `{topic}`
- `{hashtags}`

Example:

```json
{
  "title_template": "{topic} — Quick Update & Key Details",
  "description_template": "A quick breakdown of {topic}. Follow for more fresh updates and useful content.",
  "hashtags": ["Shorts", "Trending", "News", "Update"],
  "max_hashtags": 7,
  "tags_template": "{topic}, trending, news, shorts, update"
}
```

## Output format

Each row contains:

| Field | Description |
|---|---|
| topic | Original topic |
| slug | URL/file-friendly identifier |
| title | Generated content title |
| description | Generated short description |
| hashtags | Space-separated hashtags |
| tags | Comma-separated search tags |

## Design principles

This toolkit focuses on predictable automation rather than pretending to know what will go viral. Metadata is generated from configurable rules and should be reviewed for accuracy and platform-specific requirements before publishing.

## Roadmap

Potential future modules:

- YouTube API integration
- TikTok metadata templates
- Instagram caption templates
- Content calendar generation
- Keyword clustering
- Duplicate-topic detection
- JSON export
- Markdown reports
- AI provider integrations as optional adapters

## License

MIT. See `LICENSE`.
