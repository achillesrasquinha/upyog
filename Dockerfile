FROM  python:3.7-alpine

LABEL maintainer=achillesrasquinha@gmail.com

ENV BPYUTILS_PATH=/usr/local/src/bpyutils

RUN apk add --no-cache \
        bash \
        git \
    && mkdir -p $BPYUTILS_PATH

COPY . $BPYUTILS_PATH
COPY ./docker/entrypoint.sh /entrypoint.sh

RUN pip install $BPYUTILS_PATH

WORKDIR $BPYUTILS_PATH

ENTRYPOINT ["/entrypoint.sh"]

CMD ["bpyutils"]