
import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface DependencyGraphProps {
  graphHtml?: string;
  isProcessing: boolean;
}

const DependencyGraph: React.FC<DependencyGraphProps> = ({ graphHtml, isProcessing }) => {
  const [loaded, setLoaded] = useState(false);
  const [iframeHeight, setIframeHeight] = useState('600px');

  useEffect(() => {
    // Adjust iframe height based on window size
    const updateHeight = () => {
      const height = Math.max(window.innerHeight * 0.6, 600);
      setIframeHeight(`${height}px`);
    };

    window.addEventListener('resize', updateHeight);
    updateHeight();
    
    return () => window.removeEventListener('resize', updateHeight);
  }, []);

  return (
    <Card className="w-full h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold flex items-center">
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
            <circle cx="18" cy="5" r="3" />
            <circle cx="6" cy="12" r="3" />
            <circle cx="18" cy="19" r="3" />
            <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
            <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
          </svg>
          Dependency Graph Visualization
        </CardTitle>
      </CardHeader>
      <CardContent className="dependency-graph-container" style={{ height: iframeHeight }}>
        {graphHtml ? (
          <div className="w-full h-full animate-fade-in">
            <iframe
              srcDoc={graphHtml}
              className="w-full h-full border-none"
              sandbox="allow-scripts"
              onLoad={() => setLoaded(true)}
            />
          </div>
        ) : (
          <div className="w-full h-full flex flex-col items-center justify-center p-6 text-center">
            {isProcessing ? (
              <div className="flex flex-col items-center">
                <div className="relative w-16 h-16">
                  <div className="absolute top-0 left-0 w-16 h-16 rounded-full border-4 border-t-teal border-r-transparent border-b-transparent border-l-transparent animate-spin-slow" />
                  <div className="absolute top-2 left-2 w-12 h-12 rounded-full border-4 border-t-orange border-r-transparent border-b-transparent border-l-transparent animate-spin-slow" style={{ animationDirection: 'reverse' }} />
                </div>
                <p className="mt-4 text-sm text-muted-foreground">
                  Generating dependency graph...
                </p>
                <p className="mt-1 text-xs text-muted-foreground">
                  The visualization will appear here once processed
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  className="w-12 h-12 text-muted-foreground mx-auto"
                >
                  <circle cx="18" cy="5" r="3" />
                  <circle cx="6" cy="12" r="3" />
                  <circle cx="18" cy="19" r="3" />
                  <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
                  <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
                </svg>
                <h3 className="text-lg font-medium">No Graph Available</h3>
                <p className="text-sm text-muted-foreground max-w-sm">
                  Upload your codebase ZIP file to generate a dependency graph visualization
                </p>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default DependencyGraph;
