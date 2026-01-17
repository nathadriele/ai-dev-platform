import React from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Button,
  Card,
  CardContent,
  CardActions,
} from '@mui/material';
import { SmartToy, PlayArrow } from '@mui/icons-material';

const AGENTS = [
  {
    id: 'code-scaffolder',
    name: 'Code Scaffolder',
    description: 'Generates project structure and boilerplate code',
    capabilities: ['scaffold', 'boilerplate', 'structure'],
  },
  {
    id: 'code-reviewer',
    name: 'Code Reviewer',
    description: 'Reviews code for bugs, security issues, and best practices',
    capabilities: ['review', 'analyze', 'security'],
  },
  {
    id: 'test-generator',
    name: 'Test Generator',
    description: 'Generates unit and integration tests',
    capabilities: ['testing', 'unit-tests', 'integration-tests'],
  },
  {
    id: 'doc-generator',
    name: 'Documentation Generator',
    description: 'Generates technical documentation',
    capabilities: ['docs', 'documentation', 'markdown'],
  },
];

export default function AgentsPage() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Code Agents
      </Typography>

      <Grid container spacing={3}>
        {AGENTS.map((agent) => (
          <Grid item xs={12} md={6} key={agent.id}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <SmartTodo color="primary" sx={{ mr: 2 }} />
                  <Typography variant="h6">{agent.name}</Typography>
                </Box>
                <Typography variant="body2" color="textSecondary" paragraph>
                  {agent.description}
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={1}>
                  {agent.capabilities.map((cap) => (
                    <Button key={cap} size="small" variant="outlined" disabled>
                      {cap}
                    </Button>
                  ))}
                </Box>
              </CardContent>
              <CardActions>
                <Button variant="contained" startIcon={<PlayArrow />}>
                  Execute
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}
