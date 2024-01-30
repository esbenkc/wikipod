import argparse
from wikipod import utils


def main(voice_id, pages, model):
    for page in pages:
        dict = utils.scrape_page_content(page)
        folder_name = utils.generate_output_file_name(dict)
        print("Reading '", dict["title"], "'...")
        content = utils.oai_clean_content(dict, model=model)
        # Write content to file
        print("Writing content to file...")
        utils.write_content_to_file(
            utils.format_for_web(content), "public/" + folder_name + "/index.html"
        )
        print("Generating audio...")
        utils.generate_audio(
            content, "public/" + folder_name + "/audio.mp3", voice_id=voice_id
        )
        print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some inputs.")
    parser.add_argument(
        "-v",
        "--voice_id",
        required=False,
        help="ID of the voice to use",
        default="UdScy37AbDCrWZuRANDL",
    )
    parser.add_argument(
        "-m", "--model", required=False, help="GPT model to use", default="gpt-4"
    )
    parser.add_argument(
        "-p",
        "--pages",
        nargs="+",
        required=True,
        help="List of Wikipedia pages",
        default=["https://en.wikipedia.org/wiki/Special:Random"],
    )

    args = parser.parse_args()

    main(
        args.voice_id,
        args.pages,
        args.model,
    )
