
import React from 'react';
import { OUR_PROCESS_STEPS } from '../constants';

const OurProcess: React.FC = () => {
  return (
    <section className="py-20 bg-gray-800 text-white">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-sm uppercase font-bold text-amber-400 mb-2">How We Work</h2>
        <h3 className="text-3xl md:text-4xl font-bold mb-12">Our Streamlined Process</h3>
        <div className="relative">
          <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-gray-600 -translate-y-1/2"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
            {OUR_PROCESS_STEPS.map((step) => (
              <div key={step.step} className="relative bg-gray-700 p-8 rounded-lg text-left shadow-lg border border-gray-600">
                 <div className="absolute -top-5 -left-5 bg-amber-500 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold shadow-lg">
                  {step.step}
                </div>
                <h4 className="text-xl font-semibold mb-3 mt-8">{step.title}</h4>
                <p className="text-gray-400 text-sm leading-relaxed">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default OurProcess;
