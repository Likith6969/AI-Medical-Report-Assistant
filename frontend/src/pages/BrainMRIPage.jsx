import React, { useState, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { reportsService } from '../services/api';
import { 
  Activity, 
  ArrowLeft, 
  UploadCloud, 
  Brain, 
  CheckCircle2, 
  AlertCircle, 
  AlertTriangle,
  X, 
  Sparkles, 
  Clock, 
  LogOut, 
  ShieldAlert,
  Layers,
  RefreshCw,
  FileCheck,
  Eye,
  Percent,
  CheckCircle,
  AlertOctagon
} from 'lucide-react';

const CLASS_FORMAT_INFO = {
  glioma: {
    label: 'Glioma',
    badgeClass: 'bg-rose-50 text-rose-700 border-rose-200',
    barColor: 'bg-rose-500',
    description: 'Tumor originating in the glial cells of the brain or spine.',
  },
  meningioma: {
    label: 'Meningioma',
    badgeClass: 'bg-amber-50 text-amber-700 border-amber-200',
    barColor: 'bg-amber-500',
    description: 'Tumor arising from the meninges surrounding the brain and spinal cord.',
  },
  pituitary: {
    label: 'Pituitary Tumor',
    badgeClass: 'bg-cyan-50 text-cyan-700 border-cyan-200',
    barColor: 'bg-cyan-500',
    description: 'Abnormal growth in the pituitary gland at the base of the brain.',
  },
  notumor: {
    label: 'No Tumor Detected',
    badgeClass: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    barColor: 'bg-emerald-500',
    description: 'No pathological tumor mass detected in the examined brain MRI slice.',
  },
};

const BrainMRIPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [filePreview, setFilePreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStage, setProcessingStage] = useState('');
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSelectFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSelectFile(e.target.files[0]);
    }
  };

  const validateAndSelectFile = (selectedFile) => {
    setError('');
    const validExtensions = ['.jpg', '.jpeg', '.png'];
    const filename = selectedFile.name.toLowerCase();
    const isValid = validExtensions.some((ext) => filename.endsWith(ext));

    if (!isValid) {
      setError('Please upload a valid brain MRI scan image (JPG, JPEG, PNG).');
      return;
    }

    if (selectedFile.size > 15 * 1024 * 1024) {
      setError('File size exceeds the 15 MB limit.');
      return;
    }

    setFile(selectedFile);
    setFilePreview(URL.createObjectURL(selectedFile));
  };

  const removeFile = () => {
    setFile(null);
    if (filePreview) {
      URL.revokeObjectURL(filePreview);
      setFilePreview(null);
    }
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    else if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select a brain MRI image to analyze.');
      return;
    }

    setError('');
    setIsProcessing(true);
    setProcessingStage('Uploading neuroimaging scan to secure storage...');

    try {
      const stageTimer1 = setTimeout(() => {
        setProcessingStage('Preprocessing image tensors for ConvNeXt Tiny...');
      }, 1000);

      const stageTimer2 = setTimeout(() => {
        setProcessingStage('Running deep learning neural classification...');
      }, 2500);

      const stageTimer3 = setTimeout(() => {
        setProcessingStage('Generating AI radiological explanation with Gemini 3.5...');
      }, 5000);

      const data = await reportsService.analyzeBrainMRI(file);

      clearTimeout(stageTimer1);
      clearTimeout(stageTimer2);
      clearTimeout(stageTimer3);

      setResult(data);
    } catch (err) {
      console.error('Brain MRI analysis error:', err);
      if (err.response) {
        if (err.response.status === 413) {
          setError('The uploaded image is too large. Maximum supported size is 15 MB.');
        } else {
          const detail = err.response.data?.detail;
          setError(typeof detail === 'string' ? detail : 'MRI Analysis failed. Please check the image format.');
        }
      } else if (err.request) {
        setError('Unable to connect to the backend server. Please verify the API is running.');
      } else {
        setError('An unexpected error occurred while analyzing the MRI scan.');
      }
    } finally {
      setIsProcessing(false);
      setProcessingStage('');
    }
  };

  const predictionKey = (result?.prediction || '').toLowerCase();
  const predictionMeta = CLASS_FORMAT_INFO[predictionKey] || {
    label: result?.prediction?.toUpperCase() || 'Unknown',
    badgeClass: 'bg-slate-100 text-slate-800 border-slate-200',
    barColor: 'bg-cyan-500',
    description: 'Neural model classification result.',
  };

  const probabilities = result?.extracted_data?.class_probabilities || {};
  const probabilityKeys = Object.keys(probabilities);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
      {/* Header Bar */}
      <header className="sticky top-0 z-30 bg-white/85 backdrop-blur-md border-b border-slate-200/80 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              to="/dashboard"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-slate-200 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Dashboard</span>
            </Link>
            <div className="hidden sm:flex items-center gap-2.5 pl-2 border-l border-slate-200">
              <div className="p-1.5 rounded-lg bg-cyan-50 text-cyan-600 border border-cyan-100">
                <Brain className="w-4 h-4" />
              </div>
              <span className="font-bold text-slate-900 text-sm tracking-tight">
                Brain MRI Classifier
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2.5 pl-3 pr-4 py-1.5 rounded-full bg-slate-100/90 border border-slate-200/70">
              <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-600 text-white flex items-center justify-center text-[11px] font-bold">
                {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
              </div>
              <span className="text-xs font-semibold text-slate-800 hidden sm:inline">
                {user?.full_name || 'Clinician'}
              </span>
            </div>
            <button
              onClick={logout}
              className="p-2 rounded-xl text-slate-500 hover:text-rose-600 hover:bg-rose-50 border border-transparent hover:border-rose-200 transition-all cursor-pointer"
              title="Sign Out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Page Title Header */}
        <div className="space-y-1">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-50 border border-cyan-200 text-cyan-700 text-xs font-semibold">
            <span>Neuroimaging AI Suite</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
            Brain MRI Classifier
          </h1>
          <p className="text-sm text-slate-600 max-w-3xl">
            Upload a brain MRI image to classify the scan using the trained ConvNeXt deep-learning neural model and obtain class probabilities with AI-assisted clinical insights.
          </p>
        </div>

        {/* Error Banner */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 flex items-start gap-3 text-rose-900 text-sm animate-shake">
            <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
            <div className="flex-1 font-medium">{error}</div>
            <button onClick={() => setError('')} className="text-rose-400 hover:text-rose-700">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Upload Section */}
        {!result && (
          <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-6 sm:p-8 space-y-6">
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`relative border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center transition-all cursor-pointer ${
                dragActive
                  ? 'border-cyan-500 bg-cyan-50/50 scale-[0.99]'
                  : 'border-slate-300 hover:border-cyan-400 bg-slate-50/60 hover:bg-slate-50'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".jpg,.jpeg,.png"
                onChange={handleFileChange}
                className="hidden"
              />

              <div className="flex flex-col items-center gap-3.5">
                <div className="p-4 rounded-2xl bg-gradient-to-tr from-cyan-50 to-blue-50 border border-cyan-100 text-cyan-600 shadow-xs">
                  <UploadCloud className="w-8 h-8" />
                </div>
                <div>
                  <p className="text-base font-semibold text-slate-800">
                    Click to upload or drag & drop brain MRI scan
                  </p>
                  <p className="text-xs text-slate-500 mt-1">
                    Supports high-resolution neuroimaging slices (JPG, JPEG, PNG up to 15 MB)
                  </p>
                </div>
              </div>
            </div>

            {/* Selected File Details & Preview */}
            {file && (
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="flex items-center gap-3 min-w-0">
                  {filePreview ? (
                    <img
                      src={filePreview}
                      alt="MRI Preview"
                      className="w-12 h-12 object-cover rounded-lg border border-slate-200 shadow-xs"
                    />
                  ) : (
                    <div className="p-2.5 rounded-lg bg-cyan-100/80 text-cyan-700 shrink-0">
                      <FileCheck className="w-5 h-5" />
                    </div>
                  )}
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-slate-900 truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-slate-500">
                      {formatFileSize(file.size)} • Ready for ConvNeXt classification
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 w-full sm:w-auto">
                  <button
                    type="button"
                    onClick={removeFile}
                    disabled={isProcessing}
                    className="flex-1 sm:flex-initial px-3.5 py-2 text-xs font-semibold text-slate-600 hover:text-rose-600 hover:bg-rose-50 rounded-xl border border-slate-200 hover:border-rose-200 transition-colors"
                  >
                    Remove File
                  </button>
                  <button
                    type="button"
                    onClick={handleAnalyze}
                    disabled={isProcessing}
                    className="flex-1 sm:flex-initial px-6 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 rounded-xl shadow-md shadow-cyan-600/20 active:scale-[0.99] transition-all disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  >
                    {isProcessing ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        <span>Classifying...</span>
                      </>
                    ) : (
                      <>
                        <Brain className="w-4 h-4" />
                        <span>Analyze MRI</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}

            {/* Processing Multi-Stage Indicator */}
            {isProcessing && (
              <div className="p-6 rounded-2xl bg-[#0B132B] text-white space-y-4 animate-fade-in shadow-lg">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-cyan-400 uppercase tracking-wider flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
                    Neuroimaging Inference In Progress
                  </span>
                  <span className="text-slate-400 font-mono">ConvNeXt Tiny Active</span>
                </div>

                <div className="space-y-2">
                  <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full w-full animate-pulse" />
                  </div>
                  <p className="text-xs text-slate-300 font-medium text-center">
                    {processingStage}
                  </p>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 text-[11px] text-slate-400 border-t border-slate-800/80">
                  <div className="flex items-center gap-1.5 text-cyan-300">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Upload</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-cyan-300">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Preprocessing</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-cyan-300">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>ConvNeXt</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-cyan-300">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Gemini 3.5</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Results Presentation Section */}
        {result && (
          <div className="space-y-8 animate-fade-in">
            {/* Action Bar / Re-analyze */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl bg-white border border-slate-200 shadow-xs">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-emerald-50 text-emerald-600 border border-emerald-100">
                  <CheckCircle2 className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Classification Complete</h3>
                  <p className="text-xs text-slate-500 font-mono">
                    Report ID: {result.report_id} • ConvNeXt Tiny Neural Engine
                  </p>
                </div>
              </div>
              <button
                onClick={() => {
                  setResult(null);
                  removeFile();
                }}
                className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold text-slate-700 hover:text-cyan-700 bg-slate-100 hover:bg-slate-200/80 border border-slate-200 transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Analyze Another Scan</span>
              </button>
            </div>

            {/* Main Result Card Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column: Predicted Tumor Class & Confidence */}
              <div className="lg:col-span-2 p-6 sm:p-8 rounded-2xl bg-white border border-slate-200/90 shadow-sm space-y-6 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      Primary Classification Result
                    </span>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold border ${predictionMeta.badgeClass}`}>
                      {predictionKey === 'notumor' ? 'HEALTHY' : 'PATHOLOGY DETECTED'}
                    </span>
                  </div>

                  <div className="space-y-2">
                    <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                      {predictionMeta.label}
                    </h2>
                    <p className="text-sm text-slate-600 leading-relaxed">
                      {predictionMeta.description}
                    </p>
                  </div>
                </div>

                {/* Prominent Confidence Banner */}
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-cyan-100 text-cyan-700">
                      <Percent className="w-5 h-5" />
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                        Model Confidence
                      </p>
                      <p className="text-sm font-medium text-slate-700">
                        Posterior softmax probability
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-2xl sm:text-3xl font-extrabold text-slate-900 font-mono">
                      {result.confidence}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Right Column: Analyzed Scan Preview Thumbnail */}
              <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-sm flex flex-col items-center justify-center text-center space-y-3">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider self-start">
                  Analyzed Scan Slice
                </span>
                {filePreview ? (
                  <div className="w-full h-48 rounded-xl overflow-hidden bg-slate-950 border border-slate-800 flex items-center justify-center">
                    <img
                      src={filePreview}
                      alt="Analyzed Brain MRI"
                      className="w-full h-full object-contain"
                    />
                  </div>
                ) : (
                  <div className="w-full h-48 rounded-xl bg-slate-900 flex items-center justify-center text-slate-600">
                    <Brain className="w-12 h-12 text-slate-700" />
                  </div>
                )}
                <p className="text-[11px] text-slate-400 truncate max-w-xs">
                  {result.extracted_data?.original_filename || file?.name || 'mri_scan.jpg'}
                </p>
              </div>
            </div>

            {/* Class Probabilities Distribution */}
            <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-6 sm:p-8 space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                <div>
                  <h3 className="text-lg font-bold text-slate-900">
                    Class Probability Distribution
                  </h3>
                  <p className="text-xs text-slate-500">
                    Raw neural network output across all 4 target radiological classes.
                  </p>
                </div>
                <span className="text-xs font-mono text-slate-400">
                  ConvNeXt Softmax Output
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {probabilityKeys.map((cls) => {
                  const prob = probabilities[cls];
                  const info = CLASS_FORMAT_INFO[cls.toLowerCase()] || {
                    label: cls.toUpperCase(),
                    barColor: 'bg-cyan-500',
                  };
                  const isTop = cls.toLowerCase() === predictionKey;

                  return (
                    <div
                      key={cls}
                      className={`p-4 rounded-xl border transition-all ${
                        isTop
                          ? 'bg-cyan-50/40 border-cyan-300/80 shadow-xs'
                          : 'bg-slate-50 border-slate-200/80'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span className="text-sm font-bold text-slate-900">
                            {info.label}
                          </span>
                          {isTop && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-600 text-white uppercase tracking-wider">
                              Top Match
                            </span>
                          )}
                        </div>
                        <span className="text-sm font-mono font-bold text-slate-900">
                          {prob}%
                        </span>
                      </div>

                      {/* Percentage Bar */}
                      <div className="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all duration-500 ${info.barColor}`}
                          style={{ width: `${Math.min(Math.max(prob, 0), 100)}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* AI Explanation Card */}
            <div className="p-6 sm:p-8 rounded-2xl bg-gradient-to-br from-[#0B132B] via-[#0F172A] to-[#1E293B] text-white shadow-xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-cyan-500/15 border border-cyan-500/30 text-cyan-300">
                    <Sparkles className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-base sm:text-lg font-bold text-white tracking-tight">
                      AI-Assisted MRI Interpretation
                    </h3>
                    <p className="text-xs text-cyan-300/80 font-medium">
                      Gemini 3.5 Flash Educational Explanation
                    </p>
                  </div>
                </div>
                <span className="hidden sm:inline-block px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-500/30 text-cyan-300 text-xs font-semibold">
                  AI Generated
                </span>
              </div>

              <div className="pt-2 text-sm text-slate-200 leading-relaxed space-y-3 font-normal">
                {result.explanation ? (
                  result.explanation.split('\n\n').map((paragraph, idx) => (
                    <p key={idx}>{paragraph}</p>
                  ))
                ) : (
                  <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-400 text-xs flex items-center gap-3">
                    <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                    <span>
                      AI explanation is currently unavailable. The model prediction and confidence are still available above.
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Clinical Disclaimer Box */}
        <div className="p-5 rounded-2xl bg-amber-50/80 border border-amber-200/80 flex items-start gap-3.5 text-amber-900 text-xs sm:text-sm">
          <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="leading-relaxed">
            <strong className="font-semibold text-amber-950">Clinical Disclaimer:</strong>{' '}
            This tool provides educational/decision-support information and is not a substitute for professional medical diagnosis or treatment. All neuroimaging classifications and AI explanations must be verified by a licensed radiologist or neurologist.
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-200/80 bg-white py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-400">
          <p>© 2026 AI Medical Report Assistant • Neuroimaging Diagnostic Suite</p>
          <div className="flex items-center gap-4 text-slate-400">
            <span>HIPAA & GDPR Compliant</span>
            <span>•</span>
            <span>Deep Learning Convolutional Neural Models</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default BrainMRIPage;
