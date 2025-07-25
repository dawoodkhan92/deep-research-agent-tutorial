import React, { useState } from 'react';
import './App.css';

// Simple icons as SVG components
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

const BrainIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/>
    <path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/>
    <path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/>
    <path d="M17.599 6.5a3 3 0 0 0 .399-1.375"/>
    <path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/>
    <path d="M3.477 10.896a4 4 0 0 1 .585-.396"/>
    <path d="M19.938 10.5a4 4 0 0 1 .585.396"/>
    <path d="M6 18a4 4 0 0 1-1.967-.516"/>
    <path d="M19.967 17.484A4 4 0 0 1 18 18"/>
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

const NetworkIcon = () => (
  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M9 12a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"/>
    <path d="M12 1v6m0 6v6"/>
    <path d="m21 9-6 6-6-6-6 6"/>
    <path d="m21 15-6-6-6 6-6-6"/>
  </svg>
);

const DatabaseIcon = () => (
  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <ellipse cx="12" cy="5" rx="9" ry="3"/>
    <path d="M3 5v14a9 3 0 0 0 18 0V5"/>
    <path d="M3 12a9 3 0 0 0 18 0"/>
  </svg>
);

interface ResearchResult {
  id: string;
  query: string;
  timestamp: string;
  status: 'pending' | 'completed' | 'error';
  agent?: string;
}

// Sample queries based on the project's focus areas
const sampleQueries = [
  "Research the economic impact of semaglutide on global healthcare systems",
  "Analyze cultural preferences for K-pop music among Gen Z in the United States",
  "What can you tell me about TechCorp Solutions based on internal documents?",
  "Investigate sustainable fashion trends among millennials in Europe",
  "Research helium-3 lunar mining technology and market opportunities"
];

function App() {
  const [query, setQuery] = useState('');
  const [isResearching, setIsResearching] = useState(false);
  const [researchHistory, setResearchHistory] = useState<ResearchResult[]>([]);
  const [currentResult, setCurrentResult] = useState<string>('');
  const [currentAgent, setCurrentAgent] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const newQuery: ResearchResult = {
      id: Date.now().toString(),
      query: query.trim(),
      timestamp: new Date().toLocaleTimeString(),
      status: 'pending'
    };

    setResearchHistory(prev => [newQuery, ...prev]);
    setIsResearching(true);
    setCurrentResult('');

    // Simulate the multi-agent workflow from DeepResearchAgency
    const agents = ['Triage Agent', 'Clarifying Questions Agent', 'Instruction Builder Agent', 'Research Agent'];
    let step = 0;

    const simulateAgentWork = () => {
      if (step < agents.length) {
        setCurrentAgent(agents[step]);
        setCurrentResult(prev => prev + `\n🔄 ${agents[step]} is working...\n`);
        
        setTimeout(() => {
          if (agents[step] === 'Research Agent') {
            setCurrentResult(prev => prev + `\n🔍 Performing deep research with web search and cultural intelligence...\n🌐 Accessing internal documents via MCP server...\n🎯 Integrating Qloo cultural insights...\n\n✅ Research completed!\n\nThis is where comprehensive research results would appear, including:\n- Web search findings\n- Internal document insights\n- Cultural intelligence from Qloo API\n- Professional PDF report generation\n\nTo connect this UI to your Python backend, you would:\n1. Set up API endpoints in your agency files\n2. Connect the frontend to stream real research results\n3. Display actual agent handoffs and tool usage`);
            
            setResearchHistory(prev => 
              prev.map(item => 
                item.id === newQuery.id 
                  ? { ...item, status: 'completed', agent: 'Research Agent' }
                  : item
              )
            );
            setIsResearching(false);
            setCurrentAgent('');
          } else {
            step++;
            simulateAgentWork();
          }
        }, 1000);
      }
    };

    simulateAgentWork();
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
              <BrainIcon />
              <h1>Deep Research Agency</h1>
            </div>
            <p className="subtitle">
              Multi-Agent AI Research with Cultural Intelligence
            </p>
            <div className="tech-stack">
              <span className="tech-badge">OpenAI o4-mini-deep-research</span>
              <span className="tech-badge">Agency Swarm v1.x</span>
              <span className="tech-badge">Qloo Cultural Intelligence</span>
              <span className="tech-badge">MCP Integration</span>
            </div>
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
                {isResearching ? 'Researching...' : 'Start Research'}
              </button>
            </div>
          </form>

          <div className="sample-queries">
            <p className="sample-label">Try these research queries from the project:</p>
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

        {isResearching && (
          <div className="agent-workflow">
            <div className="workflow-card">
              <h3>🤖 Multi-Agent Workflow Active</h3>
              <div className="agent-steps">
                <div className={`agent-step ${currentAgent === 'Triage Agent' ? 'active' : 'completed'}`}>
                  <span className="step-number">1</span>
                  <div className="step-info">
                    <strong>Triage Agent</strong>
                    <p>Analyzing query complexity</p>
                  </div>
                </div>
                <div className={`agent-step ${currentAgent === 'Clarifying Questions Agent' ? 'active' : currentAgent === 'Instruction Builder Agent' || currentAgent === 'Research Agent' ? 'completed' : ''}`}>
                  <span className="step-number">2</span>
                  <div className="step-info">
                    <strong>Clarifying Agent</strong>
                    <p>Gathering context (if needed)</p>
                  </div>
                </div>
                <div className={`agent-step ${currentAgent === 'Instruction Builder Agent' ? 'active' : currentAgent === 'Research Agent' ? 'completed' : ''}`}>
                  <span className="step-number">3</span>
                  <div className="step-info">
                    <strong>Instruction Builder</strong>
                    <p>Enriching research instructions</p>
                  </div>
                </div>
                <div className={`agent-step ${currentAgent === 'Research Agent' ? 'active' : ''}`}>
                  <span className="step-number">4</span>
                  <div className="step-info">
                    <strong>Research Agent</strong>
                    <p>Deep research with cultural intelligence</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {currentResult && (
          <div className="result-section">
            <div className="result-header">
              <FileTextIcon />
              <h3>Research Progress & Results</h3>
            </div>
            <div className="result-content">
              <pre>{currentResult}</pre>
            </div>
          </div>
        )}

        <div className="features">
          <div className="feature">
            <UsersIcon />
            <h3>Multi-Agent Architecture</h3>
            <p>Triage → Clarifying → Instruction → Research workflow from OpenAI cookbook</p>
          </div>
          <div className="feature">
            <NetworkIcon />
            <h3>Hybrid Search</h3>
            <p>Web search + internal documents via MCP + Qloo cultural intelligence</p>
          </div>
          <div className="feature">
            <DatabaseIcon />
            <h3>Knowledge Integration</h3>
            <p>Access to TechCorp data, market research, and cultural insights</p>
          </div>
        </div>
      </div>

      <aside className="sidebar">
        <div className="sidebar-header">
          <ClockIcon />
          <h3>Research History</h3>
        </div>
        <div className="history-list">
          {researchHistory.length === 0 ? (
            <p className="no-history">No research queries yet</p>
          ) : (
            researchHistory.map((result) => (
              <div key={result.id} className="history-item">
                <div className="history-query">{result.query}</div>
                <div className="history-meta">
                  <span className={`status ${result.status}`}>
                    {result.status === 'completed' ? '✅' : result.status === 'pending' ? '⏳' : '❌'}
                    {result.status}
                  </span>
                  <span className="timestamp">{result.timestamp}</span>
                </div>
                {result.agent && (
                  <div className="agent-info">Agent: {result.agent}</div>
                )}
              </div>
            ))
          )}
        </div>
        
        <div className="project-info">
          <h4>Project Features</h4>
          <ul>
            <li>✅ Agency Swarm v1.x</li>
            <li>✅ OpenAI Deep Research</li>
            <li>✅ Qloo Cultural Intelligence</li>
            <li>✅ MCP File Search</li>
            <li>✅ PDF Report Generation</li>
            <li>✅ Zero Data Retention</li>
          </ul>
        </div>
      </aside>
    </div>
  );
}

export default App;