import json
import tempfile
import unittest
from pathlib import Path

from content_creator.generator import (
    ContentGenerator,
    load_config,
    load_topics,
    slugify,
)


class GeneratorTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("World Cup 2026!"), "world-cup-2026")

    def test_generate_record(self):
        generator = ContentGenerator(
            {
                "hashtags": ["Shorts", "News"],
                "max_hashtags": 2,
                "title_template": "{topic} | Update",
                "description_template": "Latest: {topic}",
                "tags_template": "{topic}, update",
            }
        )

        result = generator.generate("NBA")

        self.assertEqual(result["topic"], "NBA")
        self.assertEqual(result["slug"], "nba")
        self.assertEqual(result["title"], "NBA | Update")
        self.assertEqual(result["hashtags"], "#Shorts #News")

    def test_empty_topic_rejected(self):
        with self.assertRaises(ValueError):
            ContentGenerator().generate("")

    def test_load_topics_ignores_comments(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "topics.txt"
            path.write_text("# comment\nNBA\n\nNFL\n", encoding="utf-8")

            self.assertEqual(load_topics(path), ["NBA", "NFL"])

    def test_load_config(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "config.json"
            path.write_text(
                json.dumps({"max_hashtags": 3}),
                encoding="utf-8",
            )

            config = load_config(path)
            self.assertEqual(config["max_hashtags"], 3)
            self.assertIn("title_template", config)


if __name__ == "__main__":
    unittest.main()
