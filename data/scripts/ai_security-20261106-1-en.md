---
topic_id: ai_security-20261106-1
brand_id: ai_security
language: en
title: AI labelling – what applies in the EU since August 2026
description: The transparency rules of the AI Act are in force. What small businesses must do about AI content and chatbots.
hashtags: [aiact, ailabelling, smallbusiness, compliance, eu]
risk_level: medium
sources:
  - id: S1
    url: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
    title: AI Act - Shaping Europe's digital future (European Commission)
    checked_at: 2026-10-30
  - id: S2
    url: https://docs.upload-post.com/api/upload-video
    title: Upload-Post API - Upload video (parameters is_aigc, is_ai_generated, containsSyntheticMedia)
    checked_at: 2026-10-30
---
## Scene 1 (hook)
This video is AI-generated. And it has to tell you so. [S1]
> visual: headline="This video has to out itself" kind="hook"

## Scene 2 (card)
According to the European Commission, the EU AI Act became applicable on the second of August 2026, and its transparency rules with it. They do not only affect large companies but everyone who uses AI content professionally. [S1]
> visual: headline="Applicable since 2 August 2026" body="Transparency rules of the AI Act, European Commission" kind="card"

## Scene 3 (card)
Rule one: humans must be made aware that they are interacting with a machine. So a chatbot on your website has to identify itself. [S1]
> visual: headline="Chatbots must identify themselves" body="People must know they are talking to a machine" kind="card"

## Scene 4 (card)
Rule two: providers of generative AI must make their output identifiable. Certain content must be labelled, including deep fakes and text published to inform the public on matters of public interest. [S1]
> visual: headline="Label deep fakes and public-interest text" body="Identifiable output, labels for deep fakes and public-interest text" kind="card"

## Scene 5 (fact)
The platforms have switches for this. Through the Upload-Post API they are called is_aigc for TikTok, is_ai_generated for Instagram and containsSyntheticMedia for YouTube. If you post automatically, you set them on every video. [S2]
> visual: headline="Three switches, three platforms" number="3" body="is_aigc · is_ai_generated · containsSyntheticMedia" kind="fact"

## Scene 6 (payoff)
For a small business this means: label the chatbot, label AI images and videos, and write the rule down. More protection for small businesses: follow.
> visual: headline="Label it and write it down" kind="payoff"
