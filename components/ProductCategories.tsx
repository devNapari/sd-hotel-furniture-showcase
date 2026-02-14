
import React from 'react';
import { PRODUCT_CATEGORIES } from '../constants';

const ProductCategories: React.FC = () => {
  return (
    <section id="products" className="py-20 bg-white">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-sm uppercase font-bold text-amber-500 mb-2">Our Collection</h2>
        <h3 className="text-3xl md:text-4xl font-bold text-gray-800 mb-12">Explore Our Products</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {PRODUCT_CATEGORIES.map((category) => (
            <div key={category.name} className="group relative overflow-hidden rounded-lg shadow-lg cursor-pointer">
              <img src={category.image} alt={category.name} className="w-full h-80 object-cover transition-transform duration-500 group-hover:scale-110" />
              <div className="absolute inset-0 bg-black bg-opacity-40 group-hover:bg-opacity-60 transition-all duration-300"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <h4 className="text-white text-2xl font-bold drop-shadow-md">{category.name}</h4>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ProductCategories;
