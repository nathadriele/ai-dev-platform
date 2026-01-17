import React, { useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
} from '@mui/material';
import {
  Folder as FolderIcon,
  Psychology as PsychologyIcon,
  Timeline as TimelineIcon,
  SmartToy as SmartToyIcon,
} from '@mui/icons-material';
import { useAppDispatch, useAppSelector } from '@/store/hooks';
import { fetchProjects } from '@/store/slices/projectSlice';
import { fetchAIActivities } from '@/store/slices/aiActivitySlice';

export default function DashboardPage() {
  const dispatch = useAppDispatch();
  const { projects } = useAppSelector((state) => state.projects);
  const { activities } = useAppSelector((state) => state.aiActivities);

  useEffect(() => {
    dispatch(fetchProjects());
    dispatch(fetchAIActivities());
  }, [dispatch]);

  const stats = [
    {
      title: 'Total Projects',
      value: projects.length,
      icon: <FolderIcon fontSize="large" />,
      color: '#1976d2',
    },
    {
      title: 'AI Activities',
      value: activities.length,
      icon: <PsychologyIcon fontSize="large" />,
      color: '#dc004e',
    },
    {
      title: 'Active Agents',
      value: 4,
      icon: <SmartToyIcon fontSize="large" />,
      color: '#ffa000',
    },
    {
      title: 'Productivity Gain',
      value: '+63%',
      icon: <TimelineIcon fontSize="large" />,
      color: '#2e7d32',
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        {stats.map((stat) => (
          <Grid item xs={12} sm={6} md={3} key={stat.title}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography color="textSecondary" gutterBottom variant="body2">
                      {stat.title}
                    </Typography>
                    <Typography variant="h4" component="div">
                      {stat.value}
                    </Typography>
                  </Box>
                  <Box sx={{ color: stat.color }}>{stat.icon}</Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Projects
            </Typography>
            {projects.slice(0, 5).map((project) => (
              <Box key={project.id} sx={{ mb: 2, pb: 2, borderBottom: '1px solid #e0e0e0' }}>
                <Typography variant="subtitle1">{project.name}</Typography>
                <Typography variant="body2" color="textSecondary">
                  {project.description}
                </Typography>
              </Box>
            ))}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent AI Activities
            </Typography>
            {activities.slice(0, 5).map((activity) => (
              <Box key={activity.id} sx={{ mb: 2, pb: 2, borderBottom: '1px solid #e0e0e0' }}>
                <Typography variant="subtitle1">
                  {activity.tool_used.toUpperCase()} - {activity.category}
                </Typography>
                <Typography variant="body2" color="textSecondary" noWrap>
                  {activity.prompt}
                </Typography>
              </Box>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}
