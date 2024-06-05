import React, { useState } from 'react';
import {
  Button,
  TextField,
  MenuItem,
  Box,
} from '@mui/material';

const PredictSingle = () => {
  const [formData, setFormData] = useState({
    Department: '',
    Gender: '',
    Mode: '',
    GPA: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form data:', formData);
    // Normally, you would make an API request here
  };

  return (
    <Box>
      <h2>Predict Graduation</h2>
      <form onSubmit={handleSubmit}>
        <TextField
          select
          margin="dense"
          label="Department"
          name="Department"
          value={formData.Department}
          onChange={handleChange}
          fullWidth
          required
        >
          <MenuItem value="Fulltime">Computer_Application</MenuItem>
          <MenuItem value="Parttime">Pharmacology</MenuItem>
          <MenuItem value="Parttime">Computer_Networking_and_Security</MenuItem>
        </TextField>

        <TextField
          margin="dense"
          select
          label="Gender"
          name="Gender"
          value={formData.Gender}
          onChange={handleChange}
          fullWidth
          required
        >
          <MenuItem value="Male">Male</MenuItem>
          <MenuItem value="Female">Female</MenuItem>
        </TextField>
        <TextField
          margin="dense"
          select
          label="Mode"
          name="Mode"
          value={formData.Mode}
          onChange={handleChange}
          fullWidth
          required
        >
          <MenuItem value="Fulltime">Fulltime</MenuItem>
          <MenuItem value="Parttime">Parttime</MenuItem>
        </TextField>
        <TextField
          margin="dense"
          label="GPA"
          name="GPA"
          type="number"
          step="0.01"
          value={formData.GPA}
          onChange={handleChange}
          fullWidth
          required
        />
        <Button type="submit" variant="contained" color="primary">
          Predict
        </Button>
      </form>
    </Box>
  );
};

export default PredictSingle;
