import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Chip,
  Divider,
} from '@mui/material';
import { useAppDispatch, useAppSelector } from '@/store/hooks';
import { fetchProject } from '@/store/slices/projectSlice';

export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  const dispatch = useAppDispatch();
  const { currentProject } = useAppSelector((state) => state.projects);

  useEffect(() => {
    if (id) {
      dispatch(fetchProject(id));
    }
  }, [id, dispatch]);

  if (!currentProject) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Typography>Loading...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          {currentProject.name}
        </Typography>
        <Typography variant="body1" color="textSecondary" paragraph>
          {currentProject.description}
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Repository
          </Typography>
          <Typography variant="body2" color="primary">
            {currentProject.repository_url}
          </Typography>
        </Box>

        <Box sx={{ mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Tech Stack
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {currentProject.tech_stack.map((tech) => (
              <Chip key={tech} label={tech} variant="outlined" />
            ))}
          </Box>
        </Box>

        <Box sx={{ mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Status
          </Typography>
          <Chip
            label={currentProject.status}
            color={currentProject.status === 'active' ? 'success' : 'default'}
          />
        </Box>

        <Divider sx={{ my: 2 }} />

        <Typography variant="caption" color="textSecondary">
          Created: {new Date(currentProject.created_at).toLocaleString()}
        </Typography>
      </Paper>
    </Container>
  );
}
