import React from 'react';
import { useGetResultsQuery } from '../store/api/fileApi';
import { DataGrid } from '@mui/x-data-grid';
import { CircularProgress, IconButton } from '@mui/material';
import { toast, ToastContainer } from 'react-toastify';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';
import 'react-toastify/dist/ReactToastify.css';
import PrintIcon from '@mui/icons-material/Print';
import DownloadIcon from '@mui/icons-material/Download';

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

  const handleDownload = () => {
    const doc = new jsPDF();
    doc.autoTable({
      head: [columns.map(col => col.headerName)],
      body: rows.map(row => columns.map(col => row[col.field])),
    });
    doc.save('table.pdf');
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#ede0d4] p-4">
      <ToastContainer />
      <div className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">Prediction Results</h1>
          <div>
            <IconButton onClick={handleDownload} aria-label="download">
              <DownloadIcon />
            </IconButton>
            <IconButton onClick={handlePrint} aria-label="print">
              <PrintIcon />
            </IconButton>
          </div>
        </div>
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
