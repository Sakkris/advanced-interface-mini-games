# Navigate to your project directory
cd path/to/your/project

# Create a virtual environment named 'virtual'
python -m venv virtual

# Activate the virtual environment
# On Windows
virtual\Scripts\activate

# Install required packages
pip freeze > requirements.txt  
pip install -r requirements.txt

# Your environment is now set up, and you can run your Python scripts
python script.py

# When done, deactivate the virtual environment
deactivate