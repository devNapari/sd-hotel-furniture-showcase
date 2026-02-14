
import React, { useState, useEffect } from 'react';
import { NAV_LINKS } from '../constants';

const Header: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-white shadow-md text-gray-800' : 'bg-transparent text-white'}`}>
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        <a href="#" className="text-2xl font-bold tracking-wider">
          <span className={isScrolled ? 'text-gray-800' : 'text-white'}>SD</span>
          <span className="text-amber-500">HOTEL</span>
        </a>
        
        <nav className="hidden md:flex space-x-8 items-center">
          {NAV_LINKS.map((link) => (
            <a key={link.label} href={link.href} className="text-sm uppercase font-medium hover:text-amber-500 transition-colors">
              {link.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center">
            <button className="hidden md:block p-2 rounded-full hover:bg-gray-700/50 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </button>
            <button onClick={() => setIsMenuOpen(!isMenuOpen)} className="md:hidden p-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
            </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <div className={`md:hidden ${isMenuOpen ? 'block' : 'hidden'} ${isScrolled ? 'bg-white' : 'bg-gray-900/90'} backdrop-blur-sm`}>
        <nav className="flex flex-col items-center space-y-4 py-6">
          {NAV_LINKS.map((link) => (
            <a key={link.label} href={link.href} className={`text-lg uppercase font-medium ${isScrolled ? 'text-gray-800' : 'text-white'} hover:text-amber-500 transition-colors`} onClick={() => setIsMenuOpen(false)}>
              {link.label}
            </a>
          ))}
        </nav>
      </div>
    </header>
  );
};

export default Header;
