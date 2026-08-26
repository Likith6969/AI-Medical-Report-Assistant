import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Activity, 
  FileText, 
  Brain, 
  LogOut, 
  User as UserIcon, 
  CheckCircle2, 
  ArrowRight, 
  Sparkles, 
  ShieldAlert, 
  Clock,
  ChevronRight
} from 'lucide-react';

const DashboardPage = () => {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
      {/* Top Clinical Navigation Bar */}
      <header className="sticky top-0 z-30 bg-white/85 backdrop-blur-md border-b border-slate-200/80 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          {/* Brand Logo & Name */}
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 text-white shadow-md shadow-cyan-600/20">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-slate-900 text-base sm:text-lg tracking-tight block leading-tight">
                AI Medical Report Assistant
              </span>
              <span className="text-[11px] text-slate-500 font-medium tracking-wide uppercase">
                Clinical Diagnostic Suite
              </span>
            </div>
          </div>

          {/* User Profile & Logout Controls */}
          <div className="flex items-center gap-3 sm:gap-4">
            {/* User Profile Pill */}
            <div className="flex items-center gap-3 pl-3 pr-4 py-1.5 rounded-full bg-slate-100/90 border border-slate-200/70">
              <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-600 text-white flex items-center justify-center text-xs font-bold shadow-xs">
                {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
              </div>
              <div className="hidden sm:block text-left">
                <p className="text-xs font-semibold text-slate-900 leading-tight">
                  {user?.full_name || 'Clinician'}
                </p>
                <p className="text-[11px] text-slate-500 font-normal leading-tight">
                  {user?.email || 'Authenticated User'}
                </p>
              </div>
            </div>

            {/* Logout Button */}
            <button
              onClick={logout}
              className="p-2 rounded-xl text-slate-500 hover:text-rose-600 hover:bg-rose-50 border border-transparent hover:border-rose-200 transition-all cursor-pointer"
              title="Sign Out"
              aria-label="Sign Out"
            >
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Clinical Dashboard Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10 space-y-8">
        {/* Welcome Banner */}
        <div className="relative overflow-hidden p-6 sm:p-8 rounded-2xl bg-gradient-to-r from-slate-900 via-[#0B132B] to-slate-900 text-white shadow-xl shadow-slate-900/10 border border-slate-800">
          {/* Subtle Background Glows */}
          <div className="absolute -top-16 -right-16 w-64 h-64 bg-cyan-500/15 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute -bottom-16 left-1/3 w-64 h-64 bg-blue-600/15 rounded-full blur-3xl pointer-events-none" />

          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-500/30 text-cyan-300 text-xs font-semibold">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span>AI Diagnostic Engine Online</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
                Welcome back, {user?.full_name || 'Clinician'}
              </h1>
              <p className="text-sm text-slate-300 max-w-2xl leading-relaxed">
                Access advanced multimodal diagnostic tools to extract CBC blood parameters and analyze brain MRI scans with deep neural models.
              </p>
            </div>

            {/* Quick Stats or Metadata */}
            <div className="flex items-center gap-4 bg-slate-800/60 backdrop-blur-md p-3.5 rounded-xl border border-slate-700/60 shrink-0">
              <div className="flex items-center gap-2 text-xs text-slate-300">
                <Clock className="w-4 h-4 text-cyan-400" />
                <span>Active Session</span>
              </div>
              <div className="h-4 w-px bg-slate-700" />
              <div className="flex items-center gap-2 text-xs text-emerald-400 font-medium">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Ready</span>
              </div>
            </div>
          </div>
        </div>

        {/* Feature Cards Section Header */}
        <div>
          <h2 className="text-lg font-bold text-slate-900 tracking-tight">
            Diagnostic Modalities
          </h2>
          <p className="text-sm text-slate-500">
            Select a diagnostic tool to begin automated report parsing or neuroimaging classification.
          </p>
        </div>

        {/* Two Large Feature Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
          {/* Card 1: Blood Report Analyzer */}
          <div className="group relative flex flex-col justify-between p-6 sm:p-8 rounded-2xl bg-white border border-slate-200/90 shadow-sm hover:shadow-xl hover:border-cyan-200 transition-all duration-300">
            <div className="space-y-5">
              {/* Header Icon + Badge */}
              <div className="flex items-center justify-between">
                <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-100 text-rose-600 group-hover:scale-105 transition-transform duration-200 shadow-xs">
                  <FileText className="w-7 h-7" />
                </div>
                <span className="text-xs font-semibold px-3 py-1 rounded-full bg-rose-50 text-rose-700 border border-rose-200/60">
                  Hematology
                </span>
              </div>

              {/* Title & Subtitle */}
              <div>
                <h3 className="text-xl font-bold text-slate-900 group-hover:text-cyan-700 transition-colors">
                  Blood Report Analyzer
                </h3>
                <p className="text-xs text-slate-600 font-medium mt-0.5">
                  Complete Blood Count (CBC) Parser & Clinical Summary
                </p>
                <p className="text-sm text-slate-600 mt-2.5 leading-relaxed">
                  Upload a blood report image or document and extract 21 CBC parameters, abnormal values, reference ranges, and AI-assisted clinical interpretation.
                </p>
              </div>

              {/* Capability Checklist */}
              <div className="space-y-2.5 pt-2 border-t border-slate-100">
                <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Key Capabilities
                </p>
                <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-700">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                    <span>21 CBC Parameter Extraction</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                    <span>Unit & Scale Normalization</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                    <span>Out-of-Range High/Low Flags</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                    <span>AI-Assisted Educational Summary</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Action Button */}
            <div className="pt-6 mt-6 border-t border-slate-100">
              <Link
                to="/blood-report"
                className="w-full flex items-center justify-center gap-2 py-3 px-5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-sm font-semibold shadow-md shadow-cyan-600/20 group-hover:shadow-lg group-hover:shadow-cyan-600/30 transition-all cursor-pointer"
              >
                <span>Get Started</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>

          {/* Card 2: Brain MRI Classifier */}
          <div className="group relative flex flex-col justify-between p-6 sm:p-8 rounded-2xl bg-white border border-slate-200/90 shadow-sm hover:shadow-xl hover:border-cyan-200 transition-all duration-300">
            <div className="space-y-5">
              {/* Header Icon + Badge */}
              <div className="flex items-center justify-between">
                <div className="p-3.5 rounded-2xl bg-cyan-50 border border-cyan-100 text-cyan-600 group-hover:scale-105 transition-transform duration-200 shadow-xs">
                  <Brain className="w-7 h-7" />
                </div>
                <span className="text-xs font-semibold px-3 py-1 rounded-full bg-cyan-50 text-cyan-700 border border-cyan-200/60">
                  Neuroimaging
                </span>
              </div>

              {/* Title & Subtitle */}
              <div>
                <h3 className="text-xl font-bold text-slate-900 group-hover:text-cyan-700 transition-colors">
                  Brain MRI Classifier
                </h3>
                <p className="text-xs text-slate-600 font-medium mt-0.5">
                  ConvNeXt Deep Learning Tumor Classification
                </p>
                <p className="text-sm text-slate-600 mt-2.5 leading-relaxed">
                  Upload a brain MRI image and receive the predicted tumor class, confidence, class probabilities, and AI-assisted explanation.
                </p>
              </div>

              {/* Capability Checklist */}
              <div className="space-y-2.5 pt-2 border-t border-slate-100">
                <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Key Capabilities
                </p>
                <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-700">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                    <span>4-Class Tumor Detection</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                    <span>ConvNeXt Neural Model</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                    <span>Class Probability Vectors</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                    <span>AI Radiological Explanation</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Action Button */}
            <div className="pt-6 mt-6 border-t border-slate-100">
              <Link
                to="/brain-mri"
                className="w-full flex items-center justify-center gap-2 py-3 px-5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-sm font-semibold shadow-md shadow-cyan-600/20 group-hover:shadow-lg group-hover:shadow-cyan-600/30 transition-all cursor-pointer"
              >
                <span>Get Started</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>
        </div>

        {/* Clinical Disclaimer Banner */}
        <div className="p-4 sm:p-5 rounded-2xl bg-amber-50/80 border border-amber-200/80 flex items-start gap-3.5 text-amber-900 text-xs sm:text-sm">
          <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="leading-relaxed">
            <strong className="font-semibold text-amber-950">Clinical Disclaimer:</strong>{' '}
            AI Medical Report Assistant is designed for clinical supportive workflow and educational purposes only. Automated CBC parameter extractions and ConvNeXt MRI predictions are non-diagnostic and must always be verified by a licensed medical practitioner.
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-200/80 bg-white py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-400">
          <p>© 2026 AI Medical Report Assistant. All rights reserved.</p>
          <div className="flex items-center gap-4 text-slate-400">
            <span>Clinical Intelligence Platform</span>
            <span>•</span>
            <span>HIPAA Compliant</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default DashboardPage;
