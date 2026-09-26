"""Content metadata generation utilities."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_CONFIG: dict[str, Any] = {
    "title_template": "{topic} — Quick Update & Key Details",
    "description_template": (
        "A quick breakdown of {topic}. "
        "Follow for more fresh updates and useful content."
    ),
    "hashtags": ["Shorts", "Trending", "News", "Update"],
    "max_hashtags": 7,
    "tags_template": "{topic}, trending, news, shorts, update",
}


def load_config(path: Path) -> dict[str, Any]:
    """Load configuration and merge it with safe defaults."""
    if not path.exists():
        return DEFAULT_CONFIG.copy()

    with path.open("r", encoding="utf-8") as file:
        user_config = json.load(file)

    config = DEFAULT_CONFIG.copy()
    config.update(user_config)
    return config


def load_topics(path: Path) -> list[str]:
    """Read non-empty, non-comment topic lines from a text file."""
    if not path.exists():
        return []

    topics: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        topic = line.strip()
        if topic and not topic.startswith("#"):
            topics.append(topic)

    return topics


def slugify(value: str) -> str:
    """Create a stable lowercase slug from a topic."""
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"[\s-]+", "-", value)
    return value.strip("-")


def normalize_hashtag(value: str) -> str:
    """Convert a hashtag label into a valid simple hashtag."""
    cleaned = re.sub(r"[^A-Za-z0-9_]", "", value)
    return f"#{cleaned}" if cleaned else ""


class ContentGenerator:
    """Generate structured metadata from content topics."""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = {**DEFAULT_CONFIG, **(config or {})}

    def generate(self, topic: str) -> dict[str, str]:
        """Generate one content metadata record."""
        topic = topic.strip()
        if not topic:
            raise ValueError("Topic cannot be empty.")

        hashtag_values = self.config.get("hashtags", [])
        max_hashtags = int(self.config.get("max_hashtags", 7))
        hashtags = [
            normalize_hashtag(str(item))
            for item in hashtag_values[:max_hashtags]
        ]
        hashtags = [item for item in hashtags if item]

        title = self.config["title_template"].format(
            topic=topic,
            hashtags=" ".join(hashtags),
        )
        description = self.config["description_template"].format(
            topic=topic,
            hashtags=" ".join(hashtags),
        )
        tags = self.config["tags_template"].format(
            topic=topic,
            hashtags=" ".join(hashtags),
        )

        return {
            "topic": topic,
            "slug": slugify(topic),
            "title": title.strip(),
            "description": description.strip(),
            "hashtags": " ".join(hashtags),
            "tags": tags.strip(),
        }

    def generate_many(self, topics: list[str]) -> list[dict[str, str]]:
        """Generate records for multiple topics."""
        return [self.generate(topic) for topic in topics if topic.strip()]

    def write_csv(self, topics: list[str], output_path: Path) -> None:
        """Generate records and write them to a UTF-8 CSV file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        rows = self.generate_many(topics)

        fieldnames = ["topic", "slug", "title", "description", "hashtags", "tags"]

        with output_path.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
