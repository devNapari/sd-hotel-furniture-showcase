
import React from 'react';
import { VALUE_PROPOSITIONS } from '../constants';

const WhyChooseUs: React.FC = () => {
  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-sm uppercase font-bold text-amber-500 mb-2">Our Advantages</h2>
        <h3 className="text-3xl md:text-4xl font-bold text-gray-800 mb-12">Why Choose Us</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          {VALUE_PROPOSITIONS.map((prop) => (
            <div key={prop.title} className="p-8 border border-gray-200 rounded-lg hover:shadow-xl transition-shadow duration-300">
              <div className="flex justify-center mb-4">
                {prop.icon}
              </div>
              <h4 className="text-xl font-semibold text-gray-800 mb-2">{prop.title}</h4>
              <p className="text-gray-600 leading-relaxed">{prop.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default WhyChooseUs;
