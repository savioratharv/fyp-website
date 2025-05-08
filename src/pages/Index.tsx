import React, { useState, useEffect, useRef } from 'react';
import Header from '../components/Header';
import FileUpload from '../components/FileUpload';
import DependencyGraph from '../components/DependencyGraph';
import ConsoleLog from '../components/ConsoleLog';
import { useToast } from '../components/ui/use-toast';

const Index: React.FC = () => {
  const { toast } = useToast();
  const [isProcessing, setIsProcessing] = useState(false);
  const [consoleOpen, setConsoleOpen] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [graphHtml, setGraphHtml] = useState<string | undefined>(undefined);
  const logsInterval = useRef<number | null>(null);
  const graphInterval = useRef<number | null>(null);

  // Function to handle file upload
  const handleFileUpload = async (file: File, email: string) => {
    setIsProcessing(true);
    setConsoleOpen(true);
    setLogs([]);
    setGraphHtml(undefined);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('email', email);
      await fetch('/api/upload', { method: 'POST', body: formData });
      // Start polling logs
      const fetchLogs = async () => {
        try {
          const res = await fetch('/api/logs');
          if (!res.ok) return;  // skip if server error
          const data = await res.json();
          setLogs(data.logs);
          setIsProcessing(data.processing);
          if (!data.processing) {
            if (logsInterval.current) clearInterval(logsInterval.current);
            if (graphInterval.current) clearInterval(graphInterval.current);
            toast({ title: 'Documentation Generated', description: `Check your email for results.` });
          }
        } catch (err) {
          // network or parse error, ignore and retry
        }
      };
      logsInterval.current = window.setInterval(fetchLogs, 1000);
      // Start polling graph HTML
      const fetchGraph = async () => {
        try {
          const res = await fetch('/api/graph');
          if (!res.ok) return;
          const html = await res.text();
          setGraphHtml(html);
        } catch (err) {
          // ignore and retry
        }
      };
      graphInterval.current = window.setInterval(fetchGraph, 1000);
    } catch (err) {
      console.error(err);
      toast({ title: 'Upload Failed', description: 'Please try again.' });
      setIsProcessing(false);
    }
  };

  // Clear intervals on unmount
  useEffect(() => () => {
    if (logsInterval.current) clearInterval(logsInterval.current);
    if (graphInterval.current) clearInterval(graphInterval.current);
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <main className="flex-grow bg-gray-50 pb-20">
        <div className="container mx-auto py-8 px-4 md:px-6">
          <div className="mb-8 text-center">
            <h2 className="text-3xl font-bold text-navy mb-4">
              Code Documentation Generator
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Upload your Python codebase as a ZIP file to generate comprehensive documentation
              with dependency visualizations, code analysis, and more.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div className="flex flex-col space-y-6">
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-xl font-semibold mb-4 flex items-center">
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    className="w-5 h-5 mr-2 text-teal"
                  >
                    <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
                  </svg>
                  How It Works
                </h3>
                <ol className="space-y-4 text-gray-600">
                  <li className="flex">
                    <span className="bg-navy text-white rounded-full w-6 h-6 flex items-center justify-center mr-3 flex-shrink-0">1</span>
                    <span>Upload your Python codebase as a ZIP file and provide your email address.</span>
                  </li>
                  <li className="flex">
                    <span className="bg-navy text-white rounded-full w-6 h-6 flex items-center justify-center mr-3 flex-shrink-0">2</span>
                    <span>Our system analyzes your code, extracting dependencies and structure.</span>
                  </li>
                  <li className="flex">
                    <span className="bg-navy text-white rounded-full w-6 h-6 flex items-center justify-center mr-3 flex-shrink-0">3</span>
                    <span>Watch the dependency graph visualization generate in real-time.</span>
                  </li>
                  <li className="flex">
                    <span className="bg-navy text-white rounded-full w-6 h-6 flex items-center justify-center mr-3 flex-shrink-0">4</span>
                    <span>Receive comprehensive documentation via email when processing completes.</span>
                  </li>
                </ol>
              </div>
              
              <FileUpload onFileUpload={handleFileUpload} />
            </div>
            
            <div>
              <DependencyGraph graphHtml={graphHtml} isProcessing={isProcessing} />
            </div>
          </div>
        </div>
      </main>
      
      <ConsoleLog 
        logs={logs} 
        isOpen={consoleOpen} 
        onToggle={() => setConsoleOpen(!consoleOpen)}
      />
    </div>
  );
};

export default Index;
