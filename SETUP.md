# Stegano-Prompt Setup Guide

## Quick Installation

### Prerequisites
- Python 3.7+
- pip package manager
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Insider77Circle/STEGANO.git
   cd STEGANO
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "from stegano_prompt import SteganoPrompt; print('Installation successful!')"
   ```

## Running the Application

### Command Line Interface
```bash
python stegano_prompt.py
```

### Web Interface
```bash
python app.py
```
Then open your browser to `http://localhost:5000`

## Testing the Installation

Run the built-in test to ensure everything is working:
```bash
python -c "
from stegano_prompt import SteganoPrompt
attacker = SteganoPrompt()
result = attacker.generate_template('Hello world', 'HIDDEN MESSAGE')
print('Test successful! Attack vector generated.')
print('Length:', len(result))
"
```

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'jinja2'**
   - Solution: `pip install jinja2`

2. **Unicode encoding errors**
   - Solution: Ensure your terminal supports UTF-8

3. **Port 5000 already in use**
   - Solution: Change port in `app.py` or kill existing process

## Security Notice

This tool is for educational and research purposes only. Use responsibly and ethically.
