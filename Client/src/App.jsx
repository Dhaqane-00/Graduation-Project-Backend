import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Pages/Home';
import Dashboard from './Pages/Dashboard';
import PredictSingle from './Pages/PredictSingle';
import PredictionResultPage from './Pages/Result';
import ExcelFileUpload from './Pages/InputFile';
import UserManagement from './Pages/UserManagement';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />}>
          <Route path="/" element={<Home />} />
          <Route path="predict-many" element={<ExcelFileUpload />} />
          <Route path="predict-single" element={<PredictSingle />} />
          <Route path="results" element={<PredictionResultPage />} />
          <Route path="users" element={<UserManagement />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
