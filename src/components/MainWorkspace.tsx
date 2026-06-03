import { Breadcrumb, Space } from 'antd';

import DashboardView from './DashboardView';
import AnalysisView from './AnalysisView';
import PortfolioView from './PortfolioView';
import DeveloperConsole from './DeveloperConsole';

interface MainWorkspaceProps {
  activeKey: string;
  currentTicker: string;
  setCurrentTicker: (ticker: string) => void;
  priceData: any;
  loading: boolean;
}

export default function MainWorkspace({
  activeKey,
  currentTicker,
  setCurrentTicker,
  priceData,
  loading
}: MainWorkspaceProps) {
  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      {/* Breadcrumb Trail */}
      <Breadcrumb>
        <Breadcrumb.Item>Workspace</Breadcrumb.Item>
        <Breadcrumb.Item>
          {activeKey === 'dashboard' ? 'Market Dashboard' :
           activeKey === 'chat' ? 'AI Agent Grid' :
           activeKey === 'portfolio' ? 'Positions Manager' :
           'Developer API'}
        </Breadcrumb.Item>
        <Breadcrumb.Item>{currentTicker}</Breadcrumb.Item>
      </Breadcrumb>

      {/* Dynamic View Injection */}
      {activeKey === 'dashboard' && (
        <DashboardView 
          ticker={currentTicker}
          priceData={priceData}
          loading={loading}
        />
      )}


      {activeKey === 'chat' && (
        <div style={{ maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
          <AnalysisView onStockLoaded={setCurrentTicker} />
        </div>
      )}

      {activeKey === 'portfolio' && (
        <PortfolioView />
      )}

      {activeKey === 'dev-console' && (
        <div style={{ maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
          <DeveloperConsole />
        </div>
      )}
    </Space>
  );
}
