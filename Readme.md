# A Musical Introduction to RAG

*Author: Tim Burns*

[Original Article](https://www.owlmountain.net/post/a-musical-introduction-to-rag)
**

## Retrieval Augmented Generation with SQL

Large Language Model (LLM) systems like ChatGPT initially seem impressive. However, upon further interaction, certain limitations become evident:

1. **Outdated Information**: They aren't up to date.
2. **Confident Inaccuracies**: They make confident assertions about things that aren't true.

**Retrieval Augmented Generation (RAG)** aims to address these limitations by leveraging the LLM's language processing capabilities in conjunction with external data sources.

RAG enhances LLMs by:

- **Incorporating Domain-Specific Knowledge**: Crafting prompts that guide the LLM to avoid confidently false assertions.
- **Accessing Current Data**: Querying up-to-date information and utilizing the LLM to interpret it.

*The diagram below illustrates the RAG architecture, with LLM components in blue circles and the RAG client in yellow.*

![RAG Architecture Diagram](https://static.wixstatic.com/media/4ae1bd_0281ef63cbbf48a1bdf2a9ae217ac462~mv2.png)

## Evaluating the RAG Client's Performance in Answering Business Questions

The LLM (specifically, [Anthropic's Claude](https://console.anthropic.com)) demonstrates proficiency in generating queries and answering questions.

For example, when asked:

> "What are Bob Mould's top hits this past year?"

The generated SQL query was:

```sql
SELECT song, COUNT(*) as play_count
FROM import_kexp_playlist
WHERE artist = 'Bob Mould'
AND airdate >= NOW() - INTERVAL '1 year'
GROUP BY song
ORDER BY play_count DESC;
```


The LLM summarized the answer with, "Based on the results, we can see Bob Mould's most played songs in the past year, with "Here We Go Crazy" being the most popular with 22 plays, followed by "Neanderthal" and "See a Little Light" with 6 plays each.


## Links to the Code for Example of RAG with SQL

I've linked to the code here: https://github.com/timowlmtn/sql-rag/tree/main


### The Folders

**client** - The client will run the server through a bash call.


**python** agent/client/MCPClient.py agent/bash/run_query_agent.sh
**bash** - Wrapping your server in a bash script will make debugging easier.  It sets your environment variables to connect to your database.


server  - This code will contain the server connection classes to connect to your database and format the data.