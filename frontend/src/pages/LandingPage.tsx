import { Link } from 'react-router-dom';

const LandingPage = () => {
    return (
        <div className="min-h-screen bg-bg text-text font-mono selection:bg-accent selection:text-white">
            {/* Navigation */}
            <nav className="border-b-3 border-border bg-white sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
                    <div className="text-2xl font-black tracking-tighter flex items-center gap-2">
                        <div className="w-6 h-6 bg-primary border-2 border-border"></div>
                        PYQ.BANK
                    </div>
                    <div className="flex gap-4">
                        <Link to="/app" className="hidden md:block px-6 py-2 font-bold hover:underline decoration-2">
                            Log In
                        </Link>
                        <Link to="/app" className="px-6 py-2 bg-primary text-white font-bold border-2 border-border shadow-neo hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all">
                            Start Practicing
                        </Link>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <header className="relative overflow-hidden border-b-3 border-border bg-amber-50">
                <div className="max-w-7xl mx-auto px-6 pt-20 pb-32 md:pt-32 md:pb-48 relative z-10">
                    <div className="max-w-3xl">
                        <div className="inline-block px-4 py-1 bg-secondary border-2 border-border text-xs font-bold mb-6 shadow-neo transform -rotate-2">
                            NEET & JEE PREP REINVENTED
                        </div>
                        <h1 className="text-5xl md:text-7xl font-black mb-8 leading-tight">
                            Stop Guessing. <br />
                            <span className="text-primary bg-white px-2 border-3 border-border shadow-neo inline-block rotate-1">Target Weakness.</span>
                        </h1>
                        <p className="text-xl md:text-2xl mb-12 text-gray-700 max-w-2xl leading-relaxed">
                            The only question bank that uses AI to find your gaps and explain concepts instantly. No fluff, just results.
                        </p>
                        <div className="flex flex-col md:flex-row gap-4">
                            <Link to="/app" className="px-8 py-4 bg-accent text-white text-lg font-bold border-3 border-border shadow-neo hover:translate-x-[4px] hover:translate-y-[4px] hover:shadow-none transition-all text-center">
                                Try Demo Now
                            </Link>
                            <a href="#features" className="px-8 py-4 bg-white text-text text-lg font-bold border-3 border-border shadow-neo hover:translate-x-[4px] hover:translate-y-[4px] hover:shadow-none transition-all text-center">
                                How It Works
                            </a>
                        </div>
                    </div>
                </div>

                {/* Decorative Elements */}
                <div className="absolute top-20 right-[-100px] w-96 h-96 bg-secondary border-3 border-border rounded-full opacity-20 hidden md:block"></div>
                <div className="absolute bottom-[-50px] right-[100px] w-64 h-64 bg-primary border-3 border-border transform rotate-12 opacity-20 hidden md:block"></div>
            </header>

            {/* Features Grid */}
            <section id="features" className="py-24 border-b-3 border-border bg-bg">
                <div className="max-w-7xl mx-auto px-6">
                    <h2 className="text-4xl font-black mb-16 text-center">Why Top Rankers Choose Us</h2>
                    <div className="grid md:grid-cols-3 gap-8">
                        {/* Feature 1 */}
                        <div className="bg-white p-8 border-3 border-border shadow-neo hover:shadow-neo-lg transition-all group">
                            <div className="w-16 h-16 bg-primary mb-6 border-2 border-border flex items-center justify-center text-3xl shadow-neo group-hover:translate-x-1 group-hover:translate-y-1 group-hover:shadow-none transition-all">
                                🎯
                            </div>
                            <h3 className="text-2xl font-bold mb-4">Smart Search</h3>
                            <p className="text-gray-700 leading-relaxed">
                                Don't just search keywords. Search by concept. Find every question about "Rotational Motion" from the last 10 years in seconds.
                            </p>
                        </div>
                        {/* Feature 2 */}
                        <div className="bg-white p-8 border-3 border-border shadow-neo hover:shadow-neo-lg transition-all group">
                            <div className="w-16 h-16 bg-secondary mb-6 border-2 border-border flex items-center justify-center text-3xl shadow-neo group-hover:translate-x-1 group-hover:translate-y-1 group-hover:shadow-none transition-all">
                                🤖
                            </div>
                            <h3 className="text-2xl font-bold mb-4">AI Explainer</h3>
                            <p className="text-gray-700 leading-relaxed">
                                Stuck? Get instant, context-aware explanations for any option. It's like having a tutor in your pocket 24/7.
                            </p>
                        </div>
                        {/* Feature 3 */}
                        <div className="bg-white p-8 border-3 border-border shadow-neo hover:shadow-neo-lg transition-all group">
                            <div className="w-16 h-16 bg-accent mb-6 border-2 border-border flex items-center justify-center text-3xl shadow-neo group-hover:translate-x-1 group-hover:translate-y-1 group-hover:shadow-none transition-all">
                                📈
                            </div>
                            <h3 className="text-2xl font-bold mb-4">Gap Analysis</h3>
                            <p className="text-gray-700 leading-relaxed">
                                We track what you get wrong. Our algorithm prioritizes your weak topics so you stop practicing what you already know.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Live Ticker / Social Proof */}
            <section className="border-b-3 border-border bg-primary text-white py-12 overflow-hidden">
                <div className="whitespace-nowrap flex gap-12 animate-marquee font-bold text-2xl">
                    <span>ORGANIC CHEMISTRY</span> • <span>RAY OPTICS</span> • <span>ELECTROSTATICS</span> • <span>GENETICS</span> • <span>THERMODYNAMICS</span> • <span>KINEMATICS</span> • <span>ORGANIC CHEMISTRY</span> • <span>RAY OPTICS</span>
                </div>
            </section>

            {/* Call to Action */}
            <section className="py-32 px-6">
                <div className="max-w-4xl mx-auto text-center">
                    <h2 className="text-4xl md:text-6xl font-black mb-8">Ready to Crashing Your Exam?</h2>
                    <p className="text-xl mb-12 text-gray-800">Join thousands of students saving 30% of their study time.</p>
                    <Link to="/app" className="inline-block px-12 py-5 bg-text text-white text-xl font-bold border-3 border-border shadow-neo hover:scale-105 active:scale-95 transition-all">
                        Launch Dashboard
                    </Link>
                </div>
            </section>

            {/* Footer */}
            <footer className="border-t-3 border-border bg-white py-12">
                <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
                    <div className="text-xl font-bold">PYQ.BANK © 2025</div>
                    <div className="flex gap-8 font-medium">
                        <a href="#" className="hover:text-primary">Twitter</a>
                        <a href="#" className="hover:text-primary">Instagram</a>
                        <a href="#" className="hover:text-primary">Email</a>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
