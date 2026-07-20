# CFSF Bot

專為 CFSF 社群設計的多功能 Discord 機器人，基於 [discord.py](https://github.com/Rapptz/discord.py) 構建。採用模組化的 Cog 架構，方便日後輕鬆擴充新功能。

> 本專案目前正積極開發中。更多功能將陸續推出。

---

## 目前功能

- **多國語言翻譯** — 透過 Google 翻譯在繁體中文、英文與日文之間進行翻譯。翻譯後的訊息會以發送者的名稱與頭像透過 Webhook 傳送。
- **熱重載 Cog 模組** — 可在不重新啟動機器人的情況下，於執行期（Runtime）載入、卸載或重新載入功能模組。
- **斜線指令同步** — 支援靈活的應用程式指令同步，可同步至全域（Global）範圍或特定伺服器（Guild）。
- **結構化日誌** — 透過 `logging_config.py` 進行可配置的日誌記錄。
- **基於 TOML 的設定檔** — 簡單且易讀的設定檔格式。

---

## 前提條件

- Python **3.13+**
- 推薦使用 [`uv`](https://github.com/astral-sh/uv) 或使用 `pip`

---

## 安裝與設定

### 1. 複製儲存庫

```bash
git clone https://github.com/your-username/CFSF_bot.git
cd CFSF_bot
```

### 2. 安裝依賴套件

使用 `uv`（推薦）：
```bash
uv sync
```

或使用 `pip`：
```bash
pip install -e .
```

### 3. 設定環境變數

在專案根目錄建立一個 `.env` 檔案：

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

### 4. 設定機器人

編輯 [`config/general.toml`](config/general.toml) 以設定機器人名稱與指令前綴：

```toml
[bot]
name = "CFSF bot"
command_prefix = ["!", "?"]
```

### 5. 執行機器人

```bash
python main.py
```

---

## 指令說明

所有指令皆使用前綴 `!` 或 `?`。

### 翻譯功能

翻譯後的訊息將會以**您的名稱與頭像**透過 Webhook 發送，且系統會自動刪除原始訊息以保持版面整潔。

#### 單向翻譯

| 指令 | 說明 |
|---|---|
| `!zh-en <文字>` | 繁體中文 → 英文 |
| `!zh-ja <文字>` | 繁體中文 → 日文 |
| `!en-zh <文字>` | 英文 → 繁體中文 |
| `!en-ja <文字>` | 英文 → 日文 |
| `!ja-zh <文字>` | 日文 → 繁體中文 |
| `!ja-en <文字>` | 日文 → 英文 |

#### 多向翻譯

| 指令 | 說明 |
|---|---|
| `!tzh <文字>` | 中文 → 其他所有已設定的語言 |
| `!ten <文字>` | 英文 → 其他所有已設定的語言 |
| `!tja <文字>` | 日文 → 其他所有已設定的語言 |

> **注意：** 目標頻道需啟用「管理 Webhook（Manage Webhooks）」權限。

---

### 機器人管理（僅限擁有者）

| 指令 | 說明 |
|---|---|
| `!sync` | 全域同步斜線指令 |
| `!sync ~` | 同步斜線指令至目前伺服器 |
| `!sync *` | 將全域指令複製到目前伺服器 |
| `!sync ^` | 清除目前伺服器的斜線指令 |
| `!sync <GuildID...>` | 透過 ID 同步指令至特定伺服器 |
| `!sync help` | 顯示同步指令的使用說明 |
| `!load_cog <名稱>` | 載入指定的 Cog 模組 |
| `!unload_cog <名稱>` | 卸載指定的 Cog 模組 |
| `!reload_cog <名稱>` | 重新載入指定的 Cog 模組 |

---

## 專案結構

```
CFSF_bot/
├── main.py                      # 程式進入點
├── logging_config.py            # 日誌設定
├── pyproject.toml               # 專案中介資料與依賴套件設定
├── .env                         # Discord Token（請勿提交至 GitHub）
│
├── config/
│   ├── config.py                # 設定檔載入器
│   ├── general.toml             # 機器人名稱與指令前綴設定
│   └── translator.toml          # 翻譯器設定
│
└── Bot/
    ├── bot.py                   # 機器人主類別與 Cog 載入器
    ├── cogs/
    │   └── Utility/             # 工具類功能模組
    │       ├── translator.py    # 翻譯指令
    │       └── bot_manage.py    # 僅限擁有者的管理指令
    └── src/
        ├── checker/
        │   └── permission.py    # 權限檢查輔助程式
        └── util/
            └── cog.py           # Cog 自動偵測公用程式
```

---

## 機器人必要權限

| 權限項目 | 權限用途 |
|---|---|
| `Send Messages`（傳送訊息） | 傳送回應訊息 |
| `Manage Messages`（管理訊息） | 在翻譯完成後刪除原始訊息 |
| `Manage Webhooks`（管理 Webhook） | 透過 Webhook 發送翻譯後的訊息 |
| `Read Message History`（讀取訊息歷史紀錄） | 取得回覆時的上下文資訊 |

請在 [Discord Developer Portal](https://discord.com/developers/applications) 的 **Bot → Privileged Gateway Intents** 頁面中，啟用所有的**特權網關意圖（Privileged Gateway Intents）**。

---

## 開發工具與套件

- [discord.py](https://github.com/Rapptz/discord.py) `>=2.3.2`
- [deep-translator](https://github.com/nidhaloff/deep-translator) `>=1.11.4`
- [python-box](https://github.com/cdgriffith/Box) `>=7.4.1`
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 授權條款

本專案採用 [MIT 授權條款](LICENSE)。