import React from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { useAppSelector } from '@/store/hooks';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

export default function AnalyticsPage() {
  const { activities } = useAppSelector((state) => state.aiActivities);

  // Prepare data for charts
  const toolUsage = activities.reduce((acc, activity) => {
    acc[activity.tool_used] = (acc[activity.tool_used] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const toolData = Object.entries(toolUsage).map(([name, value]) => ({ name, value }));

  const categoryData = activities.reduce((acc, activity) => {
    acc[activity.category] = (acc[activity.category] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const categoryChartData = Object.entries(categoryData).map(([name, value]) => ({
    name,
    value,
  }));

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Analytics
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              AI Tool Usage
            </Typography>
            <BarChart width={400} height={300} data={toolData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#1976d2" />
            </BarChart>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Activity Categories
            </Typography>
            <PieChart width={400} height={300}>
              <Pie
                data={categoryChartData}
                cx={200}
                cy={150}
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Usage Summary
            </Typography>
            <Box display="flex" justifyContent="space-around" flexWrap="wrap">
              <Box textAlign="center" m={2}>
                <Typography variant="h3">{activities.length}</Typography>
                <Typography variant="body2" color="textSecondary">
                  Total Activities
                </Typography>
              </Box>
              <Box textAlign="center" m={2}>
                <Typography variant="h3">{Object.keys(toolUsage).length}</Typography>
                <Typography variant="body2" color="textSecondary">
                  Tools Used
                </Typography>
              </Box>
              <Box textAlign="center" m={2}>
                <Typography variant="h3">
                  {Math.round(activities.length * 0.25 * 10) / 10}h
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Time Saved
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}
