# Solana Social Buzz Tracker

This repo surfaces Solana tokens whose social “mindshare” spiked over a 24 h window—an early warning for potential hype/shill activity.

## Files

- **social_sentiment_tracker.py**  
  Main script. Pulls `percentageChange1d` from Messari Signal API, filters by threshold, outputs top N tokens.

- **top_solana_mindshare.json**  
  Sample output with tokens that passed the mindshare threshold.

- **requirements.txt**  
  Python dependencies.

## Setup

1. Clone this repo  
   ```bash
   git clone https://github.com/YOUR_USERNAME/solana-social-buzz-tracker.git
   cd solana-social-buzz-tracker
2. Create a virtual env & install
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
3. Set your Messari API key
   Ref: https://docs.messari.io/reference/introduction#api-key
   ```bash
   export MESSARI_KEY="…"
