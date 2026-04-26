import re
import os
from collections import Counter

chapters = ["1", "2", "3", "4", "5", "6", "8"]

all_en_text = ""
for ch in chapters:
    en_file = f"Bilbiie/textbook-Ch{ch}.qmd"
    if os.path.exists(en_file):
        with open(en_file, 'r', encoding='utf-8') as f:
            all_en_text += f.read() + " "

# Remove equations and markdown syntax
all_en_text = re.sub(r'\$\$?[^\$]+\$\$?', ' ', all_en_text)
all_en_text = re.sub(r'\[\^[^\]]+\]', ' ', all_en_text)
all_en_text = re.sub(r'#+\s', ' ', all_en_text)

# Extract word bi-grams and tri-grams (simple noun phrases)
words = re.findall(r'[A-Za-z\-]+', all_en_text)

stop_words = set(["the", "and", "to", "of", "a", "in", "is", "that", "for", "with", "as", "by", "this", "are", "on", "we", "be", "an", "which", "from", "it", "model", "models", "chapter", "have", "not", "but", "can", "their", "or", "has", "these", "at", "also", "its", "they", "all", "our", "will", "more", "an", "when", "how", "what", "who", "where", "why", "there", "then", "than", "so", "if", "only", "such", "other", "some", "any", "no", "do", "does", "did", "was", "were", "been", "being", "would", "could", "should", "may", "might", "must", "about", "into", "through", "after", "before", "over", "under", "between", "out", "up", "down", "very", "much", "many", "most", "less", "least", "same", "different", "use", "using", "used", "see", "show", "shows", "shown", "find", "finds", "found", "case", "cases", "paper", "papers", "book", "textbook", "author", "authors", "literature", "research", "study", "studies", "results", "result", "analysis", "approach", "framework", "section", "figure", "table", "equation", "equations", "variables", "variable", "parameter", "parameters", "value", "values", "function", "functions", "condition", "conditions", "assume", "assumes", "assuming", "assumption", "assumptions", "imply", "implies", "implying", "implication", "implications", "show", "shows", "showing", "give", "gives", "given", "take", "takes", "taking", "make", "makes", "making", "set", "sets", "setting", "get", "gets", "getting", "let", "lets", "letting", "one", "two", "three", "first", "second", "third", "i", "e", "g", "t", "s", "h", "y", "c", "r", "p", "w", "b", "m", "n", "k", "l", "j", "d", "v", "u", "f", "q", "x", "z", "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega"])

filtered_words = [w.lower() for w in words if w.lower() not in stop_words and len(w) > 2]

bigrams = [" ".join(filtered_words[i:i+2]) for i in range(len(filtered_words)-1)]

bigram_counts = Counter(bigrams)
print("Top 100 Bigrams:")
for b, c in bigram_counts.most_common(100):
    print(f"{b}: {c}")

print("\nTop 100 Unigrams:")
unigram_counts = Counter(filtered_words)
for u, c in unigram_counts.most_common(100):
    print(f"{u}: {c}")

