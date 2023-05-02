import openai_util
import re


def gen_word_explain(word):
    prompt = f"translate and provide type for {word}." +\
        " format: ori_word: meaning (type)`."

    return openai_util.chat_complete(
        [{"role": "user", "content": f"{prompt}"}], 0.5)


def gen_sentence_from_word(word):
    prompt = f"Create a Japanese sentence with dramatic scenario using {word}, " +\
        "under 10 words. Give translation in format En: translation."
    sentence, token_used = openai_util.chat_complete(
        [{"role": "user", "content": f"{prompt}"}], 0.8)
    sentence = sentence.replace("Ja:", "")
    sentence = sentence.replace("JA:", "")
    sentence = sentence.replace("日本語：", "")
    sentence = re.sub("Romaji:.*?\n", "", sentence)
    sentence = re.sub("(Note:.*?)\n", "", sentence)
    sentence = sentence.strip()

    translation = ""
    result = [s for s in sentence.split("\n") if s]

    if len(result) == 1:
        # print(f"post processing ...{sentence}")
        m = re.search("(.*)\W(En: .*)", sentence)
        sentence, translation = m.groups()
    else:
        try:
            sentence, translation = result
        except:
            print(sentence)
            print("unexpected output...")
            sys.exit()
    # sometimes, sentence is with its katakana translation from Kanji, remove it
    m = re.search(".*(\(.*\))", sentence)
    if m:
        sentence = sentence.replace(m.group(1), "").strip()
    # remove anchor for translation
    translation = translation.replace("En:", "").strip()
    return sentence, translation, token_used


def gen_jp_sentence_analyze(sentence):
    # You can shorten the prompt by removing some of the explanations and focusing
    # on the example input and output.
    prompt = f"""`{sentence}`: Break down to meaningful parts. For each part
    marking Romaji, functionality (subject, predicates, etc) and for each part
    denote Romaji with syllables separated by `-`. Example input: `食べた寿司が昨日美味しかった`
    Example output: `食べた ta-be-ta (Predicate): past tense of the verb 食べる (ta-beru, "to eat")
    寿司 su-shi (Subject): sushi
    が ga (Particle): marks the subject of the sentence
    昨日 ki-nou (Adverb) yesterday
    美味しかった o-i-shi-ka-tta (Predicate) past tense of the adjective 美味しい (o-i-shi-i, "delicious")`"""

    analyze, token_used = openai_util.chat_complete(
        [{"role": "user", "content": f"{prompt}"}], 0.3)
    # sometimes gpt repeat the input sentence again
    analyze = [line.strip() for line in analyze.split("\n")
               if line and sentence not in line]
    return "\n".join(analyze), token_used


def gen_jp_sentence_analyze_table(sentence):
    prompt = f"""`{sentence}`: breakdown the sentence, containing Romaji (`-` separated with syllable),
    role in the sentence, meaning, in a table format. Skip punctuations. For example. Input: `食べた寿司が昨日美味しかった`
    Expected output format:```| Word | Romaji | Role | Meaning |
    | --- | --- | --- | --- |
    | 食べた | ta-be-ta | Predicate | past tense of the verb 食べる (ta-beru, "to eat") |
    | 寿司 | su-shi | Subject | sushi |
    | が | ga | Particle | marks the subject of the sentence |
    | 昨日 | ki-nou | Adverb | yesterday |
    | 美味しかった | o-i-shi-ka-tta | Predicate | past tense of the adjective 美味しい (o-i-shi-i, "delicious") |"""

    # Always put the translation with format `Translation: english_translations` in one line
    return openai_util.chat_complete(
        [{"role": "user", "content": f"{prompt}"}], 0.3)
    # sometimes gpt repeat the input sentence again
    # analyze = [line.strip() for line in analyze.split("\n") if line and sentence not in line]
    # return "\n".join(analyze), token_used


def gen_verb_variations_sentences(word):
    # prompt = f"用字:{word} 的字典形,ます形,て形,た形,ない形,意志形,辭書形,假定形 分別造一個句子。每個句子少於20字。範例格式: `|型態|動詞變化|例句|En:英文翻譯|Ch:繁中翻譯|`"
    prompt = f"用字:{word} 的 辞書形,ます形,て形,た形,ない形,意志形,假定形,命令形,可能形,受動形,使役形,使役受動形 分別造句。每種型態造三個句子。每個句子少於15字範例格式: `|型態|動詞變化|例句1|En:英文翻譯|Ch:繁中翻譯|\n|型態|動詞變化|例句2|En:英文翻譯|Ch:繁中翻譯|\n|型態|動詞變化|例句3|En:英文翻譯|Ch:繁中翻譯|`"
    # prompt = f"用字:{word} 的 字典形 和 假定形 造句。每種型態各造三個句子。每個句子少於15字範例格式: `|型態|動詞變化|例句1|En:英文翻譯|Ch:繁中翻譯|\n|型態|動詞變化|例句2|En:英文翻譯|Ch:繁中翻譯|\n|型態|動詞變化|例句3|En:英文翻譯|Ch:繁中翻譯|`"
    sentences, token_used = openai_util.chat_complete(
        [{"role": "user", "content": f"{prompt}"}], 0.8)
    return sentences, token_used


def gen_conversations(scenario: str, script_format: str, side_note: str):
    prompt = f"Create a conversational script for scenario: {scenario}. " +\
             f"The script must have format like: `{script_format}`. {side_note}"
    print(f"prompt: {prompt}\n{'-'*50}\n")
    return openai_util.chat_complete(
        [{"role": "user", "content": f"{prompt}"}], 0.8)


def gen_image_from_desc(sentence, out_file_path):
    # image generation from translation ... quite expensive
    translation = ""
    for line in sentence.split("\n"):
        m = re.search("En: (.*)", line, re.IGNORECASE)
        if m:
            translation = m.group(1)
            break
    if translation:
        openai_util.img_gen(
            translation + " manga style, ink painting", out_file_path)

