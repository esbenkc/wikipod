import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI
import re
import markdown


def scrape_page_content(wiki_url):
    """
    Scrapes the content of a Wikipedia page.
    :param wiki_url: The URL of the Wikipedia page to scrape.
    :return: A dictionary containing the title, URL, and content of the page.
    """
    # Get the page content
    page_content = requests.get(wiki_url).content
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(page_content, "html.parser")
    # Get the title of the page
    title = soup.find(id="firstHeading").text
    # Get the content of the page
    content = soup.find(id="mw-content-text").text
    # Get the URL of the page
    url = soup.find(id="mw-content-text").find("a").get("href")
    # Return the page content
    return {"title": title, "url": url, "content": content, "wiki_url": wiki_url}


def generate_output_file_name(dict):
    """
    Generates the output file name.
    :param dict: The dictionary containing the content of the page.
    :return: The output file name.
    """
    # Generate the output file name
    output_folder_name = (
        dict["title"]
        .replace(" ", "_")
        .replace(":", "")
        .replace("?", "")
        .replace("!", "")
        .replace("'", "")
        .replace('"', "")
        .replace(",", "")
        .replace(".", "")
        .replace(";", "")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "")
        .replace("\\", "")
        .replace("’", "")
        .replace("“", "")
        .replace("”", "")
        .replace("–", "")
        .replace("—", "")
    )
    return output_folder_name


def read_api_key(file_name, key_name):
    with open(file_name, "r") as file:
        for line in file:
            if key_name in line:
                key, value = line.strip().split("=", 1)
                return value
    return None


def get_random_wiki_article():
    """
    Gets a random Wikipedia article.
    :return: A dictionary containing the title, URL, and content of the page.
    """
    # Get a random Wikipedia article
    wiki_url = "https://en.wikipedia.org/wiki/Special:Random"
    # Scrape the page content
    dict = scrape_page_content(wiki_url)
    return dict


def gpt4_clean_content(dict):
    """
    Cleans the content of a Wikipedia page.
    :param content: The content to clean.
    :return: The cleaned content.
    """
    # Remove after See also
    dict["content"] = dict["content"].split("\nSee also")[0]

    # Remove "Retrieved from" and everything on the same line
    lines = dict["content"].split("\n")
    for line in lines:
        if "Retrieved from" in line:
            dict["content"] = dict["content"].replace(line, "")
        if "is a stub" in line:
            dict["content"] = dict["content"].replace(line, "")
        if "^ " in line:
            dict["content"] = dict["content"].replace(line, "")
        if "\nReferences" in line:
            dict["content"] = dict["content"].replace(line, "")

    # Remove all bracketed text
    dict["content"] = re.sub(r"\[.*?\]", "", dict["content"])

    # Concate the title and content
    dict["content"] = dict["title"] + ". " + dict["content"]

    # Call the OpenAI API by reading OPENAI_API_KEY from the .secret file
    client = OpenAI(
        api_key=read_api_key(".secret", "OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are talented at reformatting Wikipedia articles into concise text.",
            },
            {
                "role": "user",
                "content": 'Rewrite the following Wikipedia article in markdown and focus ONLY on the content. Remove things that seem like they are not part of the content and make it all very readable. Don\'t worry about references or years, remove long lists and just quickly summarize them, and remove anything that decreases the readability of the text.\n\n"""\n'
                + dict["content"]
                + '\n"""\n\n---\n\nRewritten Wikipedia article:\n\n"""\n',
            },
        ],
    )
    content = response.choices[0].message.content
    print(content)

    # Return the response's output
    return content


def manual_clean_content(dict):
    """
    Cleans the content of a Wikipedia page.
    :param content: The content to clean.
    :return: The cleaned content.
    """
    # # Remove everything in the References section
    dict["content"] = dict["content"].split("\nReferences")[0]
    # # Remove after the Retrieved from
    # dict["content"] = dict["content"].split("Retrieved from")[0]

    # Remove the first line
    dict["content"] = dict["content"].split("\n", 1)[1]

    # Remove after See also
    dict["content"] = dict["content"].split("\nSee also")[0]

    # Remove "Retrieved from" and everything on the same line
    lines = dict["content"].split("\n")
    for line in lines:
        if "Retrieved from" in line:
            dict["content"] = dict["content"].replace(line, "")
        if "is a stub" in line:
            dict["content"] = dict["content"].replace(line, "")
        if "^ " in line:
            dict["content"] = dict["content"].replace(line, "")
        if "\nReferences\n" in line:
            dict["content"] = dict["content"].replace(line, "")

    # Remove all bracketed text
    dict["content"] = re.sub(r"\[.*?\]", "", dict["content"])

    # Concate the title and content
    dict["content"] = dict["title"] + ". " + dict["content"]
    content = dict["content"]
    return content


def generate_audio(content, file_name):
    """
    Reads the content of a Wikipedia page using the ElevenT Labs API.
    :param dict: The dictionary containing the content of the page.
    :return: The content of the page as an MP3 file.
    """
    import requests

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/UdScy37AbDCrWZuRANDL"
    # Esben CEO: UdScy37AbDCrWZuRANDL
    # Joanne: pZUH6e3t8ERpSXkrg4I1

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": read_api_key(".secret", "ELEVEN_LABS_API_KEY"),
    }

    data = {
        "text": content,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    response = requests.post(url, json=data, headers=headers)

    with open(file_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)


def write_content_to_file(content, file_name):
    """
    Writes the content of a Wikipedia page to a file.
    :param content: The content to write.
    :param file_name: The name of the file to write to.
    """
    # Create the output folder
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    # Write the content to a file
    with open(file_name, "w") as file:
        file.write(content)


def format_for_web(content):
    content = (
        """<head><link rel="stylesheet" href="../style.css" />
    <title contenteditable="true">Wikipod - """
        + content.split("#")[1].split("\n")[0]
        + """</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/gh/greghub/green-audio-player/dist/css/green-audio-player.min.css">
<script src="https://cdn.jsdelivr.net/gh/greghub/green-audio-player/dist/js/green-audio-player.min.js"></script>
    </head>
    <body>
  <div class="container">

    <div class="reading">
        <audio>
            <source src="./audio.mp3" type="audio/mpeg">
        </audio>
    </div>"""
        + markdown.markdown(content)
        + """</div><script>
        new GreenAudioPlayer(".reading")
    </script>
    </body>"""
    )
    return content
