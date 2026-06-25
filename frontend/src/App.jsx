import { useState } from 'react';
import { Search, Bot } from 'lucide-react';

export default function App() {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

 const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    // 1. Add user query to chat history
    const newChat = [...chatHistory, { role: 'user', content: query }];
    setChatHistory(newChat);
    setQuery('');
    setIsSearching(true); // Turns on the bouncing loader

    try {
      // 2. Hit your real Python backend
      const response = await fetch("http://localhost:8000/api/agent/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query })
      });
      
      const data = await response.json();

      // 3. Display the real AI response
      setChatHistory([...newChat, {
        role: 'agent',
        agentName: 'Manager Router',
        content: data.reply || "No data was returned."
      }]);

    } catch (error) {
      setChatHistory([...newChat, {
        role: 'agent',
        agentName: 'System Error',
        content: "Failed to connect to the backend server. Is Python running?"
      }]);
    } finally {
      setIsSearching(false); // Turns off the loader
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] text-slate-200 font-sans p-4 md:p-8 flex flex-col items-center relative">
      
      {/* 1. Header Area - Shrinks and moves up if chat exists */}
      <div className={`transition-all duration-700 flex flex-col items-center ${chatHistory.length > 0 ? 'mt-2 mb-8 scale-90' : 'mt-32 mb-12'}`}>
        <div className="flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/20 px-4 py-1.5 rounded-full text-indigo-400 text-xs font-bold tracking-widest mb-6">
          <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
          MULTI-AGENT SYSTEM ONLINE
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight text-center">
          AI Academic Copilot
        </h1>
        {chatHistory.length === 0 && (
          <p className="text-slate-400 text-lg text-center max-w-xl">
            Your intelligent gateway to the University of Stuttgart's academic ecosystem.
          </p>
        )}
      </div>

      {/* 2. Chat Display Area */}
      {chatHistory.length > 0 && (
        <div className="w-full max-w-4xl flex-1 overflow-y-auto mb-40 flex flex-col gap-6 px-2 scrollbar-hide">
          {chatHistory.map((msg, idx) => (
            <div key={idx} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`max-w-[85%] md:max-w-[75%] p-5 rounded-2xl shadow-sm ${msg.role === 'user' ? 'bg-[#4F46E5] text-white rounded-tr-sm' : 'bg-[#151C2C] border border-slate-800 text-slate-200 rounded-tl-sm'}`}>
                {msg.role === 'agent' && (
                  <div className="flex items-center gap-2 text-indigo-400 text-sm font-bold mb-3 uppercase tracking-wider">
                    <Bot size={16} /> {msg.agentName}
                  </div>
                )}
                <p className="whitespace-pre-wrap leading-relaxed text-base">{msg.content}</p>
              </div>
            </div>
          ))}
          
          {/* Simulated Loading State */}
          {isSearching && (
            <div className="flex items-start">
               <div className="bg-[#151C2C] border border-slate-800 p-5 rounded-2xl rounded-tl-sm text-slate-400 flex items-center gap-3 shadow-sm">
                  <span className="flex gap-1">
                    <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </span>
                  <span className="text-sm font-medium">Orchestrating agents...</span>
               </div>
            </div>
          )}
        </div>
      )}

      {/* 3. Search Input Area - Centers if empty, fixes to bottom if chat is active */}
      <div className={`w-full max-w-4xl px-2 transition-all duration-700 z-10 ${chatHistory.length > 0 ? 'fixed bottom-8' : ''}`}>
        <div className={chatHistory.length > 0 ? 'bg-[#0B0F19]/80 backdrop-blur-md pt-4 pb-2 rounded-3xl' : ''}>
          <form onSubmit={handleSearch} className="relative group">
            <div className="absolute inset-y-0 left-5 flex items-center pointer-events-none text-slate-500 group-focus-within:text-indigo-400 transition-colors">
              <Search size={22} />
            </div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Look up exam schedules, library books, or thesis topics..."
              className="w-full bg-[#111827] border border-slate-800 text-white rounded-full py-4 pl-14 pr-32 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 shadow-2xl transition-all text-lg placeholder:text-slate-500"
            />
            <button
              type="submit"
              disabled={isSearching || !query.trim()}
              className="absolute inset-y-2 right-2 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-6 rounded-full font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              Search
            </button>
          </form>

          {/* Sub-Agent Badges */}
          <div className="flex justify-center gap-2 md:gap-4 mt-6 flex-wrap">
            {['Manager Router', 'Admin Specialist', 'Thesis Advisor', 'Library Catalog'].map((agent, i) => (
              <div key={agent} className={`flex items-center gap-2 px-4 py-2 rounded-full text-xs font-semibold tracking-wide border transition-colors cursor-default ${i === 0 ? 'bg-indigo-500/10 border-indigo-500/30 text-indigo-300' : 'bg-slate-800/30 border-slate-700/50 text-slate-400'}`}>
                <span className={`w-1.5 h-1.5 rounded-full ${i === 0 ? 'bg-indigo-400 shadow-[0_0_8px_rgba(129,140,248,0.8)]' : 'bg-slate-500'}`}></span>
                {agent}
              </div>
            ))}
          </div>
        </div>
      </div>

    </div>
  );
}