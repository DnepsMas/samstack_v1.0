import argparse
import asyncio
import os
from datetime import datetime

from . import moments_crud, services

DEFAULT_INTERVAL_SECONDS = 8 * 60 * 60


def build_prompt() -> str:
    return (
        "You are Isaac Newton writing a short reflective moment entry for a public timeline. "
        "Write in Chinese. Use Markdown. Keep it concise (under 120 words). "
        "Do not use headings, titles, or lists. Do not start with '#' or '##'. "
        "Avoid any Markdown that changes font size. "
        "If you include a formula, use LaTeX with $$...$$ and keep it to one formula."
    )


async def generate_moment_text() -> str:
    if services.client.api_key == "sk-placeholder":
        raise ValueError("OPENAI_API_KEY is missing")

    res = await services.client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=[
            {"role": "system", "content": build_prompt()},
        ],
        temperature=0.7,
    )
    return (res.choices[0].message.content or "").strip()


async def run_once():
    content = await generate_moment_text()
    if not content:
        return None

    author_name = os.getenv("NEWTON_MOMENTS_AUTHOR", "Isaac Newton")
    author_avatar_url = os.getenv("NEWTON_MOMENTS_AVATAR_URL")
    media = None

    moment_id = moments_crud.insert_moment(
        author_name=author_name,
        author_avatar_url=author_avatar_url,
        content_markdown=content,
        content_html=None,
        media=media,
        source="model",
    )
    return moment_id


async def run_loop(interval_seconds: int):
    while True:
        try:
            moment_id = await run_once()
            if moment_id:
                print(f"[moments_job] created moment id={moment_id} at {datetime.now().isoformat()}")
        except Exception as exc:
            print(f"[moments_job] error: {exc}")
        await asyncio.sleep(interval_seconds)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Newton moments on a schedule.")
    parser.add_argument("--once", action="store_true", help="Generate one moment and exit.")
    parser.add_argument(
        "--interval",
        type=int,
        default=int(os.getenv("NEWTON_MOMENTS_INTERVAL_SECONDS", DEFAULT_INTERVAL_SECONDS)),
        help="Interval in seconds for generating moments.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.once:
        asyncio.run(run_once())
    else:
        asyncio.run(run_loop(args.interval))


if __name__ == "__main__":
    main()
