# TGRSS

[EN](README.md)/[ZH](README_zh.md)

Push RSS Feed through Telegram.

## Usage

To use this project, we highly recommend to use Github Action instead of deploy on your own server.

### Step 1 Fork this repository

Please fork this repository instead of creating Pull Requests.

### Step 2 Add Telegram token to secrets

1. Open your repository and click `Settings`.
2. Select `Secrets` → `Action`.
3. Click `New repository secret`.
4. Name the secret `TELEGRAM_TOKEN`, and value is the API Token from *@BotFather* of your telegram bot.

### Step 3 Get your chat_id

1. Clone your repository.
2. Run these commands below (Require Python 3.7 or higher).
    ```bash
    pip install -r requirements.txt
    python tools.py get_chat_id
    ```
3. Send a message to your bot, and you should be able to see you username and a string of numbers, that numbers are your `chat_id`.

### Step 4 Edit RSS list

Open `config.yml`. It's a yaml file, inside is my own RSS list. If you don't know what is **yaml**, we recommend you to learn it first from [here](https://learnxinyminutes.com/docs/yaml/), especially how to use anchors`&` and references`*`.

The `config.yml` currently has two fields.

The `rss_groups` contains groups that allow you to put multiple RSS sources into a "category". If two (or more) users subscribe some of the same sources, you can put thoses sources into a group and use anchors`&` and refrences`*` to add sources to users.

```yaml
rss_groups:
  group_1: &anchor_1
    rss_1: rss_1_url
    rss_2: rss_2_url
  group_2: &anchor_2
    rss_3: rss_3_url
```

The `chat_ids` contains `chat_id` of each user. you can add rss group to user, or just add delicated rss sources in it.

```yaml
chat_ids:
  your_chat_id:
    <<: *anchor_1
    rss_4: rss_4_url
```

### Step 5 Enable Github Action

1. Back to your repository, Click `Actions`.
2. Click `I understand my workflows, go ahead and enable them`.
3. Select `TGRSS_Action` on the left side.
4. Click `Enable workflow`.

### Step 6 Enjoy!

You have successfully set up your own Telegram RSS!