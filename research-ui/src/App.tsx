import React, { useState } from 'react';
import './App.css';

// Simple icons as SVG components since lucide-react might not be available
const SearchIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="11" cy="11" r="8"/>
    <path d="m21 21-4.35-4.35"/>
  </svg>
);

const FileTextIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14,2 14,8 20,8"/>
    <line x1="16" y1="13" x2="8" y2="13"/>
    <line x1="16" y1="17" x2="8" y2="17"/>
    <polyline points="10,9 9,9 8,9"/>
  </svg>
);

const ClockIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="10"/>
    <polyline points="12,6 12,12 16,14"/>
  </svg>
);

const SparklesIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
    <path d="M5 3v4"/>
    <path d="M19 17v4"/>
    <path d="M3 5h4"/>
    <path d="M17 19h4"/>
  </svg>
);

const GlobeIcon = () => (
  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="10"/>
    <line x1="2" y1="12" x2="22" y2="12"/>
    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
  </svg>
);

const UsersIcon = () => (
  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
    <circle cx="9" cy="7" r="4"/>
    <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
  </svg>
);

const TrendingUpIcon = () => (
  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <polyline points="22,7 13.5,15.5 8.5,10.5 2,17"/>
    <polyline points="16,7 22,7 22,13"/>
  </svg>
);

interface ResearchResult {
  id: string;
  query: string;
  timestamp: string;
  status: 'completed' | 'in-progress' | 'failed';
  summary?: string;
}

const sampleQueries = [
  "Analyze the cultural impact of K-pop on global youth fashion trends",
  "Research sustainable fashion brands among millennials in Europe",
  "Investigate the rise of plant-based food culture in urban areas",
  "Study the cultural significance of gaming communities in social media"
];

function App() {
  const [query, setQuery] = useState('');
  const [isResearching, setIsResearching] = useState(false);
  const [results, setResults] = useState<ResearchResult[]>([]);
  const [currentResult, setCurrentResult] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsResearching(true);
    const newResult: ResearchResult = {
      id: Date.now().toString(),
      query: query.trim(),
      timestamp: new Date().toLocaleString(),
      status: 'in-progress'
    };

    setResults(prev => [newResult, ...prev]);
    setCurrentResult('Starting research...\n\nInitializing Deep Research Agency...\n\n🔄 Triage Agent analyzing query...\n\n🔍 Research Agent gathering insights...\n\nThis is a demo interface. In the full implementation, this would connect to your Python backend to run the actual research agents with Qloo integration.');

    // Simulate research process
    setTimeout(() => {
      setCurrentResult(prev => prev + '\n\n✅ Research complete!\n\nA comprehensive report would be generated here with cultural intelligence insights from Qloo API.');
      setResults(prev => prev.map(r => 
        r.id === newResult.id 
          ? { ...r, status: 'completed', summary: 'Cultural intelligence research completed with Qloo insights' }
          : r
      ));
      setIsResearching(false);
    }, 3000);

    setQuery('');
  };

  const handleSampleQuery = (sampleQuery: string) => {
    setQuery(sampleQuery);
  };

  return (
    <div className="app">
      <div className="main-content">
        <header className="header">
          <div className="header-content">
            <div className="logo">
              <SparklesIcon />
              <h1>Deep Research Agency</h1>
            </div>
            <p className="subtitle">AI-Powered Cultural Intelligence Research</p>
          </div>
        </header>

        <div className="search-section">
          <form onSubmit={handleSubmit} className="search-form">
            <div className="search-input-container">
              <SearchIcon />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your research query..."
                className="search-input"
                disabled={isResearching}
              />
              <button 
                type="submit" 
                className="search-button"
                disabled={isResearching || !query.trim()}
              >
                {isResearching ? 'Researching...' : 'Research'}
              </button>
            </div>
          </form>

          <div className="sample-queries">
            <p className="sample-label">Try these cultural intelligence queries:</p>
            <div className="sample-grid">
              {sampleQueries.map((sampleQuery, index) => (
                <button
                  key={index}
                  onClick={() => handleSampleQuery(sampleQuery)}
                  className="sample-query"
                  disabled={isResearching}
                >
                  {sampleQuery}
                </button>
              ))}
            </div>
          </div>
        </div>

        {currentResult && (
          <div className="result-section">
            <div className="result-header">
              <FileTextIcon />
              <h3>Research Progress</h3>
            </div>
            <div className="result-content">
              <pre>{currentResult}</pre>
            </div>
          </div>
        )}

        <div className="features">
          <div className="feature">
            <GlobeIcon />
            <h3>Cultural Intelligence</h3>
            <p>Powered by Qloo API for deep cultural insights</p>
          </div>
          <div className="feature">
            <UsersIcon />
            <h3>Multi-Agent System</h3>
            <p>Collaborative AI agents for comprehensive research</p>
          </div>
          <div className="feature">
            <TrendingUpIcon />
            <h3>Trend Analysis</h3>
            <p>Real-time analysis of cultural and market trends</p>
          </div>
        </div>
      </div>

      <aside className="sidebar">
        <div className="sidebar-header">
          <ClockIcon />
          <h3>Research History</h3>
        </div>
        <div className="history-list">
          {results.length === 0 ? (
            <p className="no-history">No research history yet</p>
          ) : (
            results.map((result) => (
              <div key={result.id} className="history-item">
                <div className="history-query">{result.query}</div>
                <div className="history-meta">
                  <span className={`status ${result.status}`}>
                    {result.status === 'completed' ? '✅' : result.status === 'in-progress' ? '⏳' : '❌'}
                    {result.status}
                  </span>
                  <span className="timestamp">{result.timestamp}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </aside>
    </div>
  );
}

export default App;