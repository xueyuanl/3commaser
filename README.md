# 3commas bot

For FTX exchange, there is no start signal to trigger a composite bot ASAP. Although the same as Binance exchange, but using Binance, there is a `RSI-7 3min < 100` start condition to simulate this requirement.

This 3commas bot leverage GitHub Action to send start signal to composite every 5 minutes. It does not occupy any of your server resources.

But the shortage of this solution is that the minimum time interval of GitHub action is around 5 minutes, so not exactly as same as the ASAP start condition.

For more GitHub Action limitation, refer: https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration

### how to use
1. Firstly create some composite bots, add all the pair you want to run and write down the ids of them.
2. Clone this repo to your account and change some config.
2. Just Add your bot ids in the list in the `config.py` file.
3. Push the change to your new repo, just like that.

# Docker

```
docker build -t 3commas .

# add your api key first
docker run -it --rm \
-v $PWD/bot_strategies.json:/bot_strategies.json \
-v $PWD/config.json:/config.json \
--name 3commas \
-p 3333:3333 \
--env API_KEY=$API_KEY \
--env SECRET=$SECRET \
3commas /bin/bash

# test
# docker exec -it 3commas /bin/bash
```
