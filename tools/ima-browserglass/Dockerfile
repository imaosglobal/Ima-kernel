FROM node:22-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV BGLS_HOME=/opt/browserglass

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates curl gnupg dumb-init fonts-liberation \
  && install -d -m 0755 /etc/apt/keyrings \
  && curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg \
  && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends google-chrome-stable \
  && google-chrome --version \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN git clone --depth 1 https://github.com/psmux/browserglass.git /opt/browserglass \
  && cd /opt/browserglass \
  && corepack enable \
  && pnpm install --frozen-lockfile \
  && pnpm -r build

WORKDIR /opt/ima-browserglass
COPY tools/ima-browserglass/package.json ./
RUN npm install --omit=dev
COPY tools/ima-browserglass/server.mjs ./server.mjs
COPY tools/ima-browserglass/viewer.html ./viewer.html

ENV PORT=10000
ENV BGLS_INTERNAL_PORT=7799
ENV BGLS_DATA_DIR=/opt/browserglass/bgls-data
ENV CHROME_BIN=/usr/bin/google-chrome-stable
ENV BGLS_CHROME_PATH=/usr/bin/google-chrome-stable

EXPOSE 10000

ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.mjs"]
