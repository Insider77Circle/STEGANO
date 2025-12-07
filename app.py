#!/usr/bin/env python3
"""
Stegano-Prompt Web Application
Beautiful UI for invisible adversarial injection tool
"""

from flask import Flask, render_template, request, jsonify
from stegano_prompt import SteganoPrompt
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stegano-prompt-secret-key'

# Initialize the attack generator
attacker = SteganoPrompt()

@app.route('/')
def index():
    """Render the main interface"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_attack():
    """Generate steganographic attack vector"""
    try:
        data = request.get_json()
        
        visible_context = data.get('visible_context', '')
        hidden_instruction = data.get('hidden_instruction', '')
        template_type = data.get('template_type', 'variable')
        encoding_type = data.get('encoding_type', 'zero_width')
        
        if not visible_context or not hidden_instruction:
            return jsonify({'error': 'Both visible context and hidden instruction are required'}), 400
        
        # Generate attack vector
        attack_vector = attacker.generate_template(
            visible_context, 
            hidden_instruction,
            template_type,
            encoding_type
        )
        
        # Analyze the attack
        analysis = attacker.analyze_attack_vector(attack_vector)
        
        # Decode to verify (for zero-width encoding)
        decoded = ""
        if analysis['encoding_detected'] == "Zero-width character encoding":
            decoded = attacker.decode_payload(attack_vector)
        
        # Generate detection report
        detection_report = attacker.generate_detection_report(attack_vector)
        
        return jsonify({
            'success': True,
            'attack_vector': attack_vector,
            'analysis': analysis,
            'decoded_payload': decoded,
            'detection_report': detection_report,
            'encoding_type': analysis['encoding_detected']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_text():
    """Analyze text for steganographic content"""
    try:
        data = request.get_json()
        text_to_analyze = data.get('text', '')
        
        if not text_to_analyze:
            return jsonify({'error': 'Text to analyze is required'}), 400
        
        # Analyze the text
        analysis = attacker.analyze_attack_vector(text_to_analyze)
        detection_report = attacker.generate_detection_report(text_to_analyze)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'detection_report': detection_report
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_encoding_info', methods=['GET'])
def get_encoding_info():
    """Get information about available encoding types"""
    return jsonify({
        'encoding_types': [
            {
                'name': 'zero_width',
                'description': 'Zero-width characters (U+200B, U+200C, U+200D, U+FEFF)',
                'stealth_level': 'High',
                'compatibility': 'Universal'
            },
            {
                'name': 'variation_selectors',
                'description': 'Unicode variation selectors (U+FE00-U+FE03)',
                'stealth_level': 'Very High',
                'compatibility': 'Emoji-aware systems'
            },
            {
                'name': 'mixed',
                'description': 'Mixed invisible character types',
                'stealth_level': 'Maximum',
                'compatibility': 'Advanced evasion'
            }
        ],
        'template_types': [
            {
                'name': 'variable',
                'description': 'Hidden in Jinja2 variable (appears empty)',
                'use_case': 'General purpose injection'
            },
            {
                'name': 'comment',
                'description': 'Hidden in Jinja2 comment block',
                'use_case': 'Code comment injection'
            },
            {
                'name': 'whitespace',
                'description': 'Hidden in whitespace between text',
                'use_case': 'Text spacing manipulation'
            }
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
