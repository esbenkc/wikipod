from wikipod import utils

if __name__ == "__main__":
    pages = [
        "https://en.wikipedia.org/wiki/Gravitational_singularity",
        "https://en.wikipedia.org/wiki/Black_hole",
        "https://en.wikipedia.org/wiki/Event_horizon",
        "https://en.wikipedia.org/wiki/Spacetime",
        "https://en.wikipedia.org/wiki/General_relativity",
    ]
    for page in pages:
        dict = utils.scrape_page_content(page)
        folder_name = utils.generate_output_file_name(dict)
        print("Reading '", dict["title"], "'...")
        content = utils.gpt4_clean_content(dict)
        # Write content to file
        print("Writing content to file...")
        utils.write_content_to_file(
            utils.format_for_web(content), "public/" + folder_name + "/index.html"
        )
        print("Generating audio...")
        utils.generate_audio(content, "public/" + folder_name + "/audio.mp3")
        print("Done!")
