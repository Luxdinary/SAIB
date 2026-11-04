---
topic_id: ai_security-20261105-2
brand_id: ai_security
language: en
title: What an AI chat keeps from your business
description: Whether your inputs are used for training depends on one setting and on the contract. One rule for small businesses.
hashtags: [aisecurity, smallbusiness, dataprotection, chatgpt, claude]
risk_level: medium
sources:
  - id: S1
    url: https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training
    title: Is my data used for model training? (Anthropic Privacy Center)
    checked_at: 2026-10-30
  - id: S2
    url: https://privacy.claude.com/en/articles/7996875-can-you-delete-data-that-i-sent-via-api
    title: Can you delete data that I sent via API? (Anthropic Privacy Center)
    checked_at: 2026-10-30
  - id: S3
    url: https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/KI/Generative_KI-Modelle.html
    title: Generative KI-Modelle - Chancen und Risiken für Industrie und Behörden (BSI, 21 Jan 2025)
    checked_at: 2026-10-30
---
## Scene 1 (hook)
Your employee pastes the customer list into an AI chat. Where does it go?
> visual: headline="Where does the customer list go?" kind="hook"

## Scene 2 (card)
At Anthropic, for personal accounts: your chats are used to improve the models if you allow it in your privacy settings, if a conversation is flagged for safety review, or if you explicitly opt in. [S1]
> visual: headline="Personal accounts: one setting decides" body="Training only with your permission, a safety flag or an explicit opt-in" kind="card"

## Scene 3 (fact)
The business interface is different. Anthropic states it does not use API data for training unless an agreement says otherwise. But paid API customers get no ad hoc deletion either. [S2]
> visual: headline="Business access: no training, no deletion on request" number="API" body="Read the contract and the retention terms first" kind="fact"

## Scene 4 (card)
Germany's federal security office, the BSI, published a paper on generative AI models in January 2025 that lays out risks for industry and public bodies and names countermeasures. Required reading before you roll out AI in a company. [S3]
> visual: headline="BSI: risks and countermeasures" body="Generative AI models, published 21 January 2025" kind="card"

## Scene 5 (advice)
The rule for small businesses: no customer data, no contracts, no passwords in chats on personal accounts. For company data use a business plan with a contract, and check the training setting on every account.
> visual: headline="One rule, three points" body="No customer data in personal accounts · business plan with contract · check the setting" kind="advice"

## Scene 6 (payoff)
Today: open the privacy settings of your AI account and look at what is ticked. More protection for small businesses: follow. [S1]
> visual: headline="Today: check your settings" kind="payoff"
