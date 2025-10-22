import React, { useState } from 'react';
import { Upload, Download, FileText, AlertCircle, CheckCircle } from 'lucide-react';

const CSVUploader = ({ 
  onUpload, 
  onDownloadSample, 
  title, 
  description, 
  sampleColumns,
  loading = false 
}) => {
  const [dragOver, setDragOver] = useState(false);
  const [csvContent, setCsvContent] = useState('');
  const [showTextArea, setShowTextArea] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      processFile(file);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragOver(false);
    const file = event.dataTransfer.files[0];
    if (file) {
      processFile(file);
    }
  };

  const processFile = (file) => {
    if (!file.name.toLowerCase().endsWith('.csv')) {
      setUploadStatus({
        type: 'error',
        message: 'Please select a CSV file'
      });
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target.result;
      setCsvContent(content);
      setUploadStatus({
        type: 'info',
        message: `File "${file.name}" loaded. Review and click upload to import.`
      });
    };
    reader.readAsText(file);
  };

  const handleUpload = async () => {
    if (!csvContent.trim()) {
      setUploadStatus({
        type: 'error',
        message: 'Please select a CSV file or enter CSV content'
      });
      return;
    }

    try {
      setUploadStatus({
        type: 'info',
        message: 'Uploading data...'
      });

      const result = await onUpload(csvContent);
      
      setUploadStatus({
        type: 'success',
        message: result.message || 'Data uploaded successfully',
        details: result
      });

      // Clear content after successful upload
      setCsvContent('');
      setShowTextArea(false);
      
      // Clear file input
      const fileInput = document.getElementById(`csv-file-${title.replace(/\s+/g, '-')}`);
      if (fileInput) fileInput.value = '';

    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error.message || 'Failed to upload data'
      });
    }
  };

  const handleDownloadSample = async () => {
    try {
      await onDownloadSample();
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: 'Failed to download sample file'
      });
    }
  };

  const clearStatus = () => {
    setUploadStatus(null);
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
          <p className="text-sm text-gray-600">{description}</p>
        </div>
        <button
          onClick={handleDownloadSample}
          className="flex items-center text-blue-600 hover:text-blue-800 text-sm font-medium"
          disabled={loading}
        >
          <Download size={16} className="mr-1" />
          Sample CSV
        </button>
      </div>

      {/* Expected columns info */}
      <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800 font-medium mb-1">Expected CSV columns:</p>
        <p className="text-sm text-blue-700">{sampleColumns}</p>
      </div>

      {/* Status messages */}
      {uploadStatus && (
        <div className={`mb-4 p-3 rounded-lg border flex items-start ${
          uploadStatus.type === 'success' ? 'bg-green-50 border-green-200 text-green-800' :
          uploadStatus.type === 'error' ? 'bg-red-50 border-red-200 text-red-800' :
          'bg-blue-50 border-blue-200 text-blue-800'
        }`}>
          <div className="flex-shrink-0 mr-2 mt-0.5">
            {uploadStatus.type === 'success' ? (
              <CheckCircle size={16} />
            ) : uploadStatus.type === 'error' ? (
              <AlertCircle size={16} />
            ) : (
              <FileText size={16} />
            )}
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium">{uploadStatus.message}</p>
            {uploadStatus.details && uploadStatus.details.errors && (
              <div className="mt-2 text-xs">
                <p className="font-medium">Import Summary:</p>
                <ul className="list-disc list-inside mt-1">
                  <li>Created: {uploadStatus.details.created_count} / {uploadStatus.details.total_rows}</li>
                  {uploadStatus.details.errors.map((error, index) => (
                    <li key={index} className="text-red-700">{error}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
          <button
            onClick={clearStatus}
            className="flex-shrink-0 ml-2 text-current hover:opacity-70"
          >
            ×
          </button>
        </div>
      )}

      {/* File upload area */}
      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
          dragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
      >
        <Upload size={24} className="mx-auto mb-2 text-gray-400" />
        <p className="text-sm text-gray-600 mb-2">
          Drag and drop your CSV file here, or
        </p>
        <div className="flex justify-center gap-2">
          <label className="cursor-pointer">
            <input
              id={`csv-file-${title.replace(/\s+/g, '-')}`}
              type="file"
              accept=".csv"
              onChange={handleFileSelect}
              className="hidden"
              disabled={loading}
            />
            <span className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50">
              <FileText size={16} className="mr-1" />
              Choose File
            </span>
          </label>
          <button
            onClick={() => setShowTextArea(!showTextArea)}
            className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            disabled={loading}
          >
            {showTextArea ? 'Hide' : 'Paste'} CSV
          </button>
        </div>
      </div>

      {/* Text area for manual CSV input */}
      {showTextArea && (
        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Paste CSV content:
          </label>
          <textarea
            value={csvContent}
            onChange={(e) => setCsvContent(e.target.value)}
            placeholder="Paste your CSV content here..."
            rows={6}
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm font-mono"
            disabled={loading}
          />
        </div>
      )}

      {/* Upload button */}
      {(csvContent || showTextArea) && (
        <div className="mt-4 flex justify-end">
          <button
            onClick={handleUpload}
            disabled={loading || !csvContent.trim()}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            <Upload size={16} className="mr-1" />
            {loading ? 'Uploading...' : 'Upload Data'}
          </button>
        </div>
      )}
    </div>
  );
};

export default CSVUploader;