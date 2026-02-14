# SD Hotel Furniture Showcase

A modern, responsive website for showcasing hotel furniture products and projects. This project has been converted from React/TypeScript to HTML, Bootstrap, and vanilla JavaScript with Flask backend integration.

## 🚀 Features

- **Responsive Design**: Built with Bootstrap 5 for mobile-first responsive layouts
- **Modern UI**: Clean and professional design with smooth animations
- **Product Categories**: Showcase different furniture categories (Guest Room, Lobby, Restaurant, Outdoor)
- **Featured Projects**: Interactive project slider using Swiper.js
- **Value Propositions**: Highlight company advantages with custom icons
- **Process Steps**: Visual representation of the company's workflow
- **Client Logos**: Display trusted partners
- **Flask Backend**: Ready for future API integration and database connectivity

## 📁 Project Structure

```
sd-hotel-furniture-showcase/
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── css/
│   │   └── styles.css         # Custom styles
│   ├── js/
│   │   ├── data.js            # Data constants
│   │   └── app.js             # Main JavaScript functionality
│   └── images/                # Static images (add your own)
└── README.md                  # This file
```

## 🛠️ Technologies Used

### Frontend
- **HTML5**: Semantic markup
- **Bootstrap 5.3.2**: Responsive framework
- **Vanilla JavaScript**: No framework dependencies
- **Swiper.js 11**: Touch slider for projects
- **CSS3**: Custom styling and animations

### Backend
- **Flask 3.0.0**: Python web framework
- **Werkzeug 3.0.1**: WSGI utility library

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A modern web browser

## 🔧 Installation

### 1. Clone or Download the Project

```bash
cd sd-hotel-furniture-showcase
```

### 2. Create a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

### Development Mode

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🌐 Available Routes

- **`/`** - Main homepage
- **`/api/health`** - Health check endpoint
- **`/api/products`** - Products API (placeholder for future implementation)
- **`/api/projects`** - Projects API (placeholder for future implementation)
- **`/api/contact`** - Contact form endpoint (placeholder for future implementation)

## 🎨 Customization

### Updating Content

1. **Data**: Edit [`static/js/data.js`](static/js/data.js) to modify:
   - Navigation links
   - Product categories
   - Featured projects
   - Value propositions
   - Process steps
   - Client logos

2. **Styles**: Modify [`static/css/styles.css`](static/css/styles.css) to change:
   - Colors (update CSS variables in `:root`)
   - Fonts
   - Spacing
   - Animations

3. **Layout**: Edit [`templates/index.html`](templates/index.html) to change:
   - Section structure
   - HTML content
   - Meta tags

### Adding Images

Place your images in the `static/images/` directory and update the image URLs in [`static/js/data.js`](static/js/data.js).

## 🔌 Backend Integration

The Flask backend is ready for integration. To add database functionality:

1. **Install Database Driver** (e.g., for PostgreSQL):
   ```bash
   pip install psycopg2-binary
   ```

2. **Add Database Configuration** in [`app.py`](app.py):
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-url'
   ```

3. **Create Models** for your data (products, projects, etc.)

4. **Update API Endpoints** to fetch from database instead of returning placeholders

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🎯 Future Enhancements

- [ ] Add database integration (PostgreSQL/MySQL)
- [ ] Implement contact form with email functionality
- [ ] Add admin panel for content management
- [ ] Implement user authentication
- [ ] Add product detail pages
- [ ] Integrate payment gateway
- [ ] Add multi-language support
- [ ] Implement search functionality
- [ ] Add blog section
- [ ] Integrate analytics

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is already in use, change it in [`app.py`](app.py):
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Static Files Not Loading
Ensure the Flask app is running and the static folder structure is correct.

### Swiper Not Working
Check that Swiper.js CDN is accessible and JavaScript console for errors.

## 📄 License

This project is created for demonstration purposes.

## 👥 Contributing

This is a showcase project. Feel free to fork and customize for your own use.

## 📞 Support

For questions or issues, please refer to the Flask documentation:
- Flask: https://flask.palletsprojects.com/
- Bootstrap: https://getbootstrap.com/docs/
- Swiper: https://swiperjs.com/

---

**Note**: Remember to update the `SECRET_KEY` in [`app.py`](app.py) before deploying to production!
