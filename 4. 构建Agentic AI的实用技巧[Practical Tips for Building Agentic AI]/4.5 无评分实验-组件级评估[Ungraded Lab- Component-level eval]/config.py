"""Configuration for component-level evaluation experiment."""

# Model configuration
MODEL_NAME = "google:gemini-2.5-flash-lite"
MAX_TURNS = 5  # Maximum tool calling iterations

# Preferred domains for evaluation
TOP_DOMAINS = {
    # General reference / institutions / publishers
    "wikipedia.org", "nature.com", "science.org", "sciencemag.org", "cell.com",
    "mit.edu", "stanford.edu", "harvard.edu", "nasa.gov", "noaa.gov", "europa.eu",

    # CS/AI conferences and indexes
    "arxiv.org", "acm.org", "ieee.org", "neurips.cc", "icml.cc", "openreview.net",

    # Other authoritative publishers
    "elifesciences.org", "pnas.org", "jmlr.org", "springer.com", "sciencedirect.com",

    # Additional domains
    "pbs.org", "nova.edu", "nvcc.edu", "cccco.edu",

    # Programming sites
    "codecademy.com", "datacamp.com"
}

# Evaluation thresholds
MIN_RATIO = 0.4  # Minimum 40% of results should be from preferred domains

# Research task configuration
DEFAULT_RESEARCH_TASK = "Find 2-3 key papers and reliable reviews on the latest advances in black hole science."
