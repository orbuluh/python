import os
import sys
import subprocess
from google.cloud import speech
import asyncio

def seconds_to_hhmmss(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

async def transcribe_audio_segment(audio_path, start_time, lang_code, channel_cnt, duration):
    client = speech.SpeechClient()
    start_time_in_hhmmss = seconds_to_hhmmss(start_time)
    temp_chunk_path = f'{audio_path}_tmp_{start_time}.wav'

    os.system(f'ffmpeg -ss {start_time} -t {duration} -i {audio_path} {temp_chunk_path}')

    with open(temp_chunk_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #sample_rate_hertz=16000,
        audio_channel_count=channel_cnt,
        language_code=lang_code,
        alternative_language_codes=['en-US'],
        enable_automatic_punctuation=True,
    )

    # Process the specific segment
    operation = client.long_running_recognize(config=config, audio=audio)
    print(f"Processing segment starting at {start_time} for {duration} seconds")
    response = await asyncio.get_event_loop().run_in_executor(None, operation.result)
    transcriptions = [result.alternatives[0].transcript for result in response.results]
    os.remove(temp_chunk_path)
    return ' '.join(transcriptions)

async def main(file_path, output_file_path, lang_code='zh-TW', channel_cnt = 2, chunk_duration = 45):
    duration_cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file_path}'
    duration = float(os.popen(duration_cmd).read())
    tasks = []
    for start_time in range(0, int(duration), chunk_duration):
        tasks.append(transcribe_audio_segment(file_path, start_time, lang_code, channel_cnt, chunk_duration))

    results = await asyncio.gather(*tasks)

    full_transcription = ' '.join(results)
    with open(output_file_path, 'w') as output_file:
        output_file.write(full_transcription + '\n')
    print(f"Transcription saved to {output_file_path}")


if __name__ == '__main__':
    if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
        print("export GOOGLE_APPLICATION_CREDENTIALS!!!")
        sys.exit(1)

    video_url = "https://youtu.be/Iuzz98Ay1_k"
    #video_lang_code = "zh-TW"
    #video_lang_code = "en-US"
    #video_lang_code = "zh-CN"
    video_lang_code = "ja-JP"
    title_cmd = f"yt-dlp --get-title {video_url}"
    process = subprocess.run(title_cmd.split(), capture_output=True, text=True)
    title = process.stdout.strip()
    download_cmd = f"yt-dlp -x --audio-format opus -o tmp.opus {video_url}"
    process = subprocess.run(download_cmd.split(), capture_output=True, text=True)
    asyncio.run(main("tmp.opus", f"{title}_{video_lang_code}.txt", video_lang_code))
    os.remove("tmp.opus")

    #title = "recording"
    #asyncio.run(main("recording.wav", f"{title}_{video_lang_code}.txt", video_lang_code))