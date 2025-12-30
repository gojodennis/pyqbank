import React from 'react';
import ReactMarkdown from 'react-markdown';


interface ExplainDrawerProps {
    isOpen: boolean;
    isLoading: boolean;
    onClose: () => void;
    questionText: string;
    explanation: string;
    options?: string[];
    correctAnswer?: string;
}

const ExplainDrawer: React.FC<ExplainDrawerProps> = ({
    isOpen,
    isLoading,
    onClose,
    questionText,
    explanation,
    options = [],
    correctAnswer = '',
}) => {
    return (
        <>
            {/* Backdrop */}
            <div
                className={`fixed inset-0 bg-black/20 backdrop-blur-sm z-40 transition-opacity duration-300 ${isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
                    }`}
                onClick={onClose}
            />

            {/* Drawer */}
            <div
                className={`fixed top-0 right-0 h-full w-full md:w-[600px] bg-bg border-l-4 border-border shadow-2xl z-50 transform transition-transform duration-300 ease-in-out flex flex-col ${isOpen ? 'translate-x-0' : 'translate-x-full'
                    }`}
            >
                {/* Header */}
                <div className="p-6 border-b-4 border-border bg-white flex justify-between items-center sticky top-0 z-10 shrink-0">
                    <div className="flex items-center gap-3">
                        <div className="w-4 h-4 bg-accent animate-pulse" />
                        <h2 className="text-xl font-bold uppercase tracking-wider text-primary">
                            AI Breakdown
                        </h2>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-100 border-2 border-transparent hover:border-border transition-all"
                        aria-label="Close"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2.5"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                </div>

                {/* Scrollable Content */}
                <div className="flex-1 overflow-y-auto p-8 custom-scrollbar">
                    {/* Question Context */}
                    <div className="mb-8 p-6 bg-white border-2 border-border shadow-neo">
                        <h3 className="text-sm font-bold text-gray-500 mb-2 uppercase">Question</h3>
                        <p className="text-lg font-medium leading-relaxed mb-4">{questionText}</p>

                        {options.length > 0 && (
                            <div className="space-y-2">
                                {options.map((opt, idx) => {
                                    // Determine styling based on correct answer (if known)
                                    // Often options are strings like "Option Text". 
                                    // If correctAnswer is like "B" or "2", we might not be able to match simply.
                                    // But typically OCR returns full text. 
                                    // For now, simple list. Highlight if exact match or if contains text.
                                    const isCorrect = correctAnswer && (opt.includes(correctAnswer) || correctAnswer.includes(opt));

                                    return (
                                        <div
                                            key={idx}
                                            className={`p-3 border-2 rounded ${isCorrect
                                                ? 'bg-green-50 border-green-500 text-green-800'
                                                : 'bg-gray-50 border-gray-200'
                                                }`}
                                        >
                                            <span className="font-bold mr-2">{String.fromCharCode(65 + idx)}.</span> {opt}
                                            {isCorrect && <span className="ml-2 text-xs font-bold bg-green-200 text-green-800 px-2 py-0.5 rounded-full">CORRECT ANSWER</span>}
                                        </div>
                                    );
                                })}
                            </div>
                        )}

                        {correctAnswer && !options.length && (
                            <div className="mt-4 p-3 bg-green-50 border-2 border-green-500 rounded text-green-800 font-bold">
                                Correct Answer: {correctAnswer}
                            </div>
                        )}
                    </div>

                    {/* AI Response Area */}
                    <div className="relative min-h-[200px]">
                        {isLoading ? (
                            <div className="flex flex-col items-center justify-center p-12 space-y-6 animate-fade-in">
                                {/* Neo-brutalist Loader */}
                                <div className="relative">
                                    <div className="w-16 h-16 border-4 border-border bg-white animate-spin absolute top-0 left-0" />
                                    <div className="w-16 h-16 border-4 border-primary bg-secondary animate-bounce absolute top-2 left-2 mix-blend-multiply" />
                                </div>
                                <div className="text-center space-y-2">
                                    <p className="text-xl font-bold text-primary animate-pulse">
                                        ANALYZING...
                                    </p>
                                    <p className="text-sm text-gray-500 font-medium">
                                        Pulling concepts from NCERT...
                                    </p>
                                </div>
                            </div>
                        ) : explanation.startsWith('Error') || explanation.includes('429') ? (
                            <div className="animate-slide-up p-6 bg-red-50 border-2 border-red-500 rounded text-red-800 shadow-sm">
                                <div className="flex items-center gap-3 mb-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                    </svg>
                                    <h3 className="font-bold text-lg uppercase tracking-wide">Service Unavailable</h3>
                                </div>
                                <p className="mb-4 font-mono text-sm leading-relaxed border-l-2 border-red-300 pl-3">
                                    {explanation}
                                </p>
                                <div className="text-xs font-bold uppercase bg-red-100 text-red-900 px-3 py-2 rounded inline-block">
                                    Please try again in a few moments or check your API plan.
                                </div>
                            </div>
                        ) : (
                            <div className="animate-slide-up">
                                <h3 className="text-sm font-bold text-accent mb-4 uppercase border-b-2 border-accent inline-block pb-1">
                                    Explanation
                                </h3>
                                <div className="prose prose-base font-mono prose-headings:font-bold prose-p:text-text prose-strong:text-primary max-w-none">
                                    <ReactMarkdown
                                        components={{
                                            h1: ({ node, ...props }) => <h1 className="text-2xl font-bold mt-6 mb-4" {...props} />,
                                            h2: ({ node, ...props }) => <h2 className="text-xl font-bold mt-5 mb-3" {...props} />,
                                            h3: ({ node, ...props }) => <h3 className="text-lg font-bold mt-4 mb-2" {...props} />,
                                            ul: ({ node, ...props }) => <ul className="list-disc pl-5 space-y-2 mb-4" {...props} />,
                                            ol: ({ node, ...props }) => <ol className="list-decimal pl-5 space-y-2 mb-4" {...props} />,
                                            li: ({ node, ...props }) => <li className="pl-1" {...props} />,
                                            p: ({ node, ...props }) => <p className="mb-4 leading-relaxed" {...props} />,
                                            strong: ({ node, ...props }) => <strong className="font-bold text-primary bg-yellow-100 px-1" {...props} />,
                                        }}
                                    >
                                        {explanation}
                                    </ReactMarkdown>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Footer */}
                <div className="p-4 border-t-4 border-border bg-gray-50 text-center text-xs text-gray-400 font-bold uppercase">
                    Powered by Gemini 2.5 Flash Lite
                </div>
            </div>
        </>
    );
};

export default ExplainDrawer;
