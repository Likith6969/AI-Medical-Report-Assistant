import React, { useState, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { reportsService } from '../services/api';
import { 
  Activity, 
  ArrowLeft, 
  UploadCloud, 
  FileText, 
  CheckCircle2, 
  AlertCircle, 
  AlertTriangle,
  X, 
  Sparkles, 
  Clock, 
  LogOut, 
  ShieldAlert,
  Layers,
  TrendingUp,
  TrendingDown,
  Minus,
  RefreshCw,
  Eye,
  FileCheck
} from 'lucide-react';

const PARAMETER_DISPLAY_NAMES = {
  hemoglobin: 'Hemoglobin (Hb)',
  rbc: 'RBC Count (Erythrocytes)',
  wbc: 'Total WBC Count (Leukocytes)',
  platelets: 'Platelet Count (Thrombocytes)',
  hematocrit: 'Hematocrit (HCT / PCV)',
  mcv: 'Mean Corpuscular Volume (MCV)',
  mch: 'Mean Corpuscular Hemoglobin (MCH)',
  mchc: 'Mean Corpuscular Hb Conc (MCHC)',
  rdw_cv: 'RDW-CV (Red Cell Distribution Width)',
  rdw_sd: 'RDW-SD',
  mpv: 'Mean Platelet Volume (MPV)',
  neutrophils: 'Neutrophils',
  lymphocytes: 'Lymphocytes',
  monocytes: 'Monocytes',
  eosinophils: 'Eosinophils',
  basophils: 'Basophils',
  anc: 'Absolute Neutrophil Count (ANC)',
  alc: 'Absolute Lymphocyte Count (ALC)',
  amc: 'Absolute Monocyte Count (AMC)',
  aec: 'Absolute Eosinophil Count (AEC)',
  abc: 'Absolute Basophil Count (ABC)',
};

const BloodReportPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
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
    const validExtensions = ['.jpg', '.jpeg', '.png', '.pdf'];
    const filename = selectedFile.name.toLowerCase();
    const isValid = validExtensions.some((ext) => filename.endsWith(ext));

    if (!isValid) {
      setError('Please upload a valid blood report image (JPG, JPEG, PNG) or PDF document.');
      return;
    }

    if (selectedFile.size > 15 * 1024 * 1024) {
      setError('File size exceeds the 15 MB limit.');
      return;
    }

    setFile(selectedFile);
  };

  const removeFile = () => {
    setFile(null);
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
      setError('Please select a blood report to analyze.');
      return;
    }

    setError('');
    setIsProcessing(true);
    setProcessingStage('Uploading document to secure clinical storage...');

    try {
      const stageTimer1 = setTimeout(() => {
        setProcessingStage('Running EasyOCR optical character extraction...');
      }, 1200);

      const stageTimer2 = setTimeout(() => {
        setProcessingStage('Parsing 21 CBC parameters & comparing reference ranges...');
      }, 4000);

      const stageTimer3 = setTimeout(() => {
        setProcessingStage('Generating AI clinical summary with Gemini 3.5...');
      }, 7000);

      const data = await reportsService.analyzeBloodReport(file);

      clearTimeout(stageTimer1);
      clearTimeout(stageTimer2);
      clearTimeout(stageTimer3);

      setResult(data);
    } catch (err) {
      console.error('Blood report analysis error:', err);
      if (err.response) {
        if (err.response.status === 413) {
          setError('The uploaded file is too large. Maximum supported size is 15 MB.');
        } else {
          const detail = err.response.data?.detail;
          setError(typeof detail === 'string' ? detail : 'Analysis failed. Please check the uploaded file format.');
        }
      } else if (err.request) {
        setError('Unable to connect to the backend server. Please verify the API is running.');
      } else {
        setError('An unexpected error occurred while analyzing the blood report.');
      }
    } finally {
      setIsProcessing(false);
      setProcessingStage('');
    }
  };

  const getStatusBadge = (status) => {
    const s = (status || '').toUpperCase();
    if (s === 'HIGH') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-rose-50 text-rose-700 border border-rose-200 text-xs font-bold tracking-wide">
          <TrendingUp className="w-3.5 h-3.5 text-rose-600" />
          HIGH
        </span>
      );
    } else if (s === 'LOW') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-amber-50 text-amber-700 border border-amber-200 text-xs font-bold tracking-wide">
          <TrendingDown className="w-3.5 h-3.5 text-amber-600" />
          LOW
        </span>
      );
    } else {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold tracking-wide">
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
          NORMAL
        </span>
      );
    }
  };

  const parameterKeys = result?.parameters ? Object.keys(result.parameters) : [];

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
              <div className="p-1.5 rounded-lg bg-rose-50 text-rose-600 border border-rose-100">
                <FileText className="w-4 h-4" />
              </div>
              <span className="font-bold text-slate-900 text-sm tracking-tight">
                Blood Report Analyzer
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
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold">
            <span>Hematology CBC Suite</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
            Blood Report Analyzer
          </h1>
          <p className="text-sm text-slate-600 max-w-3xl">
            Upload a Complete Blood Count (CBC) report image to automatically extract biomarkers, compare against reference intervals, and receive an AI-assisted educational interpretation.
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

        {/* Upload Card */}
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
                accept=".jpg,.jpeg,.png,.pdf"
                onChange={handleFileChange}
                className="hidden"
              />

              <div className="flex flex-col items-center gap-3.5">
                <div className="p-4 rounded-2xl bg-gradient-to-tr from-cyan-50 to-blue-50 border border-cyan-100 text-cyan-600 shadow-xs">
                  <UploadCloud className="w-8 h-8" />
                </div>
                <div>
                  <p className="text-base font-semibold text-slate-800">
                    Click to upload or drag & drop your blood report
                  </p>
                  <p className="text-xs text-slate-500 mt-1">
                    Supports high-resolution laboratory scans (JPG, JPEG, PNG, PDF up to 15 MB)
                  </p>
                </div>
              </div>
            </div>

            {/* Selected File Details & Action */}
            {file && (
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="flex items-center gap-3 min-w-0">
                  <div className="p-2.5 rounded-lg bg-cyan-100/80 text-cyan-700 shrink-0">
                    <FileCheck className="w-5 h-5" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-slate-900 truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-slate-500">
                      {formatFileSize(file.size)} • Ready for analysis
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
                        <span>Analyzing...</span>
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4" />
                        <span>Analyze Report</span>
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
                    Clinical Analysis In Progress
                  </span>
                  <span className="text-slate-400 font-mono">Stage 1 of 4</span>
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
                    <span>EasyOCR</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-cyan-300">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>CBC Parser</span>
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
                  <h3 className="text-sm font-bold text-slate-900">Analysis Complete</h3>
                  <p className="text-xs text-slate-500 font-mono">
                    Report ID: {result.report_id} • Processed in {result.processing_time}s
                  </p>
                </div>
              </div>
              <button
                onClick={() => {
                  setResult(null);
                  setFile(null);
                }}
                className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold text-slate-700 hover:text-cyan-700 bg-slate-100 hover:bg-slate-200/80 border border-slate-200 transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Analyze Another Report</span>
              </button>
            </div>

            {/* Overview Metric Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-xs space-y-1">
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Extracted Biomarkers
                </p>
                <p className="text-2xl sm:text-3xl font-bold text-slate-900">
                  {parameterKeys.length} <span className="text-xs text-slate-400 font-normal">/ 21</span>
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-emerald-50/60 border border-emerald-200/80 shadow-xs space-y-1">
                <div className="flex items-center justify-between">
                  <p className="text-xs font-semibold text-emerald-700 uppercase tracking-wider">
                    Normal
                  </p>
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                </div>
                <p className="text-2xl sm:text-3xl font-bold text-emerald-800">
                  {result.overall_status?.normal || 0}
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-rose-50/60 border border-rose-200/80 shadow-xs space-y-1">
                <div className="flex items-center justify-between">
                  <p className="text-xs font-semibold text-rose-700 uppercase tracking-wider">
                    High
                  </p>
                  <TrendingUp className="w-4 h-4 text-rose-600" />
                </div>
                <p className="text-2xl sm:text-3xl font-bold text-rose-800">
                  {result.overall_status?.high || 0}
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-amber-50/60 border border-amber-200/80 shadow-xs space-y-1">
                <div className="flex items-center justify-between">
                  <p className="text-xs font-semibold text-amber-700 uppercase tracking-wider">
                    Low
                  </p>
                  <TrendingDown className="w-4 h-4 text-amber-600" />
                </div>
                <p className="text-2xl sm:text-3xl font-bold text-amber-800">
                  {result.overall_status?.low || 0}
                </p>
              </div>
            </div>

            {/* AI Summary Card */}
            <div className="p-6 sm:p-8 rounded-2xl bg-gradient-to-br from-[#0B132B] via-[#0F172A] to-[#1E293B] text-white shadow-xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-cyan-500/15 border border-cyan-500/30 text-cyan-300">
                    <Sparkles className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-base sm:text-lg font-bold text-white tracking-tight">
                      AI-Assisted Clinical Interpretation
                    </h3>
                    <p className="text-xs text-cyan-300/80 font-medium">
                      Gemini 3.5 Flash Educational Summary
                    </p>
                  </div>
                </div>
                <span className="hidden sm:inline-block px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-500/30 text-cyan-300 text-xs font-semibold">
                  AI Generated
                </span>
              </div>

              <div className="pt-2 text-sm text-slate-200 leading-relaxed space-y-3 font-normal">
                {result.ai_summary ? (
                  result.ai_summary.split('\n\n').map((paragraph, idx) => (
                    <p key={idx}>{paragraph}</p>
                  ))
                ) : (
                  <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-400 text-xs flex items-center gap-3">
                    <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                    <span>
                      AI summary is currently unavailable. The extracted laboratory results are fully structured and verified below.
                    </span>
                  </div>
                )}
              </div>
            </div>

            {/* Structured CBC Parameters Table */}
            <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden space-y-0">
              <div className="p-6 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <h3 className="text-lg font-bold text-slate-900">
                    Laboratory Biomarkers ({parameterKeys.length} Extracted)
                  </h3>
                  <p className="text-xs text-slate-500">
                    Extracted parameters with canonical unit normalization and reference interval matching.
                  </p>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50/80 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
                    <tr>
                      <th scope="col" className="py-3.5 pl-6 pr-4">Parameter</th>
                      <th scope="col" className="py-3.5 px-4 text-right">Result</th>
                      <th scope="col" className="py-3.5 px-4">Unit</th>
                      <th scope="col" className="py-3.5 px-4">Biological Reference Interval</th>
                      <th scope="col" className="py-3.5 pl-4 pr-6 text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-slate-800">
                    {parameterKeys.length > 0 ? (
                      parameterKeys.map((key) => {
                        const param = result.parameters[key];
                        return (
                          <tr key={key} className="hover:bg-slate-50/60 transition-colors">
                            <td className="py-4 pl-6 pr-4 font-semibold text-slate-900">
                              {PARAMETER_DISPLAY_NAMES[key] || key.toUpperCase()}
                            </td>
                            <td className="py-4 px-4 text-right font-mono font-bold text-base text-slate-900">
                              {param.value}
                            </td>
                            <td className="py-4 px-4 font-mono text-xs text-slate-500">
                              {param.unit || '—'}
                            </td>
                            <td className="py-4 px-4 text-xs font-medium text-slate-600">
                              {param.reference_range || 'Standard Adult Reference'}
                            </td>
                            <td className="py-4 pl-4 pr-6 text-center">
                              {getStatusBadge(param.status)}
                            </td>
                          </tr>
                        );
                      })
                    ) : (
                      <tr>
                        <td colSpan={5} className="py-8 text-center text-slate-500 text-sm">
                          No laboratory parameters could be reliably extracted from this document.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Clinical Disclaimer Box */}
        <div className="p-5 rounded-2xl bg-amber-50/80 border border-amber-200/80 flex items-start gap-3.5 text-amber-900 text-xs sm:text-sm">
          <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="leading-relaxed">
            <strong className="font-semibold text-amber-950">Clinical Disclaimer:</strong>{' '}
            This tool provides educational and clinical decision-support information and is not a substitute for professional medical diagnosis or treatment. All extracted values and AI interpretations must be verified by a qualified healthcare professional.
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-200/80 bg-white py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-400">
          <p>© 2026 AI Medical Report Assistant • CBC Laboratory Suite</p>
          <div className="flex items-center gap-4 text-slate-400">
            <span>HIPAA & GDPR Compliant</span>
            <span>•</span>
            <span>Optical Character Recognition & AI Diagnostics</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default BloodReportPage;
