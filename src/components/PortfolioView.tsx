import { useState } from 'react';
import { 
  Card, Table, Button, Tag, Modal, Form, 
  Input, InputNumber, DatePicker, Select, 
  Space, notification, Popconfirm, theme, Row, Col, Statistic 
} from 'antd';
import { PlusOutlined, DeleteOutlined, ArrowUpOutlined, ArrowDownOutlined, WalletOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';

interface PositionItem {
  key: string;
  ticker: string;
  name: string;
  buyDate: string;
  shares: number;
  buyPrice: number;
  currentPrice: number;
  strategy: string;
}

const DEFAULT_POSITIONS: PositionItem[] = [
  { key: '1', ticker: 'AAPL', name: 'Apple Inc.', buyDate: '2026-01-15', shares: 50, buyPrice: 175.20, currentPrice: 182.41, strategy: 'Long Term' },
  { key: '2', ticker: 'TSLA', name: 'Tesla Inc.', buyDate: '2026-03-10', shares: 30, buyPrice: 195.50, currentPrice: 177.46, strategy: 'Swing Trade' },
  { key: '3', ticker: 'NVDA', name: 'NVIDIA Corp.', buyDate: '2025-11-20', shares: 20, buyPrice: 980.00, currentPrice: 1150.25, strategy: 'Growth' },
  { key: '4', ticker: 'MSFT', name: 'Microsoft Corp.', buyDate: '2026-02-05', shares: 40, buyPrice: 418.00, currentPrice: 415.13, strategy: 'Dividend' }
];

export default function PortfolioView() {
  const { token } = theme.useToken();
  const [positions, setPositions] = useState<PositionItem[]>(DEFAULT_POSITIONS);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form] = Form.useForm();

  // Portfolio aggregates
  const totalCost = positions.reduce((acc, p) => acc + (p.shares * p.buyPrice), 0);
  const totalValue = positions.reduce((acc, p) => acc + (p.shares * p.currentPrice), 0);
  const totalGain = totalValue - totalCost;
  const totalGainPct = totalCost ? (totalGain / totalCost) * 100 : 0;
  const isProfit = totalGain >= 0;

  const handleAddPosition = (values: any) => {
    const buyPrice = parseFloat(values.buyPrice);
    const shares = parseInt(values.shares);
    const currentPrice = buyPrice * (1 + (Math.random() * 0.3 - 0.15));

    const newPosition: PositionItem = {
      key: Date.now().toString(),
      ticker: values.ticker.toUpperCase(),
      name: `${values.ticker.toUpperCase()} Inc.`,
      buyDate: values.buyDate.format('YYYY-MM-DD'),
      shares,
      buyPrice,
      currentPrice: parseFloat(currentPrice.toFixed(2)),
      strategy: values.strategy
    };

    setPositions(prev => [...prev, newPosition]);
    setIsModalOpen(false);
    form.resetFields();

    notification.success({
      message: 'Position Added',
      description: `Successfully added ${shares} shares of ${values.ticker.toUpperCase()} to your portfolio.`,
      placement: 'topRight'
    });
  };

  const handleDelete = (key: string) => {
    const item = positions.find(p => p.key === key);
    setPositions(prev => prev.filter(p => p.key !== key));
    notification.warning({
      message: 'Position Removed',
      description: `Removed ${item?.ticker} from your active tracking positions.`,
      placement: 'topRight'
    });
  };

  const columns = [
    {
      title: 'Symbol',
      dataIndex: 'ticker',
      key: 'ticker',
      sorter: (a: PositionItem, b: PositionItem) => a.ticker.localeCompare(b.ticker),
      render: (text: string) => <strong style={{ color: token.colorPrimary }}>{text}</strong>
    },
    {
      title: 'Company Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Acquisition Date',
      dataIndex: 'buyDate',
      key: 'buyDate',
      sorter: (a: PositionItem, b: PositionItem) => a.buyDate.localeCompare(b.buyDate),
    },
    {
      title: 'Shares',
      dataIndex: 'shares',
      key: 'shares',
      sorter: (a: PositionItem, b: PositionItem) => a.shares - b.shares,
    },
    {
      title: 'Buy Price',
      dataIndex: 'buyPrice',
      key: 'buyPrice',
      render: (val: number) => `$${val.toFixed(2)}`
    },
    {
      title: 'Market Value',
      key: 'marketValue',
      render: (_: any, record: PositionItem) => {
        const shares = record.shares || 0;
        const currentPrice = record.currentPrice || 0;
        const val = shares * currentPrice;
        return `$${val.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      }
    },
    {
      title: 'P&L State',
      key: 'pnl',
      render: (_: any, record: PositionItem) => {
        const shares = record.shares || 0;
        const buyPrice = record.buyPrice || 1;
        const currentPrice = record.currentPrice || 0;
        const gain = (currentPrice - buyPrice) * shares;
        const gainPct = buyPrice ? ((currentPrice - buyPrice) / buyPrice) * 100 : 0;
        const recordProfit = gain >= 0;

        return (
          <Tag color={recordProfit ? 'success' : 'error'} style={{ fontWeight: 600 }}>
            {recordProfit ? '+' : ''}{gainPct.toFixed(1)}% (${Math.abs(gain).toFixed(2)})
          </Tag>
        );
      }
    },
    {
      title: 'Strategy',
      dataIndex: 'strategy',
      key: 'strategy',
      render: (text: string) => {
        let color = 'blue';
        if (text === 'Swing Trade') color = 'orange';
        if (text === 'Growth') color = 'purple';
        if (text === 'Dividend') color = 'cyan';
        return <Tag color={color}>{text}</Tag>;
      }
    },
    {
      title: 'Action',
      key: 'action',
      render: (_: any, record: PositionItem) => (
        <Popconfirm
          title="Remove Position"
          description="Are you sure you want to delete this stock position?"
          onConfirm={() => handleDelete(record.key)}
          okText="Yes"
          cancelText="No"
        >
          <Button type="text" danger icon={<DeleteOutlined />} />
        </Popconfirm>
      )
    }
  ];

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      {/* Portfolio Aggregates Row */}
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable style={{ background: token.colorBgContainer }}>
            <Statistic
              title="Portfolio Value"
              value={totalValue}
              precision={2}
              prefix={<WalletOutlined style={{ marginRight: '6px', color: token.colorPrimary }} />}
              valueStyle={{ fontWeight: 800 }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable style={{ background: token.colorBgContainer }}>
            <Statistic
              title="Unrealized Gain/Loss"
              value={Math.abs(totalGain)}
              precision={2}
              prefix={isProfit ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
              valueStyle={{ color: isProfit ? token.colorSuccess : token.colorError, fontWeight: 800 }}
              suffix={
                <span style={{ fontSize: '0.85rem', fontWeight: 600, marginLeft: '6px' }}>
                  {totalGainPct.toFixed(1)}%
                </span>
              }
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable style={{ background: token.colorBgContainer }}>
            <Statistic
              title="Total Cost Basis"
              value={totalCost}
              precision={2}
              prefix="$"
              valueStyle={{ fontWeight: 800 }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable style={{ background: token.colorBgContainer }}>
            <Statistic
              title="Asset Holdings"
              value={positions.length}
              suffix="Assets"
              valueStyle={{ fontWeight: 800 }}
            />
          </Card>
        </Col>
      </Row>

      {/* Positions Registry Card */}
      <Card 
        style={{ borderRadius: token.borderRadiusLG }} 
        title={
          <Space>
            <span>Registry Positions</span>
            <Tag color="processing">{positions.length} active</Tag>
          </Space>
        }
        extra={
          <Button 
            type="primary" 
            icon={<PlusOutlined />} 
            onClick={() => setIsModalOpen(true)}
          >
            Add Transaction
          </Button>
        }
      >
        <Table 
          dataSource={positions} 
          columns={columns} 
          pagination={{ pageSize: 5 }} 
          style={{ overflowX: 'auto' }}
        />
      </Card>

      {/* Transaction Modal Form */}
      <Modal
        title="Add Stock Transaction"
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
        destroyOnClose
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleAddPosition}
          initialValues={{ strategy: 'Long Term', buyDate: dayjs() }}
          style={{ marginTop: '16px' }}
        >
          <Form.Item
            name="ticker"
            label="Stock Symbol"
            rules={[{ required: true, message: 'Please input ticker symbol (e.g. AAPL)!' }]}
          >
            <Input placeholder="e.g. AAPL" style={{ textTransform: 'uppercase' }} />
          </Form.Item>

          <Form.Item
            name="buyDate"
            label="Purchase Date"
            rules={[{ required: true, message: 'Please select purchase date!' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>

          <div style={{ display: 'flex', gap: '16px' }}>
            <Form.Item
              name="shares"
              label="Shares Quantity"
              rules={[{ required: true, message: 'Please input quantity!' }]}
              style={{ flex: 1 }}
            >
              <InputNumber min={1} style={{ width: '100%' }} />
            </Form.Item>

            <Form.Item
              name="buyPrice"
              label="Price per Share"
              rules={[{ required: true, message: 'Please input acquisition price!' }]}
              style={{ flex: 1 }}
            >
              <InputNumber min={0.01} precision={2} prefix="$" style={{ width: '100%' }} />
            </Form.Item>
          </div>

          <Form.Item
            name="strategy"
            label="Trading Strategy"
          >
            <Select>
              <Select.Option value="Long Term">Long Term Hold</Select.Option>
              <Select.Option value="Swing Trade">Swing Trade</Select.Option>
              <Select.Option value="Growth">Growth Focus</Select.Option>
              <Select.Option value="Dividend">Dividend Reinvestment</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={() => setIsModalOpen(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit">Submit Trade</Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </Space>
  );
}
