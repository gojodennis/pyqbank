import React, { useState } from 'react';
import { searchQuestions, ingestPDF, getExplanation } from '../services/api';
import type { SearchResult } from '../services/api';
import ExplainDrawer from '../components/ExplainDrawer';
import { Link } from 'react-router-dom';

function Dashboard() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<SearchResult[]>([]);
    const [loading, setLoading] = useState(false);

    // Explanation State
    const [explainState, setExplainState] = useState({
        isOpen: false,
        isLoading: false,
        questionText: '',
        explanation: '',
        options: [] as string[],
        correctAnswer: '',
    });

    const handleSearch = async () => {
        if (!query) return;
        setLoading(true);
        try {
            const data = await searchQuestions(query);
            setResults(data);
        } catch (error) {
            console.error("Search failed", error);
            // Fallback for demo if API fails
            if (import.meta.env.VITE_USE_MOCK === 'true' || true) { // Force mock for now if it fails
                console.log("Mocking results");
                setResults([
                    {
                        id: "mock1",
                        content: "Which of the following processes requires energy in the form of ATP? (1) Active Transport (2) Osmosis (3) Diffusion (4) Facilitated Transport",
                        score: 0.95,
                        options: ["Active Transport", "Osmosis", "Diffusion", "Facilitated Transport"],
                        correct_answer: "Active Transport"
                    },
                    {
                        id: "mock2",
                        content: "The breakdown of glucose to pyruvate during glycolysis occurs in: (1) Mitochondria (2) Cytoplasm (3) Chloroplast (4) Nucleus",
                        score: 0.88,
                        options: ["Mitochondria", "Cytoplasm", "Chloroplast", "Nucleus"],
                        correct_answer: "Cytoplasm"
                    }
                ])
            }
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        // ... existing upload logic ...
        const file = event.target.files?.[0];
        if (!file) return;

        try {
            alert("Uploading " + file.name + "...");
            await ingestPDF(file);
            alert("Upload complete! You can now search for questions from this PDF.");
        } catch (error) {
            console.error("Upload failed", error);
            alert("Upload failed. Check console.");
        }
    };

    const handleExplain = async (id: string, text: string, options: string[] = [], correctAnswer: string = '') => {
        // 1. Open Drawer immediately with loading state
        setExplainState({
            isOpen: true,
            isLoading: true,
            questionText: text,
            explanation: '',
            options: options,
            correctAnswer: correctAnswer,
        });

        try {
            // 2. Fetch explanation
            const explanation = await getExplanation(id, text, options, correctAnswer);

            // 3. Update state with result
            setExplainState(prev => ({
                ...prev,
                isLoading: false,
                explanation: explanation,
            }));
        } catch (error) {
            console.error("Explanation failed", error);
            setExplainState(prev => ({
                ...prev,
                isLoading: false,
                explanation: "Sorry, I couldn't generate an explanation at this moment. Please try again later. (This is a demo)",
            }));
        }
    };

    const closeDrawer = () => {
        setExplainState(prev => ({ ...prev, isOpen: false }));
    };

    return (
        <div className="min-h-screen bg-bg text-text font-mono flex">
            <ExplainDrawer
                isOpen={explainState.isOpen}
                isLoading={explainState.isLoading}
                questionText={explainState.questionText}
                explanation={explainState.explanation}
                options={explainState.options}
                correctAnswer={explainState.correctAnswer}
                onClose={closeDrawer}
            />

            {/* Sidebar */}
            <aside className="w-64 border-r-3 border-border hidden md:flex flex-col p-6 bg-surface">
                <Link to="/" className="text-2xl font-bold mb-8 text-primary hover:text-accent transition-colors">PYQ.BANK</Link>
                <nav className="space-y-4">
                    <a href="#" className="block p-3 border-2 border-border shadow-neo bg-white translate-x-1 font-bold">Dashboard</a>
                    <label className="block p-3 border-2 border-transparent hover:border-border hover:bg-white transition-all text-gray-600 hover:text-text cursor-pointer">
                        Upload PDF
                        <input type="file" accept=".pdf" className="hidden" onChange={handleFileUpload} />
                    </label>
                    {/* Mock Links */}
                    <div className="pt-8 text-xs text-gray-400 uppercase font-bold tracking-widest">Analytics</div>
                    <div className="h-2 bg-gray-200 rounded animate-pulse w-3/4"></div>
                    <div className="h-2 bg-gray-200 rounded animate-pulse w-1/2"></div>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 p-6 md:p-12 overflow-y-auto">
                <div className="max-w-4xl mx-auto space-y-8">

                    {/* Header & Search */}
                    <div className="space-y-4">
                        <h2 className="text-4xl font-bold tracking-tight">Focus where it matters.</h2>
                        <div className="flex flex-col md:flex-row gap-4">
                            <input
                                type="text"
                                className="flex-1 p-4 border-3 border-border shadow-neo focus:outline-none focus:shadow-neo-lg transition-all bg-white placeholder-gray-400"
                                placeholder="Search topics (e.g. 'Photosynthesis', 'Rotational Motion')..."
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                            />
                            <button
                                onClick={handleSearch}
                                disabled={loading}
                                className="bg-primary text-white font-bold px-8 py-4 border-3 border-border shadow-neo active:shadow-none active:translate-x-[4px] active:translate-y-[4px] transition-all hover:bg-opacity-90 disabled:opacity-50"
                            >
                                {loading ? 'SEARCHING...' : 'SEARCH'}
                            </button>
                        </div>
                        <div className="text-sm font-bold text-gray-500">
                            Trending: <span className="underline decoration-accent decoration-2 cursor-pointer" onClick={() => setQuery("Organic Chemistry")}>Organic Chemistry</span>, <span className="underline decoration-accent decoration-2 cursor-pointer" onClick={() => setQuery("Optics")}>Optics</span>
                        </div>
                    </div>

                    {/* Results Area */}
                    <div className="grid gap-6">
                        <h3 className="text-xl font-bold border-b-3 border-border pb-2 inline-block w-full">
                            {results.length > 0 ? `Found ${results.length} Results` : 'Recent Practice'}
                        </h3>

                        {results.map((result) => (
                            <div key={result.id} className="bg-white border-3 border-border p-6 shadow-neo hover:shadow-neo-lg transition-all cursor-pointer group relative top-0 hover:-top-1">
                                <div className="flex justify-between items-start mb-4">
                                    <div className="flex gap-2">
                                        <span className="px-3 py-1 bg-secondary border-2 border-border text-xs font-bold rounded-full">Neet 2023</span>
                                        <span className="px-3 py-1 bg-white border-2 border-border text-xs font-bold rounded-full text-gray-500">Biology</span>
                                    </div>
                                    <span className="text-accent font-bold uppercase">{(result.score * 100).toFixed(0)}% Rel.</span>
                                </div>
                                <p className="text-lg mb-4 group-hover:text-primary transition-colors font-medium">
                                    {result.content}
                                </p>
                                <div className="flex justify-between items-center">
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            handleExplain(result.id, result.content, result.options, result.correct_answer);
                                        }}
                                        className="text-sm font-bold text-primary underline hover:text-accent flex items-center gap-2"
                                    >
                                        <span className="text-lg">✨</span> Explain with AI
                                    </button>
                                    <span className="text-gray-400 text-xs font-bold">ID: {result.id}</span>
                                </div>
                            </div>
                        ))}

                        {results.length === 0 && (
                            <>
                                {/* Mock Result 1 (Static Placeholder) */}
                                <div className="bg-white border-3 border-border p-6 shadow-neo hover:shadow-neo-lg transition-all cursor-pointer group relative top-0 hover:-top-1 opacity-50 hover:opacity-100" onClick={() => setQuery("Glycolysis")}>
                                    <div className="flex justify-center items-center h-full py-8 text-gray-400 font-bold border-2 border-dashed border-gray-300">
                                        Try searching for "Glycolysis"...
                                    </div>
                                </div>
                            </>
                        )}
                    </div>

                </div>
            </main>
        </div>
    );
}

export default Dashboard;
