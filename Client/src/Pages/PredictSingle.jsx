import React, { useState } from 'react';
import { Button, TextField, MenuItem, Box } from '@mui/material';
import { useSinglePredictMutation } from '../store/api/fileApi'; // Adjust the import path accordingly

const PredictSingle = () => {
  const [formData, setFormData] = useState({
    Department: '',
    Gender: '',
    Mode: '',
    GPA: '',
  });

  const [singlePredict, { data, error, isLoading }] = useSinglePredictMutation();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await singlePredict(formData).unwrap();
      console.log('Prediction response:', response);
    } catch (err) {
      console.error('Failed to predict:', err);
    }
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
          <MenuItem value="Computer_Application">Computer Application</MenuItem>
          <MenuItem value="Pharmacology">Pharmacology</MenuItem>
          <MenuItem value="Computer_Networking_and_Security">Computer Networking and Security</MenuItem>
          <MenuItem value="Medical_Laboratory_Science">Medical Laboratory Science</MenuItem>
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
        <Button type="submit" variant="contained" color="primary" disabled={isLoading}>
          {isLoading ? 'Predicting...' : 'Predict'}
        </Button>
      </form>
      {data && (
        <Box mt={2}>
          <h3>Prediction Result</h3>
          <p>{data.prediction}</p>
        </Box>
      )}
      {error && (
        <Box mt={2} color="red">
          <p>Error: {error.message}</p>
        </Box>
      )}
    </Box>
  );
};

export default PredictSingle;
