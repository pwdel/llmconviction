# Base image with Python 3.12 and Debian Bookworm Slim
FROM python:3.12-bookworm

# Set a non-root user (llmbot)
ARG USER=llmbot
ARG UID=1000
ARG GID=1000

# Create a non-root user and group
RUN groupadd --gid $GID $USER && \
    useradd --uid $UID --gid $GID --shell /bin/bash --create-home $USER

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y    \
        curl                                \
        wget                                \
        unzip                               \
        nano                                \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY --chown=$USER:$USER requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set permissions for the non-root user
RUN chown -R $USER:$USER /app

# Switch to the non-root user
USER $USER

# Default command (bash for interactive use)
CMD ["/bin/bash"]
