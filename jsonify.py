import json

class Question:

    def __init__(self, text):
        self.text = text
        self._lines = self.text.splitlines()
        self.size = len(self._lines)
        self.json_fl = 'scraped.json'

        for ln in range(self.size):
            setattr(self, f'txt_{ln}', self._lines[ln])
    
    def make_dict(self):

        self.dict = {
            'question': self.txt_0,
            'answer_choices': []
        }

        for q in range(2, self.size):
            answer = getattr(self, f'txt_{q}')
            self.dict['answer_choices'].append(answer)
                
    def make_json(self):
        try:
            with open(self.json_fl) as data_file:    
                old_data = json.load(data_file)
        
        except(FileNotFoundError, json.JSONDecodeError):
            old_data = []

        old_data.append(self.dict)
        with open('scraped.json', 'w') as outfile:
            json.dump(old_data, outfile, indent=4)

    def jsonify(self):
        self.make_dict()
        self.make_json()

