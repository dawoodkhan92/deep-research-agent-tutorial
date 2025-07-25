import React, { useState } from 'react';
import './App.css';

interface ResearchQuery {
  id: string;
  query: string;
  timestamp: string;
  status: 'pending' | 'completed' | 'error';
}

function App() {
  const [query, setQuery] = useState('');
  const [isResearching, setIsResearching] = useState(false);
  const [researchHistory, setResearchHistory] = useState<ResearchQuery[]>([]);
  const [currentResult, setCurrentResult] = useState<string>('');

  const sampleQueries = [
    "What are the emerging cultural trends in Gen Z dining preferences?",
    "How do cultural values influence luxury brand perception in Asia?",
    "What entertainment preferences drive social media engagement?",
    "How do regional food cultures impact restaurant success?"
  ];

  const handleSampleQuery = (sampleQuery: string) => {
    setQuery(sampleQuery);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const newQuery: ResearchQuery = {
      id: Date.now().toString(),
      query: query.trim(),
      timestamp: new Date().toLocaleTimeString(),
      status: 'pending'
    };

    setResearchHistory(prev => [newQuery, ...prev]);
    setIsResearching(true);
    setCurrentResult('');

    // Simulate research process
    setTimeout(() => {
      setCurrentResult(`Research completed for: "${query}"\n\nThis is where the Deep Research Agency results would appear. The system would analyze cultural trends, consumer behavior, and provide comprehensive insights using the Qloo API integration.`);
      setResearchHistory(prev => 
        prev.map(item => 
          item.id === newQuery.id 
            ? { ...item, status: 'completed' }
            : item
        )
      );
      setIsResearching(false);
    }, 3000);

    setQuery('');
  };

  return (
    <div className="app">
      <div className="main-content">
        <header className="header">
          <h1 className="title">
            <span className="icon">🔬</span>
            Deep Research Agency
          </h1>
          <p className="subtitle">
            AI-powered cultural intelligence research with Qloo integration
          </p>
        </header>

        <div className="search-section">
          <form onSubmit={handleSubmit} className="search-form">
            <div className="search-container">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask about cultural trends, consumer behavior, or market insights..."
                className="search-input"
                disabled={isResearching}
              />
              <button 
                type="submit" 
                className="search-button"
                disabled={isResearching || !query.trim()}
              >
                {isResearching ? (
                  <span className="loading-spinner"></span>
                ) : (
                  <span className="search-icon">🔍</span>
                )}
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
                  className="sample-button"
                  disabled={isResearching}
                >
                  {sampleQuery}
                </button>
              ))}
            </div>
          </div>
        </div>

        {isResearching && (
          <div className="research-status">
            <div className="status-card">
              <div className="status-header">
                <span className="status-icon">⚡</span>
                <h3>Research in Progress</h3>
              </div>
              <div className="progress-steps">
                <div className="step active">
                  <span className="step-number">1</span>
                  <span>Clarifying research scope</span>
                </div>
                <div className="step active">
                  <span className="step-number">2</span>
                  <span>Gathering cultural data</span>
                </div>
                <div className="step">
                  <span className="step-number">3</span>
                  <span>Analyzing insights</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {currentResult && (
          <div className="results-section">
            <div className="result-card">
              <h3 className="result-title">Research Results</h3>
              <div className="result-content">
                {currentResult.split('\n').map((line, index) => (
                  <p key={index}>{line}</p>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="features-section">
          <h2 className="features-title">Powered by Cultural Intelligence</h2>
          <div className="features-grid">
            <div className="feature-card">
              <span className="feature-icon">🎯</span>
              <h3>Qloo API Integration</h3>
              <p>Advanced cultural and taste intelligence</p>
            </div>
            <div className="feature-card">
              <span className="feature-icon">🤖</span>
              <h3>Multi-Agent Research</h3>
              <p>Collaborative AI agents for comprehensive analysis</p>
            </div>
            <div className="feature-card">
              <span className="feature-icon">📊</span>
              <h3>Cultural Insights</h3>
              <p>Deep understanding of consumer behavior and trends</p>
            </div>
          </div>
        </div>
      </div>

      <aside className="sidebar">
        <h3 className="sidebar-title">Research History</h3>
        <div className="history-list">
          {researchHistory.length === 0 ? (
            <p className="empty-state">No research queries yet</p>
          ) : (
            researchHistory.map((item) => (
              <div key={item.id} className="history-item">
                <div className="history-header">
                  <span className={`status-badge ${item.status}`}>
                    {item.status === 'pending' && '⏳'}
                    {item.status === 'completed' && '✅'}
                    {item.status === 'error' && '❌'}
                  </span>
                  <span className="timestamp">{item.timestamp}</span>
                </div>
                <p className="history-query">{item.query}</p>
              </div>
            ))
          )}
        </div>
      </aside>
    </div>
  );
}

export default App;