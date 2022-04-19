# TGRSS_Action

[EN](README.md)/[ZH](README_zh.md)

通过Telegram推送RSS订阅。

## 用法

我们强烈建议您通过Github Action的方式使用此项目，而不是将其部署在自己的服务器上。

### 步骤 1 Fork 这个仓库

请fork这个参考而不是创建Pull Requests。

### Step 2 将 Telegram token 添加到 secrets

1. 打开您的仓库并点击 `Settings`。
2. 选择 `Secrets` → `Action`。
3. 点击 `New repository secret`。
4. 将 secret 命名为 `TELEGRAM_TOKEN`，并且将值设置为从 *@BotFather* 获取到的您bot的 API Token。

### Step 3 获取你的 chat_id

1. 克隆这个项目到本地。
2. 运行下面的命令 (需要 Python 3.7 或更高)。
    ```bash
    pip install -r requirements.txt
    python tools.py get_chat_id
    ```
3. 向您的bot发送一条消息, 您应该可以在shell中看到您的用户名和一串数组，这个数字就是您的 `chat_id`。

### Step 4 编辑 RSS 列表

打开 `config.yml`. 这是一个 yaml 文件，里面是我自己的 RSS 订阅。如果您不知道什么是 **yaml**，我们建议您先在 [这里](https://learnxinyminutes.com/docs/zh-cn/yaml-cn/) 学习一下，特别是如何使用 锚点`&` 和 引用`*`。

`config.yml` 目前有两个字段。

`rss_groups` 包含了可以让您将多个RSS源归为一个“类别”的订阅组。如果多个用户同时订阅了相同的源，您就可以将这些源放进一个订阅组中，并且使用 锚点`&` 和 应用`*` 来将他们添加给订阅的用户。

```yaml
rss_groups:
  组_1: &anchor_1
    订阅_1: 订阅_1_地址
    订阅_2: 订阅_2_地址
  组_2: &anchor_2
    订阅_3: 订阅_3_地址
```

`chat_ids` 包含了每个用户的 `chat_id`。 您可以将订阅组添加给用户，或者直接添加单独的订阅。

```yaml
chat_ids:
  您的chat_id:
    <<: *anchor_1
    订阅_4: 订阅_4_地址
```

### Step 5 启用 Github Action

1. 回到您的仓库，点击 `Actions`。
2. 点击 `I understand my workflows, go ahead and enable them`。
3. 在左边的Workflows中选择 `TGRSS_Action`。
4. 点击 `Enable workflow`。

### Step 6 享受吧!

你已经成功配置好了您的 Telegram RSS！