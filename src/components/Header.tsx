
import React from 'react';
import { cn } from '../lib/utils';

interface HeaderProps {
  className?: string;
}

const Header: React.FC<HeaderProps> = ({ className }) => {
  return (
    <header className={cn("w-full bg-navy text-white py-4 px-6", className)}>
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="rounded-md bg-teal p-2">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              className="w-6 h-6 text-white"
            >
              <circle cx="12" cy="12" r="10" />
              <path d="M12 16v-4" />
              <path d="M12 8h.01" />
            </svg>
          </div>
          <div>
            <h1 className="text-xl font-semibold">CodeScribe</h1>
            <p className="text-xs text-gray-300">Automated Documentation Generator</p>
          </div>
        </div>
        <nav>
          <ul className="flex space-x-6">
            <li>
              <a href="#" className="text-sm hover:text-teal transition-colors">
                Documentation
              </a>
            </li>
            <li>
              <a href="#" className="text-sm hover:text-teal transition-colors">
                About
              </a>
            </li>
            <li>
              <a href="#" className="text-sm hover:text-teal transition-colors">
                Contact
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
