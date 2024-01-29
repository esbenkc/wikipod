<img align="left" src="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png" width="150">

# The WikiPod

The WikiPod is the easiest way for you to generate podcast episodes out of your favorite Wikipedia pages!

See a few examples here:

- [Black holes](https://kran.ai/wikipod/Black_hole) &ndash; you won't be able to escape this topic's gravitational pull!
- [Event horizon](https://kran.ai/wikipod/Event_horizon) &ndash; don't expect events in the horizon for this one...
- [Spacetime](https://kran.ai/wikipod/Spacetime) &ndash; you thought they were separate? think again

## Getting started

Create a `.secret` file with your OpenAI API key and your Eleven Labs API key:

```
ELEVEN_LABS_API_KEY=<xi-api-key>
OPENAI_API_KEY=<openai-api-key>
```

Now run the bash command to begin wikipodding your very favorite Wikipedia pages!

```
python main.py -p https://en.wikipedia.org/wiki/Python_(programming_language) https://en.wikipedia.org/wiki/Artificial_intelligence
```

You can edit the following variables:

- `-v` or `--voice_id`: ID of the voice to use for audio generation. Default is UdScy37AbDCrWZuRANDL.
- `-m` or `--model`: The GPT model to use for content cleaning. Default is gpt4.
- `-p` or `--pages`: A list of Wikipedia page URLs to process. This argument is required. Default is a random Wikipedia page.

## Output

The script will scrape the specified Wikipedia pages, clean the content, and save it in an HTML file in the public/ directory. It will also generate an audio file in MP3 format in the same directory that is included in the HTML file.

<br clear="left"/>
