import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});


export interface SearchResult {
    id: string;
    content: string;
    score: number;
    subject?: string;
    year?: string;
    tags?: string;
    options?: string[];
    correct_answer?: string;
    explanation?: string;
}

export const searchQuestions = async (query: string): Promise<SearchResult[]> => {
    const response = await api.get<SearchResult[]>('/search', {
        params: { q: query },
    });
    return response.data;
};

export const ingestPDF = async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/ingest', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const getExplanation = async (questionId: string, text: string, options: string[] = [], correctAnswer: string = ''): Promise<string> => {
    const response = await api.post('/explain', {
        question_id: questionId,
        question_text: text,
        options: options,
        correct_answer: correctAnswer
    });
    return response.data.explanation;
};

