import React from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Chip,
} from '@mui/material';
import { useAppSelector } from '@/store/hooks';

export default function AIActivitiesPage() {
  const { activities } = useAppSelector((state) => state.aiActivities);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        AI Activities
      </Typography>

      <Box display="flex" flexDirection="column" gap={2}>
        {activities.map((activity) => (
          <Card key={activity.id}>
            <CardContent>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Chip label={activity.tool_used.toUpperCase()} color="primary" />
                <Chip label={activity.category} variant="outlined" />
              </Box>
              <Typography variant="body1" paragraph>
                <strong>Prompt:</strong> {activity.prompt}
              </Typography>
              {activity.response && (
                <Typography variant="body2" color="textSecondary" paragraph>
                  <strong>Response:</strong> {activity.response}
                </Typography>
              )}
              <Typography variant="caption" color="textSecondary">
                {new Date(activity.timestamp).toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </Box>
    </Container>
  );
}
