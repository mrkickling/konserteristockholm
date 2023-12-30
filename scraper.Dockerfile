FROM python:3.11

# Copy files
COPY python/concert_scraper/ /opt/concert_scraper
COPY python/requirements.txt /opt/concert_scraper/requirements.txt
COPY python/pyproject.toml /opt/concert_scraper/pyproject.toml

ENV DEBIAN_FRONTEND noninteractive
ENV GECKODRIVER_VER v0.29.0
ENV FIREFOX_VER 87.0
 
RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y \
       firefox-esr
 
# Add latest FireFox
RUN set -x \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox
  
# Add geckodriver
RUN set -x \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/

WORKDIR /opt/concert_scraper
RUN ls
RUN pip install --upgrade pip
RUN pip install -e .

ENTRYPOINT [ "python", "scraper.py" ]