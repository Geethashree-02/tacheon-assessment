# Task 1: Product Brief - Marketing Performance Tool

## Problem Statement
The marketing team currently answers "How is our marketing performing?" 
by manually checking multiple tools, pulling numbers, and stitching 
together a response. This is slow, inconsistent, and dependent on 
one person.

## Primary User
Internal marketing analysts at the agency.
(Not the client in v1 - keeping scope small and focused)

## What the Tool Does (v1)
A simple internal dashboard that:
- Shows key metrics from all marketing channels in one place
- Updates automatically (no manual data pulling)
- Gives a clear answer to: "What is performing well and what is not?"

## Data Sources
- Google Ads (paid search performance)
- Meta Ads (paid social performance)  
- Google Analytics (website traffic)
The tool connects to these via their existing APIs.

## What a Successful Interaction Looks Like
An analyst opens the tool, selects a client brand, and within 
30 seconds sees:
- Top performing channel this week
- Which channel needs attention
- Simple recommendation on where to focus next

## What We Are NOT Building in v1
- Client-facing view (too much risk, needs polish)
- Automated recommendations using AI (too complex for v1)
- Integration with every possible tool (scope creep)
- Custom date range filters (default to last 7 days for now)

## Why This Scope
A focused tool that works reliably is more valuable than an 
ambitious tool that breaks. Once analysts trust it, we expand it.

## What I Would Revisit With More Time
- Add client-facing view in v2
- Add AI-generated summary of performance
- Add alerts when a channel underperforms