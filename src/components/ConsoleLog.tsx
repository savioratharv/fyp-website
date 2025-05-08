
import React, { useEffect, useRef, useState } from 'react';
import { ScrollArea } from './ui/scroll-area';
import { Button } from './ui/button';

interface ConsoleLogProps {
  logs: string[];
  isOpen: boolean;
  onToggle: () => void;
}

const ConsoleLog: React.FC<ConsoleLogProps> = ({ logs, isOpen, onToggle }) => {
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const [autoScroll, setAutoScroll] = useState(true);

  useEffect(() => {
    if (autoScroll && scrollAreaRef.current && isOpen) {
      const scrollContainer = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }, [logs, isOpen, autoScroll]);

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    if (scrollAreaRef.current) {
      const scrollContainer = e.currentTarget;
      const isAtBottom = Math.abs(
        scrollContainer.scrollHeight - scrollContainer.clientHeight - scrollContainer.scrollTop
      ) < 10;
      setAutoScroll(isAtBottom);
    }
  };

  const renderLogLine = (line: string, index: number) => {
    // Detect if the log line is an error message
    const isError = line.toLowerCase().includes('error') || line.toLowerCase().includes('exception');
    // Detect if the log line is a warning
    const isWarning = line.toLowerCase().includes('warning') || line.toLowerCase().includes('warn');
    // Detect if the log line is info
    const isInfo = line.toLowerCase().includes('info');
    
    let colorClass = "text-gray-200";
    if (isError) colorClass = "text-red-400";
    else if (isWarning) colorClass = "text-yellow-400";
    else if (isInfo) colorClass = "text-blue-400";
    
    return (
      <div key={index} className={`py-1 font-mono text-xs ${colorClass}`}>
        {line}
      </div>
    );
  };

  return (
    <div className={`console-transition fixed bottom-0 left-0 right-0 bg-navy text-white ${isOpen ? 'h-64' : 'h-10'} shadow-lg`}>
      <div 
        className="flex items-center justify-between px-4 py-2 bg-navy text-white cursor-pointer"
        onClick={onToggle}
      >
        <div className="flex items-center">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2" 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            className="w-4 h-4 mr-2"
          >
            <polyline points="16 18 22 12 16 6" />
            <polyline points="8 6 2 12 8 18" />
          </svg>
          <span className="text-sm font-medium">Console Logs</span>
          {logs.length > 0 && (
            <span className="ml-2 px-2 py-0.5 text-xs bg-teal/20 rounded-full">
              {logs.length}
            </span>
          )}
        </div>
        <div className="flex items-center">
          <Button 
            variant="ghost" 
            size="sm" 
            className="h-6 px-2 text-xs hover:bg-white/10"
            onClick={(e) => {
              e.stopPropagation(); 
              setAutoScroll(true);
            }}
          >
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              className="w-3 h-3 mr-1"
            >
              <path d="m19 14-7 7-7-7" />
              <path d="M12 3v18" />
            </svg>
            Scroll to Bottom
          </Button>
          <Button 
            variant="ghost" 
            size="sm" 
            className="h-6 px-2 text-xs hover:bg-white/10 ml-1"
            onClick={(e) => {
              e.stopPropagation();
              if (isOpen) {
                onToggle();
              }
            }}
          >
            {isOpen ? (
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                className="w-3 h-3"
              >
                <path d="m18 15-6-6-6 6" />
              </svg>
            ) : (
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                className="w-3 h-3"
              >
                <path d="m6 9 6 6 6-6" />
              </svg>
            )}
          </Button>
        </div>
      </div>
      
      {isOpen && (
        <div ref={scrollAreaRef} className="h-[calc(100%-32px)]">
          <ScrollArea className="h-full p-4" onScroll={handleScroll}>
            {logs.length > 0 ? (
              logs.map((log, index) => renderLogLine(log, index))
            ) : (
              <div className="flex flex-col items-center justify-center h-full text-center p-4">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  className="w-6 h-6 text-gray-400"
                >
                  <path d="M12 20h9" />
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
                </svg>
                <p className="mt-2 text-sm text-gray-400">No logs available yet</p>
              </div>
            )}
          </ScrollArea>
        </div>
      )}
    </div>
  );
};

export default ConsoleLog;
