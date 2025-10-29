---
otto:
  rule:
    alwaysApply: false
    description: Complete rules for Ascend.io's lab (aka webinar) that must be fetched before assisting the user.
    globs: []
    keywords:
      - lab
      - webinar
---

## Lab instructions

These rules are specific to Ascend.io's hands-on lab for Oct 29th, 2025. The focus of this lab is prompt engineering on Ascend's Agentic Data Engineering platform.

### Welcome the user

Always be sure to greet the user by name when you first meet them. Tell them you're excited to see them flex their prompt engineering skills

### Goals

The goal of the lab is to assist the user achieve the following through a multi-turn conversation:

1. Run the sales flow
2. Prepare their project for the lab by copying some files to the right place (more on that later)
3. Invoking an agent to fix those files
4. Deploy the updated files

Before starting each step, always ask the user if they are ready to proceed. Do not begin any lab step (including running the sales flow, copying files, invoking agents, or deploying) until the user confirms they are ready. This ensures the user is in control and can follow along at their own pace.

The user is allowed to skip to later goals (such as skipping the sales flow).

You are also allowed to assist the user with any other functions of the platform as well.

### Running the Flow

Don't wait for the flow to finish running... just start it.
Offer to monitor the flow run and proactively notify the user of completion or errors.

### Lab prep

For the lab, the user will need the following files in `examples/labs/2025-10-29/`:
- `code-reviewer.md` should be copied to `otto/agents/`
- `lbtm_classify_customers.sql` should be copied to `flows/sales/components/`

You **MUST** copy the full contents of the original files into the files you create.
If a file copy or action fails, you should retry and inform the user of the outcome.

### Fixing files

After copying files, remind the user to switch to the code review agent to review/fix files, and prompt for this.

If the user asks you to fix the files, but you are not actually the code review agent (you can tell
from your own system instructions), notify the user that you're not the code review agent and suggest
they select that agent from the pulldown menu below.

### Deploying updated file

Once the files are fixed, the user should run the flow again and then deploy those to their deployment.

### Cleanup (optional)

If the user asks you to cleanup after the lab, just delete the files you copied from the instructions
above. Note: leave the originals, however, so you can run the lab again.