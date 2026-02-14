
import React from 'react';
import { CLIENT_LOGOS } from '../constants';

const ClientLogos: React.FC = () => {
  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-6">
        <h3 className="text-center text-2xl font-semibold text-gray-500 mb-8">Trusted by the Industry's Best</h3>
        <div className="flex flex-wrap justify-center items-center gap-x-12 gap-y-8">
          {CLIENT_LOGOS.map((logoUrl, index) => (
            <div key={index} className="flex-shrink-0">
              <img 
                src={logoUrl} 
                alt={`Client Logo ${index + 1}`} 
                className="h-12 object-contain filter grayscale hover:grayscale-0 transition-all duration-300"
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ClientLogos;
