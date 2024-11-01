from music import create_app  # Import the create_app function from the travel package

# Check if this script is run directly
if __name__ == '__main__':
    # Create an instance of the Flask application
    app = create_app()
    # Run the Flask application with debug mode turned off for production
    app.run(debug=False)
