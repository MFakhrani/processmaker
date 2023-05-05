import json
import os
import openai
import sys

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.organization = os.environ["OPENAI_ORG"]

# Supported languages dictionary
languages = {
  'es': 'Spanish',
  'de': 'German',
  'fr': 'French',
  'ja': 'Japanese',
  'nl': 'Dutch'
}

# Check if the script received the expected number of arguments
if len(sys.argv) != 2:
    print("Usage: python translate.py lang")
    sys.exit(1)

# Access the language argument passed to the script
lang = sys.argv[1]

def main():
    with open('resources/lang/en.json', 'r') as f:
        en_data = json.load(f)
    
    # Check if the language is supported
    if lang in languages:
        lang_name=languages[lang]
    else:
        print("Unsupported language:", lang)
        sys.exit(1)

    file_path = f'resources/lang/{lang}.json'
    translated_data = json.load(open(file_path, 'r')) if os.path.exists(file_path) else {}
    changed = False

    for key, value in en_data.items():
        if key not in translated_data:
            prompt='You are an i18n-compatible translation service. Translate the English string on the next line to {lang}. Maintain whitespace. Do not modify or translate interpolated variables in any way.\n"{text}"'.format(lang=lang_name, text=value)
            response=openai.ChatCompletion.create(
                model='gpt-4',
                messages=[
                  {
                    "role": "user",
                    "content": prompt
                  }
                ],
                temperature=0.3,
                max_tokens=500,
                n=1,
                stop=None
            )
            translated_data[key] = response.choices[0].message.content.strip('"')
            changed = True

    if changed:
        with open(file_path, 'w') as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
