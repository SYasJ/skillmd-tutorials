"""score.py - compare a Whisper transcript with the script we actually read.
usage: python3 score.py reference.txt out/clip.txt
Word error rate = (substitutions + deletions + insertions) / words in the reference."""
import re, sys
NUM = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
def words(path):
    t = open(path).read().lower().replace("-", " ")
    t = re.sub(r"\b(\d+)\b", lambda m: NUM[int(m.group(1))] if int(m.group(1)) < 21 else m.group(1), t)
    t = t.replace("31", "thirty one")
    return re.findall(r"[a-z0-9']+", t)
ref, hyp = words(sys.argv[1]), words(sys.argv[2])
# edit distance on words
d = list(range(len(hyp) + 1))
for i, r in enumerate(ref, 1):
    prev, d[0] = d[0], i
    for j, h in enumerate(hyp, 1):
        cur = min(d[j] + 1, d[j-1] + 1, prev + (r != h))
        prev, d[j] = d[j], cur
errors = d[len(hyp)]
text = " ".join(hyp)
print(f"reference words : {len(ref)}")
print(f"word errors     : {errors}")
print(f"word error rate : {100*errors/len(ref):.1f}%")
for term in ["claude code", "ollama", "json", "gemma"]:
    want = " ".join(ref).count(term)
    got = text.count(term)
    print(f"  '{term}': {got} of {want} correct")
