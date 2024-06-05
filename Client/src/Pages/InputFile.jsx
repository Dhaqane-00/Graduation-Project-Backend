import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Formik, Form } from 'formik';
import * as Yup from 'yup';
import { ClipLoader } from 'react-spinners';
import { useUploadFileMutation } from '../store/api/fileApi'; // Import the mutation hook
import { Link, useNavigate } from 'react-router-dom';

const handleClear = (resetForm) => {
  resetForm();
  toast.info('Form cleared!');
};

const FileDropzone = ({ setFieldValue }) => {
  const onDrop = useCallback(
    (acceptedFiles, rejectedFiles) => {
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        if (!file.name.match(/\.(xls|xlsx|csv)$/)) {
          toast.error('Please upload a valid Excel or CSV file.');
          return;
        }
        setFieldValue('file', file);
        toast.success('File uploaded successfully!');
      }

      if (rejectedFiles.length > 0) {
        toast.error('Only Excel or CSV files are allowed.');
      }
    },
    [setFieldValue]
  );

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: '.xls, .xlsx, .csv',
  });

  return (
    <div
      {...getRootProps()}
      className="border-2 border-dashed border-gray-300 p-6 text-center cursor-pointer"
    >
      <input {...getInputProps()} />
      <div>
        <h1 className="text-red-500 font-bold text-xl sm:text-2xl mb-4">
          Upload your File:
        </h1>
        <div className="flex justify-center mb-4">
          <img src="path_to_image.png" alt="Upload Icon" className="h-24 w-24" />
        </div>
        <p className="text-gray-500">
          Drag & Drop or{' '}
          <span className="text-blue-500 hover:underline">browse</span>
        </p>
        <p className="text-gray-500">Supports: XLS, XLSX, CSV</p>
      </div>
    </div>
  );
};

const FileUploadSchema = Yup.object().shape({
  file: Yup.mixed()
    .required('A file is required')
    .test('fileType', 'Only Excel or CSV files are allowed', (value) => {
      return value && (value.name.endsWith('.xls') || value.name.endsWith('.xlsx') || value.name.endsWith('.csv'));
    }),
});

const ExcelFileUpload = () => {
  const [loading, setLoading] = useState(false);
  const [uploadFile] = useUploadFileMutation(); // Use the mutation hook
  const navigate = useNavigate();
  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    setLoading(true);
    try {
      await uploadFile(values.file).unwrap(); // Upload the file and get the response
      toast.success('Form submitted successfully!');
      setLoading(false);
      setSubmitting(false);
      resetForm();
      navigate('/results');
    } catch (error) {
      console.error('Failed to upload file:', error);
      toast.error('Failed to upload file.');
      setLoading(false);
      setSubmitting(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-[#ede0d4] p-4 sm:p-6 lg:p-8">
      <ToastContainer />
      <div className="w-full max-w-xs sm:max-w-md lg:max-w-lg">
        <Formik
          initialValues={{ file: null }}
          validationSchema={FileUploadSchema}
          onSubmit={handleSubmit}
        >
          {({ setFieldValue, errors, touched, isSubmitting, resetForm }) => (
            <Form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
              <FileDropzone setFieldValue={setFieldValue} />
              {errors.file && touched.file ? (
                <div className="text-red-500 text-sm mt-2">{errors.file}</div>
              ) : null}
              <div className="flex justify-center mt-4">
                <a
                  href="/sample.xlsx"
                  className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                  download
                >
                  Download Sample Excel
                </a>
              </div>
              <div className="flex items-center justify-between mt-4">
                <button
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 sm:px-8 lg:px-20 rounded focus:outline-none focus:shadow-outline"
                  type="submit"
                  disabled={isSubmitting || loading}
                >
                  {loading ? (
                    <ClipLoader size={20} color={'#fff'} loading={loading} />
                  ) : (
                    'Process File'
                  )}
                </button>
                <button
                  onClick={() => handleClear(resetForm)}
                  className="mt-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-8 rounded focus:outline-none focus:shadow-outline"
                  type="button"
                >
                  Clear File
                </button>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default ExcelFileUpload;
