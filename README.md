# 3commas bot

For FTX exchange, there is no start signal to trigger a composite bot ASAP. Although the same as Binance exchange, but using Binance, there is a `RSI-7 3min < 100` start condition to simulate this requirement.

This 3commas bot leverage GitHub Action to send start signal to composite every 5 minutes. It does not occupy any of your server resources.

But the shortage of this solution is that the minimum time interval of GitHub action is around 5 minutes, so not exactly as same as the ASAP start condition.

For more GitHub Action limitation, refer: https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration

### how to use
1. Firstly create a composite bot. add all the pair you want to run.
2. clone this repo to your account and change some config.
2. config the `config.py` file,  change you quote and  add all your pairs in step1 to the base.
3. push all the repo to your github repo and it is supposed to work.
