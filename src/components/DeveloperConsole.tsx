import { useState } from 'react';
import { Card, Input, Select, Button, Space, Spin, theme } from 'antd';

import { PlayCircleOutlined, InfoCircleOutlined } from '@ant-design/icons';

export default function DeveloperConsole() {
  const { token } = theme.useToken();
  const [ticker, setTicker] = useState('TSLA');
  const [timeframe, setTimeframe] = useState('7 days');
  const [loading, setLoading] = useState(false);
  const [jsonResponse, setJsonResponse] = useState<any>(null);
  const [activeAction, setActiveAction] = useState('');

  const handleAction = async (actionType: string) => {
    if (!ticker.trim()) return;

    setLoading(true);
    setActiveAction(actionType);
    setJsonResponse(null);

    const symbol = ticker.toUpperCase();

    try {
      let res;
      if (actionType === 'price') {
        res = await fetch(`/api/stock/${symbol}/price`);
      } else if (actionType === 'news') {
        res = await fetch(`/api/stock/${symbol}/news`);
      } else if (actionType === 'change') {
        res = await fetch(`/api/stock/${symbol}/price-change?timeframe=${encodeURIComponent(timeframe)}`);
      } else if (actionType === 'all') {
        res = await fetch('/api/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: `Fetch transaction logs details for ${symbol} over ${timeframe}` })
        });
      }

      if (!res || !res.ok) {
        throw new Error('API server returned error code during compile validation.');
      }

      const data = await res.json();
      setJsonResponse(data);
    } catch (err: any) {
      setJsonResponse({ error: err.message || 'Endpoint request failure.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card 
      style={{ borderRadius: token.borderRadiusLG }} 
      title="Developer manual API Console"
      bodyStyle={{ display: 'flex', flexDirection: 'column', gap: '16px' }}
    >
      <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: '150px' }}>
          <label style={{ fontSize: '0.75rem', color: token.colorTextDescription, display: 'block', marginBottom: '4px' }}>Symbol</label>
          <Input 
            value={ticker} 
            onChange={(e) => setTicker(e.target.value)}
            placeholder="Symbol"
            style={{ textTransform: 'uppercase', fontWeight: 600 }}
          />
        </div>
        
        <div style={{ flex: 1.5, minWidth: '180px' }}>
          <label style={{ fontSize: '0.75rem', color: token.colorTextDescription, display: 'block', marginBottom: '4px' }}>Variance Timeframe</label>
          <Select 
            value={timeframe} 
            onChange={setTimeframe}
            style={{ width: '100%' }}
          >
            <Select.Option value="today">Today</Select.Option>
            <Select.Option value="7 days">7 Days</Select.Option>
            <Select.Option value="1 month">1 Month</Select.Option>
          </Select>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <Button 
          icon={<PlayCircleOutlined />} 
          onClick={() => handleAction('price')}
          loading={loading && activeAction === 'price'}
        >
          Get Ticker Price API
        </Button>
        <Button 
          icon={<PlayCircleOutlined />} 
          onClick={() => handleAction('news')}
          loading={loading && activeAction === 'news'}
        >
          Get Ticker News API
        </Button>
        <Button 
          icon={<PlayCircleOutlined />} 
          onClick={() => handleAction('change')}
          loading={loading && activeAction === 'change'}
        >
          Net Variance API
        </Button>
        <Button 
          type="primary"
          icon={<PlayCircleOutlined />} 
          onClick={() => handleAction('all')}
          loading={loading && activeAction === 'all'}
        >
          Trigger AI Pipeline API
        </Button>
      </div>

      <div>
        <label style={{ fontSize: '0.75rem', color: token.colorTextDescription, display: 'block', marginBottom: '4px' }}>JSON response payload stream</label>
        <div className="json-output-screen" style={{ height: '240px' }}>
          {loading && (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
              <Spin tip="Waiting on API telemetry response..." />
            </div>
          )}
          {!loading && jsonResponse && (
            <pre style={{ margin: 0 }}>{JSON.stringify(jsonResponse, null, 2)}</pre>
          )}
          {!loading && !jsonResponse && (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: token.colorTextDescription }}>
              <Space><InfoCircleOutlined /> Awaiting developer endpoint invocation...</Space>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}
