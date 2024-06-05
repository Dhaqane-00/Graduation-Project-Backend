import React from 'react';
import { useGetResultsQuery } from '../store/api/fileApi';
import { DataGrid } from '@mui/x-data-grid';
import { CircularProgress } from '@mui/material';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const columns = [
  { field: '_id', headerName: 'ID', width: 150 },
  { field: 'Department', headerName: 'Department', width: 230 },
  { field: 'Gender', headerName: 'Gender', width: 130 },
  { field: 'Mode', headerName: 'Mode', width: 130 },
  { field: 'GPA', headerName: 'GPA', width: 100 },
  { field: 'Prediction', headerName: 'Prediction', width: 200 }
];

const PredictionResultPage = () => {
  const { data, error, isLoading } = useGetResultsQuery();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <CircularProgress />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-screen">
        Error loading results...
      </div>
    );
  }

  const rows = data?.results.map(row => ({ id: row._id, ...row })) ?? [];

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#ede0d4] p-4">
      <ToastContainer />
      <div className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6">
        <h1 className="text-2xl font-bold mb-4 text-center">Prediction Results</h1>
        <div className="h-[400px] w-full md:w-[600px] lg:w-full">
          <DataGrid
            rows={rows}
            columns={columns}
            pageSize={5}
            checkboxSelection
          />
        </div>
      </div>
    </div>
  );
};

export default PredictionResultPage;
