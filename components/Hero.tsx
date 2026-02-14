
import React from 'react';

const Hero: React.FC = () => {
  return (
    <section 
      className="h-screen bg-cover bg-center flex items-center justify-center text-white" 
      style={{ backgroundImage: "url('https://picsum.photos/seed/hero/1920/1080')" }}
    >
      <div className="absolute inset-0 bg-black opacity-50"></div>
      <div className="relative z-10 text-center px-4">
        <h1 className="text-4xl md:text-6xl font-extrabold mb-4 drop-shadow-lg leading-tight">
          Crafting <span className="text-amber-400">Timeless</span> Hospitality Experiences
        </h1>
        <p className="text-lg md:text-xl max-w-3xl mx-auto mb-8 drop-shadow-md">
          Bespoke furniture solutions that blend luxury, comfort, and durability for the world's finest hotels and resorts.
        </p>
        <a 
          href="#projects" 
          className="bg-amber-500 text-white font-bold py-3 px-8 rounded-full hover:bg-amber-600 transition-transform transform hover:scale-105 shadow-lg"
        >
          View Our Work
        </a>
      </div>
    </section>
  );
};

export default Hero;
