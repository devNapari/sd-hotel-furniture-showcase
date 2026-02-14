import React from 'react';
import { FEATURED_PROJECTS } from '../constants';
// FIX: Import from `types.ts` to make TypeScript aware of the global Swiper.js element declarations.
import type { Project } from '../types';

const FeaturedProjects: React.FC = () => {
  const swiperBreakpoints = {
    '768': { slidesPerView: 2 },
    '1024': { slidesPerView: 3 },
  };

  return (
    <section id="projects" className="py-20 bg-gray-50">
      <div className="container mx-auto px-6">
        <div className="text-center">
          <h2 className="text-sm uppercase font-bold text-amber-500 mb-2">Our Portfolio</h2>
          <h3 className="text-3xl md:text-4xl font-bold text-gray-800 mb-12">Featured Projects</h3>
        </div>

        <swiper-container
          slides-per-view="1"
          space-between="30"
          loop="true"
          navigation="true"
          pagination='{"clickable": true}'
          breakpoints={JSON.stringify(swiperBreakpoints)}
        >
          {FEATURED_PROJECTS.map((project) => (
            <swiper-slide key={project.title}>
              <div className="group relative overflow-hidden rounded-lg shadow-xl text-left h-96">
                <img src={project.image} alt={project.title} className="w-full h-full object-cover" />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>
                <div className="absolute bottom-0 left-0 p-6 text-white w-full">
                  <h4 className="text-xl font-bold mb-2">{project.title}</h4>
                  <p className="text-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 max-h-0 group-hover:max-h-40 overflow-hidden">
                    {project.description}
                  </p>
                </div>
              </div>
            </swiper-slide>
          ))}
        </swiper-container>

      </div>
    </section>
  );
};

export default FeaturedProjects;
