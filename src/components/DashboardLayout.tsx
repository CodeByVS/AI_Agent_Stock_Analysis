import React from 'react';
import { Layout, Button, Badge, Space, Input, Popover, List, theme } from 'antd';
import { 
  MenuFoldOutlined, 
  MenuUnfoldOutlined, 
  BellOutlined, 
  SunOutlined, 
  MoonOutlined, 
  ReloadOutlined 
} from '@ant-design/icons';
import Sidebar from './Sidebar';

const { Header, Content } = Layout;

interface DashboardLayoutProps {
  isDarkMode: boolean;
  setIsDarkMode: (val: boolean) => void;
  collapsed: boolean;
  setCollapsed: (val: boolean) => void;
  activeKey: string;
  setActiveKey: (key: string) => void;
  setCurrentTicker: (ticker: string) => void;
  loading: boolean;
  onSync: () => void;
  children: React.ReactNode;
}

export default function DashboardLayout({
  isDarkMode,
  setIsDarkMode,
  collapsed,
  setCollapsed,
  activeKey,
  setActiveKey,
  setCurrentTicker,
  loading,
  onSync,
  children
}: DashboardLayoutProps) {

  const { token } = theme.useToken();

  const alertsData = [
    { title: 'AAPL Target Price Reached', description: 'Apple Inc. climbed past $182.00 target.', time: '5m ago' },
    { title: 'AI Synthesis Compiled', description: 'AI Agent Grid completed PLTR performance summary.', time: '1h ago' },
    { title: 'Alpha Vantage Telemetry Alert', description: 'Alpha Vantage API daily limits refreshed.', time: '4h ago' }
  ];

  const notificationContent = (
    <List
      size="small"
      dataSource={alertsData}
      renderItem={item => (
        <List.Item>
          <List.Item.Meta
            title={<span style={{ fontSize: '0.82rem', fontWeight: 600 }}>{item.title}</span>}
            description={<span style={{ fontSize: '0.75rem' }}>{item.description} <br/> <small style={{ color: '#8c8c8c' }}>{item.time}</small></span>}
          />
        </List.Item>
      )}
      style={{ width: '280px' }}
    />
  );

  return (
    <Layout style={{ minHeight: '100vh' }}>
      {/* Collapsible Sidebar */}
      <Sidebar 
        collapsed={collapsed} 
        activeKey={activeKey} 
        onChangeKey={setActiveKey} 
      />

      <Layout style={{ background: token.colorBgBase }}>
        {/* Top Header Panel (Spacious UI Controls) */}
        <Header style={{ 
          background: token.colorBgContainer, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between',
          borderBottom: `1px solid ${token.colorBorder}`,
          height: 72,
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.015)'
        }}>
          <Space size="large">
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
              style={{ fontSize: '18px', width: 44, height: 44 }}
            />
            <Input.Search
              placeholder="Search ticker..."
              onSearch={(value) => value.trim() && setCurrentTicker(value.toUpperCase())}
              style={{ width: 240 }}
            />
          </Space>

          <Space size="middle">
            <Button 
              icon={<ReloadOutlined />} 
              onClick={onSync} 
              loading={loading}
            >
              Sync Data
            </Button>

            <Button
              icon={isDarkMode ? <SunOutlined /> : <MoonOutlined />}
              onClick={() => setIsDarkMode(!isDarkMode)}
            />

            <Popover 
              content={notificationContent} 
              title={<strong style={{ fontSize: '0.85rem' }}>Workspace Alerts</strong>} 
              trigger="click" 
              placement="bottomRight"
            >
              <Badge count={alertsData.length} size="small" style={{ cursor: 'pointer' }}>
                <Button icon={<BellOutlined />} />
              </Badge>
            </Popover>
          </Space>
        </Header>

        {/* Breathable Content Panel */}
        <Content style={{ 
          margin: '24px', 
          padding: '32px', 
          background: token.colorBgContainer,
          borderRadius: token.borderRadiusLG,
          border: `1px solid ${token.colorBorder}`,
          overflowY: 'auto',
          minHeight: '280px'
        }}>
          {children}
        </Content>
      </Layout>
    </Layout>
  );
}
