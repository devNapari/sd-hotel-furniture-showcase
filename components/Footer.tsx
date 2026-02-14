
import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer id="contact" className="bg-gray-900 text-gray-300">
      <div className="container mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
          {/* About */}
          <div>
            <h3 className="text-xl font-bold text-white mb-4">
              SD<span className="text-amber-500">HOTEL</span>
            </h3>
            <p className="text-sm leading-relaxed">
              Manufacturing exquisite, durable, and custom-designed furniture for the global hospitality industry.
            </p>
            <div className="flex space-x-4 mt-6">
                <a href="#" className="p-2 bg-gray-700 rounded-full hover:bg-amber-500 transition-colors"><IconFacebook /></a>
                <a href="#" className="p-2 bg-gray-700 rounded-full hover:bg-amber-500 transition-colors"><IconTwitter /></a>
                <a href="#" className="p-2 bg-gray-700 rounded-full hover:bg-amber-500 transition-colors"><IconInstagram /></a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#about" className="hover:text-amber-500">About Us</a></li>
              <li><a href="#products" className="hover:text-amber-500">Products</a></li>
              <li><a href="#projects" className="hover:text-amber-500">Projects</a></li>
              <li><a href="#" className="hover:text-amber-500">Careers</a></li>
            </ul>
          </div>

          {/* Product Categories */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Categories</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-amber-500">Guest Room</a></li>
              <li><a href="#" className="hover:text-amber-500">Lobby & Public Area</a></li>
              <li><a href="#" className="hover:text-amber-500">Restaurant & Bar</a></li>
              <li><a href="#" className="hover:text-amber-500">Outdoor Furniture</a></li>
            </ul>
          </div>
          
          {/* Contact */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Contact Us</h4>
            <ul className="space-y-3 text-sm">
              <li className="flex items-start">
                <span className="mt-1 mr-3"><IconMapPin/></span>
                123 Furniture Avenue, Design City, 12345
              </li>
              <li className="flex items-start">
                <span className="mt-1 mr-3"><IconPhone/></span>
                +1 (555) 123-4567
              </li>
              <li className="flex items-start">
                 <span className="mt-1 mr-3"><IconMail/></span>
                 contact@sdhotelfurniture.com
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div className="bg-black py-4">
        <div className="container mx-auto px-6 text-center text-xs text-gray-500">
          <p>&copy; {new Date().getFullYear()} SD Hotel Furniture. All Rights Reserved. Frontend created for demonstration.</p>
        </div>
      </div>
    </footer>
  );
};

// Helper SVG Icon Components
const IconFacebook = () => <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>;
const IconTwitter = () => <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path></svg>;
const IconInstagram = () => <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>;
const IconMapPin = () => <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>;
const IconPhone = () => <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>;
const IconMail = () => <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>;

export default Footer;
