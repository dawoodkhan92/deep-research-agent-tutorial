import React, { useState } from 'react';
import { Search, FileText, Clock, Sparkles, Globe, Users, TrendingUp } from 'lucide-react';
import './App.css';

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
              <Sparkles className="logo-icon" />
              <h1>Deep Research Agency</h1>
            </div>
            <p className="subtitle">AI-Powered Cultural Intelligence Research</p>
          </div>
        </header>

        <div className="search-section">
          <form onSubmit={handleSubmit} className="search-form">
            <div className="search-input-container">
              <Search className="search-icon" />
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
              <FileText className="result-icon" />
              <h3>Research Progress</h3>
            </div>
            <div className="result-content">
              <pre>{currentResult}</pre>
            </div>
          </div>
        )}

        <div className="features">
          <div className="feature">
            <Globe className="feature-icon" />
            <h3>Cultural Intelligence</h3>
            <p>Powered by Qloo API for deep cultural insights</p>
          </div>
          <div className="feature">
            <Users className="feature-icon" />
            <h3>Multi-Agent System</h3>
            <p>Collaborative AI agents for comprehensive research</p>
          </div>
          <div className="feature">
            <TrendingUp className="feature-icon" />
            <h3>Trend Analysis</h3>
            <p>Real-time analysis of cultural and market trends</p>
          </div>
        </div>
      </div>

      <aside className="sidebar">
        <div className="sidebar-header">
          <Clock className="sidebar-icon" />
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