FROM node:22-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV BGLS_HOME=/opt/browserglass

RUN apt-get update \
  && apt-get install -y --no-install-recommends git chromium ca-certificates dumb-init fonts-liberation \
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
COPY tools/ima-browserglass/server.mjs ./
COPY tools/ima-browserglass/viewer.html ./viewer.html

ENV PORT=10000
ENV BGLS_INTERNAL_PORT=7799
ENV BGLS_DATA_DIR=/opt/browserglass/bgls-data
ENV CHROME_BIN=/usr/bin/chromium

EXPOSE 10000

ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.mjs"]
