import boto3

polly = boto3.client('polly', region_name='ap-northeast-1')

# voice list: https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
# Neural JP Voices: Takumi, Kazuha, Tomoko


def text_to_speech(text: str, voice_id: str = 'Kazuha',
                   output_file_name: str = "output.mp3"):
    response = polly.synthesize_speech(
        Text=text,
        VoiceId=voice_id,
        OutputFormat='mp3',
        Engine='neural',
    )

    with open(output_file_name, 'wb') as file:
        file.write(response['AudioStream'].read())
