// Navigation Links
const NAV_LINKS = [
    { href: '#', label: 'Home' },
    { href: '#products', label: 'Products' },
    { href: '#projects', label: 'Projects' },
    { href: '#about', label: 'About Us' },
    { href: '#contact', label: 'Contact' }
];

// Product Categories
const PRODUCT_CATEGORIES = [
    { name: 'Sofa Sets', image: '/static/images/000231.jpg' },
    { name: 'Dining Tables', image: '/static/images/dinetable0012.jpg' },
    { name: 'Complete Room Decorations', image: '/static/images/0053423.jpg' },
    { name: 'Kitchen Setup', image: '/static/images/kitchen00123.jpg' },
    { name: 'Office Furniture', image: '/static/images/office00123.jpg' },
    { name: 'Construction Services', image: '/static/images/cons00123.jpg' }
];

// Featured Projects
const FEATURED_PROJECTS = [
    {
        title: 'Government Office Complex',
        description: 'Complete office furniture and construction for a modern government facility.',
        image: '/static/images/officecomp00123.jpg'
    },
    {
        title: 'School Furniture & Construction',
        description: 'Affordable and durable furniture solutions for educational institutions.',
        image: '/static/images/schfurni00123.jpg'
    },
    {
        title: 'Residential Home Construction',
        description: 'Eco-friendly affordable homes with flexible payment terms.',
        image: '/static/images/homecons00123.png'
    }
];

// Value Propositions with SVG Icons
const VALUE_PROPOSITIONS = [
    {
        icon: `<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-amber">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
        </svg>`,
        title: 'Eco-Friendly Materials',
        description: 'We manufacture furniture using eco-friendly materials, combining both local and foreign materials for sustainability.'
    },
    {
        icon: `<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-amber">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 6v6l4 2"></path>
        </svg>`,
        title: 'Flexible Payment Terms',
        description: 'We provide affordable homes and furniture with flexible payment options to suit your budget.'
    },
    {
        icon: `<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-amber">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>`,
        title: 'Complete Solutions',
        description: 'From furniture manufacturing to construction of homes, offices, schools, and roads - we do it all.'
    }
];

// Process Steps
const OUR_PROCESS_STEPS = [
    {
        step: '01',
        title: 'Consultation',
        description: 'We discuss your needs, whether furniture or construction, and provide expert recommendations.'
    },
    {
        step: '02',
        title: 'Design & Planning',
        description: 'Our team creates detailed designs and plans tailored to your specifications and budget.'
    },
    {
        step: '03',
        title: 'Manufacturing/Construction',
        description: 'Using eco-friendly materials and skilled craftsmanship, we bring your project to life.'
    },
    {
        step: '04',
        title: 'Delivery & Support',
        description: 'We deliver and install with care, offering flexible payment terms and ongoing support.'
    }
];

// Client Logos
const CLIENT_LOGOS = [
    'https://picsum.photos/seed/logo1/150/80',
    'https://picsum.photos/seed/logo2/150/80',
    'https://picsum.photos/seed/logo3/150/80',
    'https://picsum.photos/seed/logo4/150/80',
    'https://picsum.photos/seed/logo5/150/80',
    'https://picsum.photos/seed/logo6/150/80'
];