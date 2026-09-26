"""Command-line entry point for Content Creator Toolkit."""

from pathlib import Path

from content_creator.generator import ContentGenerator, load_config, load_topics


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
TOPICS_PATH = BASE_DIR / "data" / "topics.txt"
OUTPUT_PATH = BASE_DIR / "output" / "content_plan.csv"


def main() -> None:
    config = load_config(CONFIG_PATH)
    topics = load_topics(TOPICS_PATH)

    if not topics:
        print(f"No topics found in {TOPICS_PATH}")
        return

    generator = ContentGenerator(config)
    generator.write_csv(topics, OUTPUT_PATH)

    print(f"Generated {len(topics)} content records.")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
