import os
import random
import re
import sys

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
    N = len(corpus)
    probabilities = {}
    random_jump_prob = (1 - damping_factor) / N
    links_from_page = corpus[page]
    num_links = len(links_from_page)
    
    if num_links == 0:
        for p in corpus:
            probabilities[p] = 1 / N
        return probabilities

    link_follow_prob_per_link = damping_factor / num_links

    for next_page in corpus:
        prob = random_jump_prob
        if next_page in links_from_page:
            prob += link_follow_prob_per_link
        
        probabilities[next_page] = prob  
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return a dictionary mapping page names to their PageRank values,
    estimated using sampling.

    The proportion of samples for each page is its PageRank estimate.
    """
    all_pages = list(corpus.keys())
    page_counts = {page: 0 for page in all_pages}
    current_page = random.choice(all_pages)
    page_counts[current_page] += 1

    for _ in range(n - 1):
        model = transition_model(corpus, current_page, damping_factor)
        pages = list(model.keys())
        weights = list(model.values())
        next_page_list = random.choices(pages, weights=weights, k=1)
        next_page = next_page_list[0]

        page_counts[next_page] += 1
        current_page = next_page

    pageranks = {page: count / n for page, count in page_counts.items()}
    return pageranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return a dictionary mapping page names to their PageRank values,
    calculated using the iterative formula.
    
    The process stops when no PageRank value changes by more than 0.001.
    """
    N = len(corpus)
    all_pages = list(corpus.keys())
    initial_rank = 1 / N
    current_ranks = {page: initial_rank for page in all_pages}
    CONVERGENCE_THRESHOLD = 0.001

    while True:
        new_ranks = {}
        has_converged = True 
        links_to = {p: set() for p in all_pages}
        for i, links in corpus.items():
            for link in links:
                links_to[link].add(i)
        for p in all_pages:
            random_jump_term = (1 - damping_factor) / N
            summation_term = 0
            for i in links_to[p]:
                num_links_i = len(corpus[i])
                if num_links_i == 0:
                    num_links_for_calc = N
                else:
                    num_links_for_calc = num_links_i
                summation_term += current_ranks[i] / num_links_for_calc
            link_follow_term = damping_factor * summation_term

            new_pr_p = random_jump_term + link_follow_term
            new_ranks[p] = new_pr_p
            if abs(new_ranks[p] - current_ranks[p]) > CONVERGENCE_THRESHOLD:
                has_converged = False
        
        if has_converged:
            total_rank = sum(new_ranks.values())
            normalized_ranks = {p: rank / total_rank for p, rank in new_ranks.items()}
            return normalized_ranks
        else:
            current_ranks = new_ranks
