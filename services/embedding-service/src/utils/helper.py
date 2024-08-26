

def format_results(results):
    formatted_results = []
    for doc, metadata, distance in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        formatted_result = {
            "content": doc,
            "source": f"{metadata['original_file_name']}, Page {metadata['page_number']}",
            "similarity": 1 - distance
        }
        formatted_results.append(formatted_result)
    return formatted_results


def combine_content(formatted_results):
    return "\n".join([f"Content: {r['content']}\nSource: {r['source']}" for r in formatted_results])


def create_summary_prompt(query, combined_content):
    return f"Based on the following information, answer the question: '{query}'\n\nPlease include the source (PDF name and page number) for each piece of information in your answer.\n\Information:\n{combined_content}"