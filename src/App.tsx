import { useState, useEffect } from 'react';
import { ConfigProvider } from 'antd';
import { getThemeConfig } from './components/ThemeConfig';
import DashboardLayout from './components/DashboardLayout';
import MainWorkspace from './components/MainWorkspace';

export default function App() {
  const [collapsed, setCollapsed] = useState(false);
  const [activeKey, setActiveKey] = useState('dashboard');
  const [currentTicker, setCurrentTicker] = useState('AAPL');
  const [priceData, setPriceData] = useState<any>(null);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);

  const loadTickerDetails = async (symbol: string) => {
    setLoadingDetails(true);
    try {
      const res = await fetch(`/api/stock/${symbol}/price`);
      if (res.ok) {
        const data = await res.json();
        setPriceData(data);
      } else {
        throw new Error('API request failed');
      }
    } catch (err) {
      console.warn('Failed to load stock details from backend, using client simulation:', err);
      const basePrices: { [key: string]: any } = {
        AAPL: { price: 182.41, change: 1.25, change_percent: "+0.69%", high: 183.92, low: 180.88, volume: 52400000, name: "Apple Inc." },
        TSLA: { price: 177.46, change: -4.82, change_percent: "-2.64%", high: 184.20, low: 176.80, volume: 86200000, name: "Tesla Inc." },
        NVDA: { price: 1150.25, change: 24.50, change_percent: "+2.18%", high: 1158.10, low: 1130.50, volume: 42100000, name: "NVIDIA Corporation" },
        MSFT: { price: 415.13, change: -2.34, change_percent: "-0.56%", high: 418.40, low: 412.20, volume: 22400000, name: "Microsoft Corporation" },
        AMZN: { price: 181.28, change: 0.45, change_percent: "+0.25%", high: 183.10, low: 179.80, volume: 31500000, name: "Amazon.com Inc." },
        GOOGL: { price: 173.50, change: 1.12, change_percent: "+0.65%", high: 175.10, low: 171.80, volume: 25000000, name: "Alphabet Inc." },
      };
      
      const symbolUpper = symbol.toUpperCase();
      const mockVal = basePrices[symbolUpper] || {
        price: 150.00,
        change: 0.50,
        change_percent: "+0.33%",
        high: 152.00,
        low: 148.00,
        volume: 15000000,
        name: `${symbolUpper} Inc.`
      };
      
      setPriceData({
        status: "success",
        source: "frontend-simulation",
        ...mockVal
      });
    } finally {
      setLoadingDetails(false);
    }
  };

  useEffect(() => {
    if (currentTicker) {
      loadTickerDetails(currentTicker);
    }
  }, [currentTicker]);

  return (
    <ConfigProvider theme={getThemeConfig(isDarkMode)}>
      <DashboardLayout
        isDarkMode={isDarkMode}
        setIsDarkMode={setIsDarkMode}
        collapsed={collapsed}
        setCollapsed={setCollapsed}
        activeKey={activeKey}
        setActiveKey={setActiveKey}
        setCurrentTicker={setCurrentTicker}
        loading={loadingDetails}
        onSync={() => loadTickerDetails(currentTicker)}
      >

        <MainWorkspace
          activeKey={activeKey}
          currentTicker={currentTicker}
          setCurrentTicker={setCurrentTicker}
          priceData={priceData}
          loading={loadingDetails}
        />
      </DashboardLayout>
    </ConfigProvider>
  );
}
