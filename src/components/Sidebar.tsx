import { Layout, Menu, theme } from 'antd';

import { 
  DashboardOutlined, 
  MessageOutlined, 
  TableOutlined, 
  CodeOutlined 
} from '@ant-design/icons';

const { Sider } = Layout;

interface SidebarProps {
  collapsed: boolean;
  activeKey: string;
  onChangeKey: (key: string) => void;
}

export default function Sidebar({ collapsed, activeKey, onChangeKey }: SidebarProps) {
  const { token } = theme.useToken();

  const menuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: 'Market Dashboard',
    },
    {
      key: 'chat',
      icon: <MessageOutlined />,
      label: 'AI Agent Grid',
    },
    {
      key: 'portfolio',
      icon: <TableOutlined />,
      label: 'Stock Positions',
    },
    {
      key: 'dev-console',
      icon: <CodeOutlined />,
      label: 'Developer API',
    },
  ];

  return (
    <Sider 
      trigger={null} 
      collapsible 
      collapsed={collapsed}
      style={{
        background: token.colorBgContainer,
        borderRight: `1px solid ${token.colorBorderSecondary}`,
      }}
    >
      <div style={{ 
        height: 72, 
        margin: 0, 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        background: token.colorBgContainer,
        borderBottom: `1px solid ${token.colorBorderSecondary}`,
        gap: '8px'
      }}>
        <span style={{ fontSize: '1.5rem', textShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>⚡</span>
        {!collapsed && (
          <span style={{ 
            fontWeight: 800, 
            fontSize: '1rem',
            letterSpacing: '-0.5px',
            color: token.colorPrimary
          }}>
            Forecaster Grid
          </span>
        )}
      </div>

      <Menu
        mode="inline"
        selectedKeys={[activeKey]}
        onClick={({ key }) => onChangeKey(key)}
        items={menuItems}
        style={{
          borderRight: 0,
          paddingTop: '8px',
        }}
      />
    </Sider>
  );
}
