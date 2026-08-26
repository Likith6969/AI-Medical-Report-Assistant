import React from 'react';
import { Activity, Brain, ShieldCheck, Sparkles, FileText, CheckCircle2 } from 'lucide-react';

const AuthHero = () => {
  return (
    <div className="relative hidden lg:flex flex-col justify-between w-1/2 p-12 bg-[#0B132B] text-white overflow-hidden select-none">
      {/* Dynamic Background Glows & Grids */}
      <div className="absolute -top-24 -right-24 w-96 h-96 bg-cyan-500/15 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-blue-600/15 rounded-full blur-3xl pointer-events-none" />
      
      {/* Decorative Grid Overlay */}
      <div 
        className="absolute inset-0 opacity-[0.03] pointer-events-none" 
        style={{ 
          backgroundImage: 'radial-gradient(#38bdf8 1px, transparent 1px)', 
          backgroundSize: '24px 24px' 
        }} 
      />

      {/* Top Header Badge */}
      <div className="relative z-10 flex items-center justify-between">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-950/70 border border-cyan-500/30 text-cyan-300 text-xs font-semibold tracking-wide">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span>Multimodal Clinical Intelligence</span>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-slate-400">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>Secure Clinical Node</span>
        </div>
      </div>

      {/* Centerpiece Visuals / Feature Cards */}
      <div className="relative z-10 my-auto space-y-6">
        <div className="space-y-3">
          <h2 className="text-3xl xl:text-4xl font-bold tracking-tight text-white leading-tight">
            Next-Generation <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-sky-300 to-blue-400">
              Medical Diagnostics
            </span>
          </h2>
          <p className="text-sm text-slate-300 max-w-md leading-relaxed">
            Automating CBC report parsing with clinical precision and assisting brain tumor classification with deep learning neural networks.
          </p>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid gap-3.5 pt-2">
          {/* Blood Report Card */}
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800/80 backdrop-blur-md hover:border-slate-700/80 transition-all duration-200">
            <div className="flex items-start gap-3.5">
              <div className="p-2.5 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 shrink-0">
                <FileText className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <h4 className="text-sm font-semibold text-white">CBC Hematology Parser</h4>
                  <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    21 Parameters
                  </span>
                </div>
                <p className="text-xs text-slate-400 line-clamp-2">
                  Multi-stage OCR extraction, automatic unit scaling, and out-of-range flag detection.
                </p>
              </div>
            </div>
          </div>

          {/* Brain MRI Card */}
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800/80 backdrop-blur-md hover:border-slate-700/80 transition-all duration-200">
            <div className="flex items-start gap-3.5">
              <div className="p-2.5 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 shrink-0">
                <Brain className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <h4 className="text-sm font-semibold text-white">ConvNeXt MRI Classifier</h4>
                  <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                    4-Class Neural Model
                  </span>
                </div>
                <p className="text-xs text-slate-400 line-clamp-2">
                  Classifies Glioma, Meningioma, Pituitary, or Healthy scans with calibrated probability vectors.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Highlights Row */}
        <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-xs text-slate-400">
          <div className="flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
            <span>Automated Normalization</span>
          </div>
          <div className="flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
            <span>Standardized Reference Ranges</span>
          </div>
          <div className="flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
            <span>AI Clinical Summaries</span>
          </div>
        </div>
      </div>

      {/* Bottom Footer Note */}
      <div className="relative z-10 flex items-center justify-between text-xs text-slate-400 pt-6">
        <p>© 2026 AI Medical Report Assistant</p>
        <p className="text-[11px] text-slate-400">Clinical Decision Support System</p>
      </div>
    </div>
  );
};

export default AuthHero;
