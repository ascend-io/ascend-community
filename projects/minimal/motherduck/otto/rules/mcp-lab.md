---
otto:
  rule:
    alwaysApply: false
    description: "Slack MCP setup guide - opens relevant configuration files"
    globs: []
    keywords: [MCP lab, slack mcp]
---

# Slack MCP Lab - Step-by-Step Setup Guide

When the user mentions "MCP lab" or asks about Slack MCP setup, guide them through the complete setup process with these detailed steps. Note that there is a section specifically for listing what files will be opened and then have a separate section under which each step is summarized.

## Required Files to Open

Automatically open these files when helping with MCP lab:

1. **`otto/mcp.yaml`** - Slack MCP server configuration
2. **`otto/otto.yaml`** - Otto agent configuration
3. **`automations/otto-slack-success.yaml`** - Success notification automation
4. **`automations/otto-slack-failure.yaml`** - Failure notification automation

### Step 1: Create a Slack Workspace
**Link:** https://slack.com/create
**What's Happening:** Creating a new Slack workspace where Otto will send notifications.
**Key Actions:**
- Click "Get Started" on "Create a New Workspace"
- Workspace Name: **Ascend-[YourName]** (e.g., Ascend-Ayush)
- Your Name: **[YourName]**
- Skip inviting team members
- Choose "Start with the Limited Free Version"

---

### Step 2: Create a Slack App
**Link:** https://api.slack.com/apps
**What's Happening:** Creating a bot application that Otto will use to post messages.
**Key Actions:**
- Click "Create New App"
- Select "From scratch"
- App name: **otto-automation**
- Workspace: Select your **Ascend** workspace
- Click "Create App"

---

### Step 3: Configure Bot Permissions
**What's Happening:** Granting your bot the permissions it needs to read channels and send messages.
**Key Actions:**
- Navigate to "OAuth & Permissions" in left sidebar
- Scroll down to "Scopes" section
- Under "Bot Token Scopes", click "Add an OAuth Scope"
- Add these two scopes:
  - `chat:write` - Send messages as the bot
  - `channels:read` - View basic information about public channels
- Navigate to top of page (in OAuth & Permissions)
- Click "Install to Ascend" button under "OAuth Tokens" (may be greyed out initially)
- Click the green "Allow" or "Install otto-automation" button

**Important:** These are minimum required scopes; you can add more later if needed.

---

### Step 4: Obtain Slack App Bot Token
**What's Happening:** Saving the bot's OAuth token that will be used in Step 6 to authenticate Otto with Slack.
**Key Actions:**
- After installing the app, find the "Bot User OAuth Token" field (replaces install button)
- **CRITICAL:** Copy the "Bot User OAuth Token" value and save it somewhere
  - This value starts with `xoxb-`
  - You'll need this in Step 6

---

### Step 5: Get Your Workspace and Channel IDs
**Reference Link:** https://slack.com/help/articles/221769328-Locate-your-Slack-URL-or-ID
**What's Happening:** Finding the unique identifiers for your workspace and the channel where Otto will post.
**Key Actions:**
1. Open your Slack workspace in a browser
2. Navigate to the channel where you want Otto to post (e.g., #general)
3. Add the bot to the channel using the command: `/invite @otto-automation`
   - If Otto doesn't appear, verify you completed Step 3 correctly
4. Look at the browser URL (example): `https://app.slack.com/client/T01ABC123DEF/C01XYZ456GHI`
5. **Workspace ID:** Part after `/client/` (starts with `T`, e.g., `T01ABC123DEF`)
6. **Channel ID:** Last part of URL (starts with `C`, e.g., `C01XYZ456GHI`)

---

### Step 6: Store Credentials in Ascend
**What's Happening:** Securely storing your Slack credentials in Ascend's Environment Vault so Otto can access them.
**Key Actions:**
1. In Ascend, click your profile in top right → "Settings"
2. Select "Secrets & Vaults"
3. Under "Environments" section, click "Default"
4. Add these 3 secrets (create a separate secret for each):
   - `SLACK_APP_TOKEN`: Your Bot OAuth Token from Step 4 (starts with `xoxb-`)
   - `SLACK_TEAM_ID`: Your Workspace ID from Step 5 (starts with `T`)
   - `SLACK_CHANNEL_ID`: Your Channel ID from Step 5 (starts with `C`)

---

### Step 7: Configure the Slack MCP Server
**What's Happening:** Creating the bridge between Otto and Slack by configuring the MCP (Model Context Protocol) server in `otto/mcp.yaml`.
**Key Actions:**
1. Navigate to Ascend homepage → Click your Workspace
2. Open the file tree → Navigate to `otto` directory
3. Open the `mcp.yaml` file
4. Ensure the file contains at least this configuration:

```yaml
mcpServers:
  slack:
    command: npx
    args:
      - --cache
      - /tmp/npm-cache
      - -y
      - "@zencoderai/slack-mcp-server"
    env:
      SLACK_BOT_TOKEN: ${vaults.environment.SLACK_APP_TOKEN}
      SLACK_TEAM_ID: ${vaults.environment.SLACK_TEAM_ID}
      SLACK_CHANNEL_IDS: ${vaults.environment.SLACK_CHANNEL_ID}
```
**Note:** The MCP server runs automatically when Otto needs to interact with Slack.

---

### Step 8: Configure Otto Agents
**What's Happening:** Granting your Otto agents access to the Slack MCP server in `otto/otto.yaml`.
**Key Actions:**
1. In the same `otto` directory, open the `otto.yaml` file
2. Copy/paste the following code into the file:

```yaml
otto:
  agents:
    "chat":
      mcp_servers:
        - slack
```
**Note:** You can add the `slack` MCP server to any existing agents or create new agents.

---

### Step 9: Explore the Slack Notification Automations
**What's Happening:** Understanding the pre-configured automations that monitor Flow events and send intelligent Slack notifications.

**Files to Review:**
- `automations/otto-slack-success.yaml` - Monitors FlowRunSuccess events
- `automations/otto-slack-failure.yaml` - Monitors FlowRunError events

**Automation Components:**
- **Type:** `run_otto` - Leverages Otto's AI capabilities
- **Agent:** "Slack Summary Notification" - Configured with Slack MCP access
- **Triggers:** Monitors both success and failure events
- **Prompt:** Instructs Otto on how to investigate and craft messages

---

### Step 10: Deploy and Test
**What's Happening:** Deploying your Workspace changes to Production and testing the automation by running a Flow.

**Deploy Changes:**
1. In your Workspace, click the Source Control tab (Git branch icon in top right of left sidebar)
2. Click "Open Git log & actions"
3. Click "Merge to Deployment" → Select "Production" from dropdown
   - This pushes your changes from Workspace to Production Deployment

**Test the Automation:**
1. Navigate to Ascend homepage → Click "Production" Deployment
2. On the left side, click the "sales" flow
3. In top right, click "Run Flow" → Click "Run" in the pop-up
4. Wait for Flow completion and a bit more time for the Automation to run
5. Check Slack for the new notification message!

---
