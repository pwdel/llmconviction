FROM python:3.12-bookworm


SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

ARG USER=llmbot
ARG UID=1000
ARG GID=1000

RUN groupadd --gid $GID $USER && \
    useradd --uid $UID --gid $GID --shell /bin/bash --create-home $USER

WORKDIR /app

RUN apt-get update && apt-get install -y    \
        curl                                \
        wget                                \
        unzip                               \
        nano                                \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --chown=$USER:$USER requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN chown -R $USER:$USER /app

USER $USER

CMD ["/bin/bash"]
