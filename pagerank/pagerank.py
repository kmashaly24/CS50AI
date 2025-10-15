import os
import random
import re
import sys
from random import choice

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus[page]
    n = len(links)
    if n == 0:
        links = corpus.keys()
        n = len(links)
    else:
        prob_distr = {page : (1 - damping_factor) / (n + 1)}
        for link in links:
            prob_distr[link] = prob_distr[page] + (damping_factor / n)
        return prob_distr


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    start_page = choice(list(corpus.keys()))
    prob_distr = transition_model(corpus, start_page, damping_factor)
    page_rank = {key : 0 for key in corpus.keys()}
    page_rank[start_page] += 1
    for _ in range(n - 1):
        next_page = random.choices(
            list(prob_distr.keys()),
            weights=list(prob_distr.values()),
            k=1
        )[0]
        page_rank[next_page] += 1
        prob_distr = transition_model(corpus, next_page, damping_factor)
    for key in page_rank.keys():
        page_rank[key] /= n
    return page_rank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {key : 1 / len(corpus) for key in corpus.keys()}
    for key in corpus.keys():
        incoming_links = [page for page in corpus.keys() if key in corpus[page]]
        total = 0
        for page in incoming_links:
            total += page_rank[page] / len(corpus[page])
        new_rank = (1 - damping_factor) / len(corpus) + damping_factor * total
        while abs(new_rank - page_rank[key]) >= 0.001:
            page_rank[key] = new_rank
            total = 0
            for page in incoming_links:
                total += page_rank[page] / len(corpus[page])
            new_rank = (1 - damping_factor) / len(corpus) + damping_factor * total
        page_rank[key] = (1 - damping_factor) / len(corpus) + damping_factor * total
    return page_rank


if __name__ == "__main__":
    main()

