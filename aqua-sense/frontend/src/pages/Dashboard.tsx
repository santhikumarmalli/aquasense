import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  AppBar,
  Toolbar,
  IconButton,
  Badge,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  Settings as SettingsIcon,
  Dashboard as DashboardIcon,
  WaterDrop as WaterDropIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface SensorData {
  timestamp: string;
  ph: number;
  temperature: number;
  turbidity: number;
  dissolvedOxygen: number;
}

interface AlertData {
  id: string;
  severity: 'high' | 'medium' | 'low';
  message: string;
  timestamp: string;
}

const Dashboard: React.FC = () => {
  const [sensorData, setSensorData] = useState<SensorData[]>([]);
  const [alerts, setAlerts] = useState<AlertData[]>([]);
  const [stats, setStats] = useState({
    totalSensors: 24,
    activeSensors: 22,
    alerts: 3,
    quality: 'Good',
  });

  useEffect(() => {
    // Simulate real-time data
    const mockData: SensorData[] = Array.from({ length: 20 }, (_, i) => ({
      timestamp: new Date(Date.now() - (20 - i) * 60000).toLocaleTimeString(),
      ph: 7.2 + Math.random() * 0.6,
      temperature: 22 + Math.random() * 3,
      turbidity: 2 + Math.random() * 2,
      dissolvedOxygen: 7 + Math.random() * 2,
    }));
    setSensorData(mockData);

    // Mock alerts
    setAlerts([
      { id: '1', severity: 'high', message: 'Sensor S-104: High turbidity detected', timestamp: '2 min ago' },
      { id: '2', severity: 'medium', message: 'Sensor S-067: Temperature above threshold', timestamp: '15 min ago' },
      { id: '3', severity: 'low', message: 'Sensor S-032: Routine maintenance required', timestamp: '1 hour ago' },
    ]);

    // Simulate real-time updates
    const interval = setInterval(() => {
      const newReading: SensorData = {
        timestamp: new Date().toLocaleTimeString(),
        ph: 7.2 + Math.random() * 0.6,
        temperature: 22 + Math.random() * 3,
        turbidity: 2 + Math.random() * 2,
        dissolvedOxygen: 7 + Math.random() * 2,
      };
      setSensorData(prev => [...prev.slice(1), newReading]);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const StatCard: React.FC<{ title: string; value: string | number; icon: React.ReactNode; color: string }> = ({
    title,
    value,
    icon,
    color,
  }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="overline">
              {title}
            </Typography>
            <Typography variant="h3" component="div">
              {value}
            </Typography>
          </Box>
          <Box
            sx={{
              backgroundColor: color,
              borderRadius: '50%',
              p: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <WaterDropIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            AquaSense - Water Intelligence Platform
          </Typography>
          <IconButton color="inherit">
            <Badge badgeContent={alerts.length} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>
          <IconButton color="inherit">
            <SettingsIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        {/* Stats Overview */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Total Sensors"
              value={stats.totalSensors}
              icon={<DashboardIcon sx={{ color: 'white' }} />}
              color="#1976d2"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Active Sensors"
              value={stats.activeSensors}
              icon={<CheckCircleIcon sx={{ color: 'white' }} />}
              color="#2e7d32"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Active Alerts"
              value={stats.alerts}
              icon={<WarningIcon sx={{ color: 'white' }} />}
              color="#ed6c02"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Water Quality"
              value={stats.quality}
              icon={<WaterDropIcon sx={{ color: 'white' }} />}
              color="#0288d1"
            />
          </Grid>
        </Grid>

        {/* Charts */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Real-Time Water Quality Metrics
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={sensorData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="timestamp" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="ph" stroke="#1976d2" strokeWidth={2} />
                  <Line type="monotone" dataKey="temperature" stroke="#d32f2f" strokeWidth={2} />
                  <Line type="monotone" dataKey="dissolvedOxygen" stroke="#2e7d32" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>

          {/* Alerts Panel */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Recent Alerts
              </Typography>
              <Box>
                {alerts.map(alert => (
                  <Box
                    key={alert.id}
                    sx={{
                      p: 2,
                      mb: 2,
                      borderLeft: `4px solid ${
                        alert.severity === 'high' ? '#d32f2f' : alert.severity === 'medium' ? '#ed6c02' : '#0288d1'
                      }`,
                      backgroundColor: '#f5f5f5',
                      borderRadius: 1,
                    }}
                  >
                    <Typography variant="body2" fontWeight="bold">
                      {alert.message}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {alert.timestamp}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </Paper>
          </Grid>
        </Grid>

        {/* Additional Information */}
        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                System Status
              </Typography>
              <Typography variant="body2" color="textSecondary">
                All systems operational. Last update: {new Date().toLocaleString()}
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Dashboard;
