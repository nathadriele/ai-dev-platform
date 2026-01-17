import React, { useEffect, useState } from 'react';
import {
  Container,
  Box,
  Button,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useAppDispatch, useAppSelector } from '@/store/hooks';
import { fetchProjects, createProject } from '@/store/slices/projectSlice';
import { Project } from '@/types';

export default function ProjectsPage() {
  const dispatch = useAppDispatch();
  const { projects, isLoading, pagination } = useAppSelector((state) => state.projects);
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    repository_url: '',
    tech_stack: '',
  });

  useEffect(() => {
    dispatch(fetchProjects());
  }, [dispatch]);

  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false);
    setFormData({ name: '', description: '', repository_url: '', tech_stack: '' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await dispatch(
      createProject({
        name: formData.name,
        description: formData.description,
        repository_url: formData.repository_url,
        tech_stack: formData.tech_stack.split(',').map((s) => s.trim()),
      })
    );
    handleClose();
  };

  const columns: GridColDef[] = [
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'description', headerName: 'Description', width: 300 },
    { field: 'repository_url', headerName: 'Repository', width: 250 },
    { field: 'status', headerName: 'Status', width: 120 },
    {
      field: 'tech_stack',
      headerName: 'Tech Stack',
      width: 200,
      valueGetter: (params) => params.value.join(', '),
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Projects</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={handleOpen}>
          New Project
        </Button>
      </Box>

      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={projects}
          columns={columns}
          getRowId={(row) => row.id}
          loading={isLoading}
          rowCount={pagination.total}
          pageSizeOptions={[20]}
          paginationModel={{ page: pagination.page - 1, pageSize: pagination.per_page }}
          paginationMode="server"
        />
      </Box>

      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Project</DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Project Name"
              fullWidth
              variant="outlined"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              sx={{ mb: 2 }}
            />
            <TextField
              margin="dense"
              label="Description"
              fullWidth
              multiline
              rows={3}
              variant="outlined"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              sx={{ mb: 2 }}
            />
            <TextField
              margin="dense"
              label="Repository URL"
              fullWidth
              variant="outlined"
              value={formData.repository_url}
              onChange={(e) => setFormData({ ...formData, repository_url: e.target.value })}
              required
              sx={{ mb: 2 }}
            />
            <TextField
              margin="dense"
              label="Tech Stack (comma-separated)"
              fullWidth
              variant="outlined"
              value={formData.tech_stack}
              onChange={(e) => setFormData({ ...formData, tech_stack: e.target.value })}
              helperText="e.g., React, TypeScript, FastAPI"
              sx={{ mb: 2 }}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button type="submit" variant="contained">
              Create
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
}
