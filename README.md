# llmconviction

# Test Out a Bot Designed

Test out a bot designed to use LLM's to classify sentiment and conviction level so that we can experiment with conformal prediction.

## Start Up and Shut Down Remote GPU Virtual Private Server

### Quickstart - Testing Out a CPU Instance Launch

* This quickstart assumes a reasonably updated MacOS or Linux Machine with`docker` as well as `docker compose` installed. Ensure you are using `docker compose` and not the deprecated `docker-compose`.

1. Within `./app/` create a directory `./app/keys/`, which MUST STAY ON THE `.gitignore` file as `keys/`.
2. Add a file `digital_ocean_key` and put your Digital Ocean API key in here. Again DO NOT REMOTE `keys/` from the `.gitignore` file for risk of leaking this online.
3. Add a directory `./app/keys/google_ai_studio/` and put your Google AI Studio / Gemini key in that file.
4. Navigate to the root directory in your terminal and do: `./run start` ... which will start up a containerized service.
5. Your terminal will put you within the containerized service at `root@container:/app#`. From here you can see that you have access to directories `app/` and `keys/` as well as `requirements.txt`.
6. Do `exit`, which will allow you to exit from the container. You can get back into the container with `./run bash`.
7. Having confirmed that, you can run a few different python scripts.

* `./app/test [QUERY]` will generate a response from an input query.
* `./app/readnews --output [FILE] [TOPIC]` will read news about "TOPIC" to the file "OUTPUT" with the default being `news_result.csv`
* `./app/sentiment --topic [TOPIC] --file [FILE] --output [OUTPUT]` gives a `json` formatted output sentiment and conviction level on a particular topic found in a particular file, based upon `gemini-1.5-flash`.
* For example: `./app/sentiment --topic "nvidia" --file "exported_news.csv" --output "sentiment_result_20250202"`