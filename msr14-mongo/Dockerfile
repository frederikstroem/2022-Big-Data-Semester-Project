FROM mongo

RUN apt update && apt install -y wget
RUN wget -q --show-progress http://ghtorrent-downloads.ewi.tudelft.nl/datasets/msr14-mongo.tar.gz
RUN tar -xvzf msr14-mongo.tar.gz
RUN mongorestore -d msr14 msr14
