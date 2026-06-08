class KnowledgeBase:

    def __init__(self, data):
        self.data = data

    def add(self, question, answer):
        self.data[question] = answer

    def get(self, question):
        return self.data.get(question)

    def all_questions(self):
        return list(self.data.keys())

    def all_data(self):
        return self.data

    def remove(self, question):

        if question in self.data:

            del self.data[question]

            return True

        return False