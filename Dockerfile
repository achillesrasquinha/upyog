FROM  python:3.7-alpine

LABEL maintainer=achillesrasquinha@gmail.com

ENV BPYUTILS_PATH=/usr/local/src/bpyutils

RUN apk add --no-cache \
        bash \
        git \
    && mkdir -p $BPYUTILS_PATH

COPY . $BPYUTILS_PATH
COPY ./docker/entrypoint.sh /entrypoint
RUN sed -i 's/\r//' /entrypoint \
	&& chmod +x /entrypoint

WORKDIR $BPYUTILS_PATH

RUN pip install -r ./requirements.txt && \
    python setup.py install

ENTRYPOINT ["/entrypoint"]

CMD ["bpyutils"]