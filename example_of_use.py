from secretsanta import SecretSanta

if __name__ == '__main__':
    #The sender of all emails, after configuration to allow for Python to send mails
    secret_email = "your-secret-santa-mail@gmail.com" 
    
    friends = ["You", "Leonard", "Penny", "Howard", "Raj"]
    emails = ["mymail@hotmail.com", "leonardsmail@yahoo.com", "pennysmail@gmail.com",
              "howardsmail@hotchicks.com", "rajsmail@university.com"]
    exceptions = {fr:[] for fr in friends}
    #Penny and Leonard are married and are mutually excluded
    exceptions["Leonard"].append("Penny")
    exceptions["Penny"].append("Leonard")
    
    #Let's get down to business
    
    ss = SecretSanta(friends, emails, exceptions)
    #Raj does not want to participate anymore
    ss.remove_people(["Raj"])
    ss.get_matches() #Print who is sending to who?
    ss.send_secret_santa(secret_email) #Send results
    
    #Or simply
    ss = SecretSanta(friends, emails, exceptions)
    ss.do_and_send_secret_santa(secret_email)
