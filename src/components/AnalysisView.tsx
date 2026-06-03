import { useState, useEffect, useRef } from 'react';
import { Card, Input, Button, theme, Timeline, Spin, Avatar } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined } from '@ant-design/icons';

interface AnalysisViewProps {
  onStockLoaded: (symbol: string) => void;
}

const TypewriterText = ({ text }: { text: string }) => {
  const [displayedText, setDisplayedText] = useState('');
  
  useEffect(() => {
    if (!text) return;
    setDisplayedText('');
    let idx = 0;
    const intervalTime = text.length > 500 ? 2 : 5;
    
    const timer = setInterval(() => {
      setDisplayedText((prev) => prev + text.charAt(idx));
      idx++;
      if (idx >= text.length) {
        clearInterval(timer);
      }
    }, intervalTime);
    
    return () => clearInterval(timer);
  }, [text]);

  return (
    <div className="analysis-result-markdown">
      {displayedText.split('\n').map((line, idx) => {
        if (line.startsWith('### ') || line.startsWith('## ')) {
          return <h3 key={idx} style={{ marginTop: '8px' }}>{line.replace(/^###?\s+/, '')}</h3>;
        }
        if (line.startsWith('**') && line.endsWith('**')) {
          return <p key={idx}><strong>{line.replace(/\*\*/g, '')}</strong></p>;
        }
        if (line.startsWith('* **') || line.startsWith('- **')) {
          const matches = line.match(/^[\s-*]+\*\*(.*?)\*\*(.*)/);
          if (matches) {
            return <p key={idx} style={{ marginLeft: '8px' }}><strong>{matches[1]}</strong>{matches[2]}</p>;
          }
        }
        if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
          return <li key={idx} style={{ marginLeft: '12px' }}>{line.replace(/^[\s-*]+\s+/, '')}</li>;
        }
        if (line.trim() === '') {
          return <div key={idx} style={{ height: '6px' }}></div>;
        }
        return <p key={idx}>{line}</p>;
      })}
      <span className="typewriter-cursor"></span>
    </div>
  );
};

export default function AnalysisView({ onStockLoaded }: AnalysisViewProps) {
  const { token } = theme.useToken();
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [steps, setSteps] = useState<any[]>([]);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, loading]);

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const userMsg = query;
    setQuery('');
    setLoading(true);

    setChatHistory(prev => [...prev, { sender: 'user', text: userMsg }]);

    setSteps([
      { id: 1, name: 'Ticker Identify Agent', status: 'working', desc: 'Extracting ticker symbol...' },
      { id: 2, name: 'Stock Price Agent', status: 'pending', desc: 'Awaiting symbol extraction...' },
      { id: 3, name: 'News Retrieval Agent', status: 'pending', desc: 'Awaiting symbol extraction...' },
      { id: 4, name: 'Price Variance Agent', status: 'pending', desc: 'Awaiting symbol extraction...' },
      { id: 5, name: 'Synthesis Analyst Agent', status: 'pending', desc: 'Compiling reports...' }
    ]);

    try {
      await new Promise(r => setTimeout(r, 600));
      setSteps(prev => prev.map(s => {
        if (s.id === 1) return { ...s, status: 'completed', desc: 'Ticker resolved' };
        if (s.id === 2) return { ...s, status: 'working', desc: 'Fetching prices from AV query...' };
        return s;
      }));

      await new Promise(r => setTimeout(r, 600));
      setSteps(prev => prev.map(s => {
        if (s.id === 2) return { ...s, status: 'completed', desc: 'Quotes loaded' };
        if (s.id === 3) return { ...s, status: 'working', desc: 'Fetching headlines and index metrics...' };
        if (s.id === 4) return { ...s, status: 'working', desc: 'Calculating timeframe ratios...' };
        return s;
      }));

      const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMsg })
      });

      if (!res.ok) throw new Error('API server returned error state.');
      const data = await res.json();

      setSteps(prev => prev.map(s => {
        if (s.id === 3) return { ...s, status: 'completed', desc: 'Articles fetched' };
        if (s.id === 4) return { ...s, status: 'completed', desc: 'Variance measured' };
        if (s.id === 5) return { ...s, status: 'working', desc: `Processing LLM summaries (${data.llm_used})...` };
        return s;
      }));

      await new Promise(r => setTimeout(r, 800));
      setSteps(prev => prev.map(s => {
        if (s.id === 5) return { ...s, status: 'completed', desc: 'Insights synthesized' };
        return s;
      }));

      if (onStockLoaded && data.ticker) {
        onStockLoaded(data.ticker);
      }

      setChatHistory(prev => [...prev, {
        sender: 'agent',
        ticker: data.ticker,
        analysis: data.analysis,
        llm: data.llm_used
      }]);
    } catch (err: any) {
      setChatHistory(prev => [...prev, {
        sender: 'agent',
        text: `⚠️ Agent Error: ${err.message || 'Workflow pipeline interrupted.'}`
      }]);
      setSteps([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card 
      style={{ borderRadius: token.borderRadiusLG }} 
      title="Conversational AI Stock Agent Grid"
      bodyStyle={{ height: '540px', display: 'flex', flexDirection: 'column', padding: '16px' }}
    >
      <div className="chat-scroller">
        {chatHistory.length === 0 && !loading && (
          <div className="chat-placeholder" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: token.colorTextDescription, gap: '12px' }}>
            <span style={{ fontSize: '3rem' }}>🔮</span>
            <span style={{ fontWeight: 600 }}>Awaiting NLP Agent Prompt</span>
            <span style={{ fontSize: '0.8rem', textAlign: 'center', maxWidth: '300px' }}>
              Ask questions like: "Why did Nvidia stock climb today?" or "Give me a news summary for Tesla."
            </span>
          </div>
        )}

        {chatHistory.map((msg, index) => (
          <div key={index} style={{ display: 'flex', gap: '12px', justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start', marginBottom: '16px' }}>
            {msg.sender === 'agent' && (
              <Avatar icon={<RobotOutlined />} style={{ background: token.colorPrimary, color: '#fff', flexShrink: 0 }} />
            )}
            <div className={`chat-bubble ${msg.sender}`} style={{ margin: 0 }}>
              {msg.text && <div>{msg.text}</div>}
              {msg.analysis && (
                <div>
                  <TypewriterText text={msg.analysis} />
                  <div className="analysis-meta">
                    <span>Engine: <strong>{msg.llm}</strong></span>
                    <span>Symbol: <strong>{msg.ticker}</strong></span>
                  </div>
                </div>
              )}
            </div>
            {msg.sender === 'user' && (
              <Avatar icon={<UserOutlined />} style={{ background: token.colorFillSecondary, color: token.colorText, flexShrink: 0 }} />
            )}
          </div>
        ))}

        {loading && (
          <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-start', marginBottom: '16px' }}>
            <Avatar icon={<RobotOutlined />} style={{ background: token.colorPrimary, color: '#fff', flexShrink: 0 }} />
            <div className="chat-bubble agent" style={{ width: '100%', maxWidth: '100%', padding: '12px', margin: 0 }}>
              <div className="agent-pipeline-timeline">
                <Timeline 
                  items={steps.map(step => ({
                    color: step.status === 'completed' ? 'green' : step.status === 'working' ? 'blue' : 'gray',
                    children: (
                      <div>
                        <strong>{step.name}</strong>
                        <div style={{ fontSize: '0.7rem', color: token.colorTextDescription }}>{step.desc}</div>
                      </div>
                    )
                  }))}
                />
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '4px 8px', fontSize: '0.75rem', color: token.colorTextSecondary }}>
                <Spin size="small" />
                <span>Multi-agent reasoning workflow in action...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <form onSubmit={handleQuery} style={{ display: 'flex', gap: '10px' }}>
        <Input 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Query AI Stock Agents (e.g. Why did Tesla drop today?)"
          disabled={loading}
          style={{ height: '40px' }}
        />
        <Button 
          type="primary" 
          htmlType="submit" 
          icon={<SendOutlined />}
          disabled={loading || !query.trim()}
          style={{ height: '40px' }}
        >
          Run
        </Button>
      </form>
    </Card>
  );
}
