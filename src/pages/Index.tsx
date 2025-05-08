
import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import FileUpload from '../components/FileUpload';
import DependencyGraph from '../components/DependencyGraph';
import ConsoleLog from '../components/ConsoleLog';
import { useToast } from '../components/ui/use-toast';

// Sample HTML for dependency graph visualization
const sampleGraphHtml = `
<!DOCTYPE html>
<html>
<head>
  <title>Code Dependency Graph</title>
  <style>
    body { margin: 0; padding: 0; font-family: system-ui, sans-serif; }
    #graph { width: 100%; height: 100vh; background-color: #f8f9fa; }
    .node { fill: #0d9488; }
    .node:hover { fill: #f97316; }
    .link { stroke: #1a365d; stroke-opacity: 0.6; stroke-width: 1.5px; }
    .label { font-size: 12px; fill: #333; pointer-events: none; }
  </style>
  <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
  <div id="graph"></div>
  <script>
    // This would be replaced with actual dependency data from your Python backend
    const data = {
      nodes: [
        { id: "main.py", group: 1 },
        { id: "utils.py", group: 1 },
        { id: "database.py", group: 2 },
        { id: "models.py", group: 2 },
        { id: "api.py", group: 3 },
        { id: "config.py", group: 1 },
        { id: "auth.py", group: 3 }
      ],
      links: [
        { source: "main.py", target: "utils.py", value: 2 },
        { source: "main.py", target: "database.py", value: 2 },
        { source: "main.py", target: "api.py", value: 1 },
        { source: "database.py", target: "models.py", value: 3 },
        { source: "api.py", target: "models.py", value: 2 },
        { source: "api.py", target: "auth.py", value: 2 },
        { source: "main.py", target: "config.py", value: 1 }
      ]
    };

    // Create force simulation
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    const svg = d3.select("#graph")
      .append("svg")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; max-height: 100%;");

    const simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-400))
      .force("center", d3.forceCenter(width / 2, height / 2));

    // Create links
    const link = svg.append("g")
      .selectAll("line")
      .data(data.links)
      .join("line")
      .attr("class", "link")
      .attr("stroke-width", d => Math.sqrt(d.value));

    // Create nodes
    const node = svg.append("g")
      .selectAll("circle")
      .data(data.nodes)
      .join("circle")
      .attr("class", "node")
      .attr("r", 8)
      .call(drag(simulation));

    // Add labels to nodes
    const label = svg.append("g")
      .selectAll("text")
      .data(data.nodes)
      .join("text")
      .attr("class", "label")
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .attr("x", d => d.x)
      .attr("y", d => d.y + 20)
      .text(d => d.id);

    // Update positions on simulation tick
    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

      label
        .attr("x", d => d.x)
        .attr("y", d => d.y + 20);
    });

    // Enable dragging of nodes
    function drag(simulation) {
      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }
      
      function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }
      
      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }
      
      return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
    }
  </script>
</body>
</html>
`;

const Index: React.FC = () => {
  const { toast } = useToast();
  const [isProcessing, setIsProcessing] = useState(false);
  const [consoleOpen, setConsoleOpen] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [graphHtml, setGraphHtml] = useState<string | undefined>(undefined);

  // Function to handle file upload
  const handleFileUpload = (file: File, email: string) => {
    setIsProcessing(true);
    setConsoleOpen(true);
    setLogs([]);
    setGraphHtml(undefined);

    // Simulate adding logs over time
    const logMessages = [
      "Starting code documentation process...",
      "Extracting ZIP file contents...",
      "Scanning Python files...",
      "Building dependency graph...",
      "Analyzing import statements...",
      "Generating code structure map...",
      "Processing module: core.py",
      "Processing module: utils.py",
      "Processing module: models.py",
      "Processing module: database.py",
      "Processing module: api.py",
      "INFO: Found 5 Python modules with 12 interdependencies",
      "Generating HTML visualization...",
      "Documentation process completed",
      `Sending results to ${email}...`,
      "Email sent successfully! Check your inbox shortly."
    ];

    // Add logs with delays
    let i = 0;
    const intervalId = setInterval(() => {
      if (i < logMessages.length) {
        setLogs(prev => [...prev, logMessages[i]]);
        i++;

        // Show the graph after a few logs
        if (i === 7) {
          setGraphHtml(sampleGraphHtml);
        }
      } else {
        clearInterval(intervalId);
        setIsProcessing(false);
        toast({
          title: "Documentation Generated",
          description: `Your documentation has been sent to ${email}`,
        });
      }
    }, 1000);
  };

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
