import os
import random
import re
import sys
from random import choices, choice

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    # Calculate PageRank using the sampling method
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    # Calculate PageRank using the iterative method
    ranks = iterate_pagerank(corpus, DAMPING)
    print("PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links.
    """
    pages = dict()
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = set(
                re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            )
            pages[filename] = set(link for link in links if link in os.listdir(directory))
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    The return value is a dictionary mapping page names to probabilities.
    """
    links = corpus[page]
    prob_distribution = {}
    if links:
        for p in corpus.keys():
            if p in links:
                prob_distribution[p] = (((1 - damping_factor) / len(corpus)) + (damping_factor / len(links)))
            else:
                prob_distribution[p] = (1 - damping_factor) / len(corpus)
    else:
        for p in corpus.keys():
            prob_distribution[p] = 1 / len(corpus)

    return prob_distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return a dictionary mapping page names to their PageRank values,
    estimated using sampling.

    The proportion of samples for each page is its PageRank estimate.
    """
    start = choice(list(corpus.keys()))
    counts = {page: 0 for page in corpus.keys()}
    counts[start] += 1
    for i in range(n):
        prob_distribution = transition_model(corpus, start, damping_factor)
        new = choices(list(prob_distribution.keys()), weights=list(prob_distribution.values()), k=1)[0]
        counts[new] += 1
        start = new

    return {page : value / n for page, value in counts.items()}

def iterate_pagerank(corpus, damping_factor):
    """
    Return a dictionary mapping page names to their PageRank values,
    calculated using the iterative formula.
    
    The process stops when no PageRank value changes by more than 0.001.
    """
    page_rank = {key : (1/len(corpus)) for key in corpus.keys()}
    incomings = {p: set() for p in corpus.keys()}
    for p, links in corpus.items():
        for link in links:
            incomings[link].add(p)
    random = (1 - damping_factor) / len(corpus)
    while True:
        for p in corpus.keys():
            summing = 0
            for i in incomings[p]:
                summing += page_rank[i] / len(corpus[i])

            new_rank = random + (damping_factor * summing)
            if abs(new_rank - page_rank[p]) > 0.001:
                page_rank[p] = new_rank
            else:
                return {key : value/sum(page_rank.values()) for key , value in page_rank.items()}

if __name__ == "__main__":
    main()
