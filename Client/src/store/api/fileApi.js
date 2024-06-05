import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const fileApi = createApi({
  reducerPath: 'fileApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://localhost:5000' }), // Ensure this matches your Flask backend
  endpoints: (builder) => ({
    uploadFile: builder.mutation({
      query: (file) => {
        const formData = new FormData();
        formData.append('file', file);
        return {
          url: '/predict',
          method: 'POST',
          body: formData,
          responseHandler: (response) => response.json(), // Ensure response is parsed as JSON
        };
      },
    }),
    getResults: builder.query({
      query: () => ({
        url: '/results',
        method: 'GET',
        responseHandler: (response) => response.json(), // Ensure response is parsed as JSON
      }),
    }),
    getChartData: builder.query({
      query: () => ({
        url: '/chart-data',
        method: 'GET',
        responseHandler: (response) => response.json(), // Ensure response is parsed as JSON
      }),
    }),
    getSummaryChartData: builder.query({
      query: () => ({
        url: '/summary-chart-data',
        method: 'GET',
        responseHandler: (response) => response.json(), // Ensure response is parsed as JSON
      }),
    }),
  }),
});

export const {
  useUploadFileMutation,
  useGetResultsQuery,
  useGetChartDataQuery,
  useGetSummaryChartDataQuery,
} = fileApi;
export default fileApi.reducer;
