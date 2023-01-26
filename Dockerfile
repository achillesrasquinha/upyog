FROM  python:3.7-alpine

ARG DEVELOPMENT=false

LABEL maintainer=achillesrasquinha@gmail.com

ENV UPYOG_PATH=/usr/local/src/upyog

RUN apk add --no-cache \
        bash \
        git \
    && mkdir -p $UPYOG_PATH

COPY . $UPYOG_PATH
COPY ./docker/entrypoint.sh /entrypoint
RUN sed -i 's/\r//' /entrypoint \
	&& chmod +x /entrypoint

WORKDIR $UPYOG_PATH

RUN if [[ "${DEVELOPMENT}" ]]; then \
        apk add --no-cache \
            gcc \
            musl-dev \
            libffi-dev \
            python3-dev \
            make \
            git; \
        pip install -r ./requirements-dev.txt; \
        python setup.py develop; \
    else \
        pip install -r ./requirements.txt; \
        python setup.py install; \
    fi

ENTRYPOINT ["/entrypoint"]

CMD ["upyog"]