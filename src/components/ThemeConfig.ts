import { theme } from 'antd';

export const getThemeConfig = (isDarkMode: boolean) => ({
  algorithm: isDarkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
  token: {
    colorPrimary: isDarkMode ? '#00e5ff' : '#2563eb',
    colorBgBase: isDarkMode ? '#030712' : '#f8fafc',
    colorBgContainer: isDarkMode ? '#0b1329' : '#ffffff',
    colorBorder: isDarkMode ? 'rgba(0, 229, 255, 0.08)' : 'rgba(15, 23, 42, 0.06)',
    colorBorderSecondary: isDarkMode ? 'rgba(0, 229, 255, 0.04)' : 'rgba(15, 23, 42, 0.03)',
    colorTextBase: isDarkMode ? '#e2e8f0' : '#0f172a',
    borderRadius: 12,
    fontFamily: "'Manrope', 'Outfit', sans-serif",
    
    // Spacing overrides
    paddingLG: 24,
    marginLG: 24,
  },
  components: {
    Layout: {
      colorBgHeader: isDarkMode ? '#070c1b' : '#ffffff',
      colorBgBody: isDarkMode ? '#030712' : '#f8fafc',
      headerPadding: '0 24px',
    },
    Card: {
      paddingLG: 24,
      colorBgContainer: isDarkMode ? '#0b1329' : '#ffffff',
    },
    Table: {
      padding: 16,
      colorHeaderBg: isDarkMode ? '#0e1735' : '#f1f5f9',
    },
    Menu: {
      colorItemBg: 'transparent',
      colorItemBgSelected: isDarkMode ? 'rgba(0, 229, 255, 0.08)' : 'rgba(37, 99, 235, 0.06)',
      colorItemTextSelected: isDarkMode ? '#00e5ff' : '#2563eb',
    },
    Button: {
      controlHeight: 40,
      borderRadius: 8,
    },
    Input: {
      controlHeight: 40,
      borderRadius: 8,
    }
  }
});
