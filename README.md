# 3commas bot manager

### Docker

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

### Usage

```
python3 harmonic_trade.py -x 59800 -a 58800 -b BTC
```
