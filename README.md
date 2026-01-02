# The Cozy Corner - Cafe Menu App

A modern, responsive Flask web application for managing a cafe menu with categories, image uploads, and an admin panel.

## Features

- **Menu Display**: Beautiful card-based layout with category filtering
- **Admin Panel**: Full CRUD operations for menu items
- **Image Uploads**: Secure file uploads with validation
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Modals**: Popup forms for adding/editing items
- **Categories**: Breakfast, Lunch, and Drinks filtering

## Local Development

1. Clone the repository
2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:

   ```bash
   python app.py
   ```

5. Or test the production server locally:

   ```bash
   python run_production.py
   ```

6. Open http://localhost:5000 (dev) or http://localhost:8000 (production) in your browser

## Production Server Warning

When you see the warning "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.", it means you're using Flask's built-in development server.

**For production deployment, always use:**

- **Gunicorn** (Linux/Unix): `gunicorn app:application`
- **Waitress** (Windows): `python run_production.py`
- **uWSGI**: For advanced deployments

The development server is not secure, performant, or suitable for production use.

## Deployment

### Heroku Deployment

1. Create a Heroku app
2. Set environment variables:

   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set FLASK_DEBUG=False
   ```

3. Deploy:
   ```bash
   git push heroku main
   ```

### Windows Server Deployment

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables:
   ```bash
   set SECRET_KEY=your-secret-key-here
   set FLASK_DEBUG=False
   ```
3. Run: `python run_production.py`

### Linux/Unix Server Deployment

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables:
   ```bash
   export SECRET_KEY=your-secret-key-here
   export FLASK_DEBUG=False
   ```
3. Run with Gunicorn: `gunicorn --bind 0.0.0.0:8000 app:application`

### General Production Deployment

- Set `FLASK_DEBUG=False` in environment
- Use a production WSGI server like Gunicorn
- Set a strong `SECRET_KEY`
- Configure a production database if needed
- Use HTTPS in production

## Environment Variables

- `SECRET_KEY`: Flask secret key (required for production)
- `FLASK_DEBUG`: Set to 'true' for development, 'false' for production

## File Structure

```
menu/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version for Heroku
├── Procfile              # Heroku process file
├── .env.example          # Environment variables template
├── menu.db               # SQLite database (created automatically)
├── static/
│   ├── style.css         # Main stylesheet
│   └── uploads/          # Uploaded images
└── templates/
    ├── index.html        # Main menu page
    ├── admin.html        # Admin panel
    ├── add_item.html     # Add item form
    ├── edit_item.html    # Edit item form
    ├── 404.html          # 404 error page
    └── 500.html          # 500 error page
```

## Security Notes

- File uploads are limited to 16MB
- Only image files (PNG, JPG, JPEG, GIF) are allowed
- SQL injection protection with parameterized queries
- Secure filename handling

## License

This project is open source and available under the MIT License.
