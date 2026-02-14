
import React from 'react';

const AboutSection: React.FC = () => {
  return (
    <section id="about" className="py-20 bg-gray-50">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center gap-12">
          <div className="md:w-1/2">
            <img 
              src="https://picsum.photos/seed/aboutus/800/600" 
              alt="Hotel Lobby Furniture"
              className="rounded-lg shadow-2xl w-full"
            />
          </div>
          <div className="md:w-1/2">
            <h2 className="text-sm uppercase font-bold text-amber-500 mb-2">About Our Company</h2>
            <h3 className="text-3xl md:text-4xl font-bold text-gray-800 mb-6">Your Vision, Our Craftsmanship</h3>
            <p className="text-gray-600 mb-4 leading-relaxed">
              For over two decades, SD Hotel Furniture has been a trusted partner for hoteliers and designers worldwide. We specialize in creating high-quality, custom-made furniture that not only meets the aesthetic and functional needs of the hospitality industry but also tells a story.
            </p>
            <p className="text-gray-600 leading-relaxed">
              Our commitment to excellence is reflected in every piece we create, from elegant guest room furnishings to stunning public area installations. We believe in building lasting relationships with our clients through collaboration, innovation, and unwavering dedication to quality.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
