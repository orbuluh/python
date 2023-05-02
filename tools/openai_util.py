import api_util
import openai

import requests

openai.api_key = api_util.get_api_key("OPENAI_API_KEY")


def chat_complete(messages, temperature):
    # print(f"$> {prompt}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature
    )

    # For temperature, higher values like 0.8 will make the output more random,
    # while lower values like 0.2 will make it more focused and deterministic.
    # In the case of max tokens, if you want to limit a response to a certain
    # length, max tokens can be set to an arbitrary number. This may cause
    # issues for example. if you set the max tokens value to 5 since the output
    # will be cut-off and the result will not make sense to users.

    return (response.choices[0]['message']['content'].strip(),
            response.usage.total_tokens)


def img_gen(prompt, output_path):
    # print(f"$> {prompt}")
    generation_response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="url",
    )
    # any name you like; the filetype should be .png
    generated_image_filepath = output_path
    # extract image URL from response
    generated_image_url = generation_response["data"][0]["url"]
    print(generated_image_url)
    generated_image = requests.get(
        generated_image_url).content  # download the image

    with open(generated_image_filepath, "wb") as image_file:
        image_file.write(generated_image)


def whisper_speech_to_text(audio_file_path):
    with open(audio_file_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
        print(transcript['text'])
        return transcript['text']
