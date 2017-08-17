import os
import sqlite3
from email.parser import Parser
########################################################################################################################
######                                      EMAIL CLASS                                                           ######
########################################################################################################################
class Email:
    def __init__(self, \
                 # sender_name,sender_email_address,sentOn,to,cc,bcc,subject,body,\
                 header_from, header_to, header_subject, header_date, message_id, email_body, \
                 is_confirmed, class0, class1 \
                 ):
        """email being classified into different classes which need to be confirmed by the user

        Attributes:
        mail information
        header_from: 
        header_to: 
        header_subject:
        header_date:
        message_id:
        email_body:

        mail Flag
        is_confirmed:
        class0:
        class1:

        """
        # mail information
        self.header_from = header_from
        self.header_to = header_to
        self.header_subject = header_subject
        self.header_date = header_date
        self.message_id = message_id

        self.email_body = email_body

        # mail Flag
        self.is_confirmed = is_confirmed  # True/False: if flag is the truth
        # self.log_confirmed             #time of confirmation
        self.class0 = class0  # True/False
        self.class1 = class1

    def insert_email_in_db(self, sqlite_cursor):
        email_data = [(  # str(self.sentOn), self.sender_name,self.sender_email_address,\
            # self.to,self.cc, self.bcc,self.subject,self.body,
            str(self.header_date), self.header_from, self.header_to, self.header_subject, \
            self.message_id, self.email_body, \
            self.is_confirmed, self.class0, self.class1)]

        sqlite_cursor.executemany("INSERT INTO TABLE_EMAILS_ICTU VALUES(?,?,?,?,?,?,?,?,?)", email_data)

        # user data? user_id? date of confirmed
        # def predict(model):


########################################################################################################################
######                                      DATABASE DATA                                                         ######
########################################################################################################################

def update_database(path_db, path_new_mails,database_file):

    # connection to database
    conn = sqlite3.connect(path_db + database_file)
    # create cursor
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS TABLE_EMAILS_ICTU
             (EMAIL_date text, EMAIL_from text, 
             EMAIL_to text, EMAIL_subject text,
             EMAIL_message_id text,EMAIL_body text,EMAIL_html text
             EMAIL_is_confirmed boolean, EMAIL_class0 boolean, EMAIL_class1 boolean)''')

    #### READ NEW MAILS FROM NEW_MAIL DIR ###
    for mail_file in os.listdir(path_new_mails):
        print('Read file: ' + mail_file)
        parser = Parser()
        with open(path_new_mails + '/' + mail_file, 'r') as fp:
            msg = parser.parse(fp)

        def get_clean_body(msg, html_or_plain):
            _msg = ''
            if msg.is_multipart():
                for part in msg.get_payload():
                    _msg += get_clean_body(part, html_or_plain)
            else:
                if msg.get_content_type() == 'text/' + html_or_plain:
                    _msg += str(msg.get_payload(decode=True).decode('utf-8', 'ignore'))
            return _msg

        mail = Email(
            msg['Date'], msg['From'], msg['To'], msg['Subject'], \
            msg['Message-ID'], get_clean_body(msg,'plain'),get_clean_body(msg,'html'), \
            False, True, False
        )

        mail.insert_email_in_db(c)

    # Save the changes when done
    print('Commit changes to database...')
    conn.commit()
    # close connection
    print('Close connection to database...')
    conn.close()

def load_database(path_db,database_file):
    conn = sqlite3.connect(path_db + database_file)
    # create cursor
    c = conn.cursor()
    dic_unknown = list()
    dic_class0 = list()
    dic_class1 = list()
    for x in c.execute('SELECT * FROM TABLE_EMAILS_ICTU ORDER BY EMAIL_date'):
        if not (x[7]):
            dic_unknown.append({'header_from': x[2], 'header_to': x[3], 'header_subject': x[0],
                                'header_date': x[1], 'message_id': x[4], 'email_body': x[5],'email_html':x[6], \
                                'class0': x[8], 'class1': x[9]})
        if x[7]:
            if x[8]:
                dic_class0.append({'header_from': x[2], 'header_to': x[3], 'header_subject': x[0],
                                'header_date': x[1], 'message_id': x[4], 'email_body': x[5],'email_html':x[6], \
                                'class0': x[8], 'class1': x[9]})
            if x[9]:
                dic_class1.append({'header_from': x[2], 'header_to': x[3], 'header_subject': x[0],
                                'header_date': x[1], 'message_id': x[4], 'email_body': x[5],'email_html':x[6], \
                                'class0': x[8], 'class1': x[9]})

    conn.close()
    return {"unknown_emails":dic_unknown,"class0_emails": dic_class0,"class1_emails":dic_class1}
python_data = {"unknown_emails":[{
                            'message_id': 1,
                            'class0':True,
                            'class1':False,
                            'header_from': "Kimberly Grant",
                            'header_to': "Lize Lewis",
                            'header_subject': "subject 1",
                            'email_body': "Hi, how are you? Grant here...",
                            'header_date':"17-01-2017"
                        }, {
                            'message_id': 2,
                            'class0':False,
                            'class1':True,
                            'header_from': "Elizabeth Lewis",
                            'header_to': "Kim Grant",
                            'header_subject': "subject 2",
                            'email_body': "Hi, how are you? Liz here...",
                            'header_date':"25-12-2016"
                        },{
                            'message_id': 3,
                            'class0':False,
                            'class1':True,
                            'header_from': "Shawn Ellis",
                            'header_to': "Lize Lewis",
                            'header_subject': "subject 3",
                            'email_body': "Hi, how are you? Shawn here...",
                            'header_date':"16-10-2016"
                        },{
                            'message_id': 4,
                            'class0':True,
                            'class1':False,
                            'header_from': "Shawn Ellis",
                            'header_to': "Kim Grant",
                            'header_subject': "subject 4",
                            'email_body': "Hi, how are you? Sh here...",
                            'header_date':"13-09-2016"
                        },{
                            'message_id': 5,
                            'class0':False,
                            'class1':True,
                            'header_from': "Shawn Ellis",
                            'header_to': "Lize G.",
                            'header_subject': "subject 5",
                            'email_body': "Hi, how are you? I am here...",
                            'header_date':"05-07-2016"
                        },{
                            'message_id': 6,
                            'class0':False,
                            'class1':True,
                            'header_from': "Shawn Ellis",
                            'header_to': "Lize T.",
                            'header_subject': "subject 5",
                            'email_body': "Hi, how are you? Ellis here...",
                            'header_date':"12-02-2016"
                        }
]}

'''
MACHINE LEARNING
'''


'''
RETRAIN MODEL
'''