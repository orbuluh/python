import jp_analyze_util
import re

def extend_verb_types(word: str, word_explain: str):
    m = re.search(".*\((.*)\)", word_explain)
    if m:
        word_type = m.group(1)
        if "verb" in word_type:
            detail_type = jp_analyze_util.get_verb_type(word)
            word_explain = word_explain.replace(")", f" {detail_type})")
    return word_explain


def sentence_analyze_normalizer(analyze: str):
    """
    Sometimes the sentence is just too long to fit in the video ....
    have to selectively remove some line from analyze table and hopefully
    we still have enough information to represent the analyze of sentence.
    """
    lines = analyze.split("\n")
    if (len(lines) < 12): return analyze
    lines = list(filter(lambda s: "Particle" not in s and "Conjunction" not in s,
                 lines))
    if (len(lines) < 12): return "\n".join(lines)
    lines = list(filter(lambda s: "Subject" not in s, lines))
    return "\n".join(lines)


def reconstruct_conversation_1(script: str):
    """
    Convert Gpt format to expected format ...
    Expected format:
        Person A: うーん、でもマイケル・ジョーダンは伝説的な存在だよ。|Hmmm, but Michael Jordan is a legendary figure.
    Gpt format:
        Person A: うーん、でもマイケル・ジョーダンは伝説的な存在だよ。
        (Uun, demo Maikeru Joodan wa densetsu-tekina sonzai da yo.)
        |Translation: Hmmm, but Michael Jordan is a legendary figure.
    """
    script = script.split('\n')
    cur = ""
    res = ""
    for line in script:
        if "Scene change" in line:
            res += line + '\n'
            continue
        if line:
            if len(cur) == 0:
                cur = line
            else:
                m = re.search("Translation: (.*)", line)
                if m:
                    res += cur + '|' + m.group(1) + '\n'
                    cur = ""
    return res