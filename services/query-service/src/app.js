import express from 'express'
import axios from 'axios'
import { ChromaClient } from "chromadb";

const app = express();
app.use(express.json());


const chromaClient = new ChromaClient({
    path: `http://${process.env.CHROMA_HOST}:${process.env.CHROMA_PORT}`
})


async function getEmbedding(text) {
    try {
        const url = `http://${process.env.EMBEDDING_SERVICE_HOST}:${process.env.EMBEDDING_SERVICE_PORT}/embedding`
        const response = await  axios.post(url, { text });
        console.log('embedding response:', response.data);
        return response.data.embedding;
    } catch (error) {
        console.error('Error getting embedding:', error);
        throw error;
    }
}

async function retrieveDocuments(query, topK) {
    try {
        const embedding = await getEmbedding(query);
        const collection = await chromaClient.getCollection({
            name: process.env.COLLECTION_NAME
        });
        return collection.query({
            queryEmbeddings: [embedding],
            nResults: topK
        });
    } catch (error) {
        console.error('Error retrieving documents:', error);
        throw error;
    }
}

function formatResults(results) {
    return results.documents[0].map((doc, index) => ({
      content: doc,
      source: `${results.metadatas[0][index].original_file_name}, Page ${results.metadatas[0][index].page_number}`,
      similarity: 1 - results.distances[0][index]
    }));
}

function combineContent(formattedResults) {
    return formattedResults.map(r => `Content: ${r.content}\nSource: ${r.source}`).join('\n');
}
  
function createSummaryPrompt(query, combinedContent) {
    return `Based on the following information, answer the question: '${query}'\n\nPlease include the source (PDF name and page number) for each piece of information in your answer.\n\nInformation:\n${combinedContent}`;
}


async function getChatCompletion(messages) {
    try {
      const response = await axios.post('https://api.openai.com/v1/chat/completions', {
        model: 'gpt-3.5-turbo',
        messages: messages
      }, {
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      });
      console.log('chat completion response:', response.data);
      return response.data.choices[0].message.content;
    } catch (error) {
      console.error('Error getting chat completion:', error);
      throw error;
    }
  }



app.post('/query', async (req, res) => {
    try {
        const { query } = req.body;

        const results = await retrieveDocuments(query, 2);
        
        if (!results || !results.documents || results.documents.length === 0) {
            throw new Error('Failed to retrieve documents');
        }

        const formattedResults = formatResults(results);
        const combinedContent = combineContent(formattedResults);

        const summaryPrompt = createSummaryPrompt(query, combinedContent);

        const finalResponse = await getChatCompletion([
            { role: 'system', content: 'You are a helpful assistant that summarizes information. Always include the source of information in your answers.' },
            { role: 'user', content: summaryPrompt }
        ]);

        console.log('final response:', finalResponse);
        res.json({
            query: query,
            response: finalResponse,
            sources: formattedResults.map(r => r.source)
        });
    }  catch (error) {
        console.error(`Error processing query: ${error.message}`);
        res.status(500).json({ error: 'Failed to process query' });
    }
});

const port = process.env.QUERY_SERVICE_PORT || 3000;
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });