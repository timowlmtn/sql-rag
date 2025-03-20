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
