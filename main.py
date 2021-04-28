from similarity import find_most_similar, find_most_similar_interaction
from corpus import CORPUS,TALK_TO_HUMAN

class Bot:

    def __init__(self):
        self.event_stack = []
        self.interact = []
        self.settings = {
            "min_score": 0.3,
            "help_email": "fakeEmail@notArealEmail.com",
            "faq_page": "www.NotActuallyAnFAQ.com"
        }
        print ("Ask a question:")
        while(True):
            text = input()
            self.allow_question(text)
        

    def allow_question(self, text):
        # Check for event stack
        potential_event = None
        # print(self.interact)
        
        if(len(self.event_stack)):
            potential_event = self.event_stack.pop()
        if len(self.interact):
            self.interact.pop()
            # text = input("Question to Human: ")
            # send question to humans
            print("ok, wait until a human answers")
            return {'answer': 'Question sent, wait for a response'}
            
        if potential_event:
            # text = input("Response: ")
            potential_event.handle_response(text, self)
        else:
            # print('here')
            # text = input("Question: ")
            answer = self.pre_built_responses_or_none(text)
            person = find_most_similar_interaction(text)
            
            if not answer:
                # print('here')
                if person['score'] > 0.3:
                    self.interact.append(True)
                    print('Asking what to send to a human')
                    return {'answer': 'What do you want to ask to a human?'}
                answer = find_most_similar(text)
                print(answer['score'])
                if answer['score'] < 0.3:
                    # send the question to humans
                    print('Cant answer, Question sent to human')
                    return {'answer': 'i cannot answer that, i just sent it to a human, wait for the response'}
                print(self.answer_question(answer, text))
                return self.answer_question(answer, text)
            

    def answer_question(self, answer, text):
        if answer['score'] > self.settings['min_score']:
            # set off event asking if the response question is what they were looking for
            return {'most_similar_question':answer['question'],
                    'similarity_percentage':answer['score'],
                    'answer':answer['answer']}

        else:
            
            return {'most_similar_question':'',
                    'similarity_percentage':0.0,
                    'answer': 'I could not understand you, Would you like to see the list of questions that I am able to answer?\n'}
            # set off event for corpus dump
            self.event_stack.append(Event("corpus_dump", text))

    def pre_built_responses_or_none(self, text):
        # only return answer if exact match is found
        pre_built = [
            {
                "Question": "Hello",
                "Answer": "Hello, What can I Help you with?\n"
            },
            {
                "Question": "Who made you?",
                "Answer": "I was created by NousCommerce Team.\n"
            },
            {
                "Question": "When were you born?",
                "Answer": "I said my first word on march 26, 2021.\n"
            },
            {
                "Question": "What is your purpose?",
                "Answer": "I assist user experience by providing an interactive FAQ chat.\n"
            },
            {
                "Question": "Thanks",
                "Answer": "Glad I could help!\n"
            },
            {
                "Question": "Thank you",
                "Answer": "Glad I could help!\n"
            }
        ]
        for each_question in pre_built:
            if each_question['Question'].lower() in text.lower():
                print (each_question['Answer'])
                return each_question

    def dump_corpus(self):
        # Get json from backend 
        question_stack = []
        for each_item in CORPUS:
            question_stack.append(each_item['Question'])
        return question_stack


class Event:

    def __init__(self, kind, text):
        self.kind = kind
        self.CONFIRMATIONS = ["yes", "sure", "okay", "that would be nice", "yep", "ok", "fine"]
        self.NEGATIONS = ["no", "don't", "dont", "nope", "nevermind"]
        self.original_text = text

    def handle_response(self, text, bot):
        if self.kind == "corpus_dump":
            self.corpus_dump(text, bot)

    def corpus_dump(self, text, bot):
        for each_confirmation in self.CONFIRMATIONS:
            for each_word in text.split(" "):
                if each_confirmation.lower() == each_word.lower():
                    corpus = bot.dump_corpus()
                    corpus = ["-" + s for s in corpus]
                    print ("%s%s%s" % ("\n", "\n".join(corpus), "\n"))
                    return 0
        for each_negation in self.NEGATIONS:
            for each_word in text.split(" "):
                if each_negation.lower() == each_word.lower():
                    print ("Feel free to ask another question or send an email to %s.\n" % bot.settings['help_email'])
                    bot.allow_question()
                    return 0
       
        text = input("Question: ")
        answer = self.pre_built_responses_or_none(text)
        if not answer:
            answer = find_most_similar(text)
            self.answer_question(answer, text)
        # base case, no confirmation or negation found
        # print ("I'm having trouble understanding what you are saying. At the time, my ability is quite limited, " \
        #       "please refer to %s or email %s if I was not able to answer your question. " \
        #       "For convenience, a google link has been generated below: \n%s\n" % (bot.settings['faq_page'],
        #                                                                          bot.settings['help_email'],
        #                                                                          "https://www.google.com/search?q=%s" %
        #                                                                          ("+".join(self.original_text.split(" ")))))
        return 0


Bot()
