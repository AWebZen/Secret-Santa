# -*- coding: utf-8 -*-
"""
@author: awebzen
"""
from copy import deepcopy
import smtplib, ssl

import numpy as np

class SecretSanta:
    def __init__(self, names, emails, exceptions):
        """
        INPUT:
        names - list of participant names
        emails - list of emails, in the same order as the names
        exceptions - dict key name, value list of names to exclude for this person
        """
        self._check_validity(names, emails, exceptions)
        self.names = deepcopy(names)
        self.emails = deepcopy(emails)
        self.exceptions = deepcopy(exceptions)
        self.message = """\
Subject: Secret Santa! You got...

Dear {PERS1},


For Secret Santa you must give a present to {PERS2}.


Be creative!


Secret Santa"""


    def add_people(self, names, emails, exceptions):
        """
        Add one or multiple people to the participants
        
        INPUT:
        names - list of names
        emails - list of emails, in the same order as the names
        exceptions - dict key name, value list of names to exclude for this person
        """
        self._check_validity(names, emails, exceptions)
        self.names.extend(names)
        self.emails.extend(emails)
        self.exceptions.update(exceptions)
       
       
    def remove_people(self, names):
        """
        Remove one or multiple participants
        
        INPUT:
        names - list of names to remove
        """
        assert all([n in self.names for n in names]), \
        "Some people you want to remove are not in the list"
        for _, name in enumerate(names):
            i = self.names.index(name)
            self.names.remove(name)
            del self.emails[i]
            del self.exceptions[name]
            

    def _check_validity(self, names, emails, exceptions):
        """
        Check validity of input participants

        INPUT:
        names - list of names
        emails - list of emails, in the same order as the names
        exceptions - dict key name, value list of names to exclude for this person
        """
        assert type(names) == list and type(emails) == list and type(exceptions) == dict, \
        "Type error: you must give two lists and a dictionary"
        assert len(names) == len(set(names)), "Uh oh, two people have the same name!"
        assert len(names) == len(emails) and len(names) == len(exceptions), \
        "Your lists and dictionary must have the same length"
        assert all([isinstance(em, str) and "@" in em and "." in em for em in emails]), \
        "There are one or multiple invalid emails!"
        assert sorted(names) == sorted(exceptions.keys()), \
        "Exception dictionary must contain all participant names as keys!"
        if hasattr(self, 'names') and len(self.names) > 0:
            assert len(set(self.names + names)) == len(names) + len(self.names), \
            "Somebody already has one of the new names you entered!"
            
    
    def find_secret_match(self, _c=0):
        """Assign secret santa matches"""
        left = deepcopy(self.names)
        self.results = {}
        for pers in self.names:
            possible_pers = [prs for prs in left if prs not in self.exceptions[pers] and prs != pers]
            if len(possible_pers) < 1:
                break
            who = np.random.choice(possible_pers)
            self.results[pers] = who
            left.remove(who)
        if len(self.results) != len(self.names):
            _c += 1
            if _c > 15:
                print("There are no valid matches for Secret Santa.")
                raise SystemExit()
            self.find_secret_match(_c) #Recursive until valid match for everyone
            
            
    def get_matches(self):
        """
        Print secret santa results (if no secret santa match has been assigned,
        assign and then print.
        """
        if not hasattr(self, "results"):
            self.find_secret_match()
        for pers in self.names:
            print("{} must give a gift to {}".format(pers, self.results[pers]))
    
    
    def personalize_message(self, mail_subject, mail_message):
        """
        You may want to personalize the email message.
        The default message is "Dear {PERS1}, For Secret Santa you must give a
        present to {PERS2}. Be creative! Secret Santa". The subject of the mail is
        "Secret Santa! You got..."
        It is mandatory that you use {PERS1} as the name of the present giver and
        {PERS2} of the present receiver, with the curly brackets. 
        Obviously, both names must be present in the message and/or title!
        
        INPUT:
        mail_subject - the personalized subject of the mail
        mail_message - the personalized message of the mail
        """
        print("Please, don't forget to put {PERS1} as the name of the giver and\
 {PERS2} as the name of the receiver in your text, without forgetting the curly\
 brackets.")
        assert "{PERS1}" in mail_subject+mail_message and "{PERS2}" in mail_subject+mail_message,\
        "You must put {PERS1} as the name of the present giver and {PERS2} as the name of the receiver!"
        self.message = "Subject: {}\n\n{}".format(mail_subject, mail_message)
       
       
    def send_secret_santa_results(self, mail_address):
        """
        Sends mails with secret santa results.

        INPUT:
        mail_address - mail address which will send the results to the participants
            Must be a gmail account.
        """
        assert isinstance(mail_address, str) and mail_address.endswith("@gmail.com"),\
        "Your mail must be a gmail address"
        port = 465  # For SSL
        password = input("Type your mail password and press enter: ")
        # Create a secure SSL context
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(mail_address, password)
            you_sure = input("Do you really want to send the emails? y or n: ")
            if you_sure.lower()[0] == "y":
                for i, pers in enumerate(self.names):
                    print("Sending email to {}...".format(pers))
                    server.sendmail(mail_address, self.emails[i], 
                                    self.message.format(PERS1=pers, 
                                                        PERS2=self.results[pers]).encode("utf8"))
                                                        
                                                        
    def do_and_send_secret_santa(self, mail_address):
        """
        No time to waste! Assign and send emails directly.
        
        INPUT:
        mail_address - mail address which will send the results to the participants
            Must be a gmail account.
        """
        if not hasattr(self, "results"):
            self.find_secret_match()
        self.send_secret_santa_results(mail_address)
