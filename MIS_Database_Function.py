__author__ = 'John'
import sqlite3
import Info_IaState_Scraper


def get_connection():
    return sqlite3.connect('MIS.Checkin.sqlite3')

###########################################
#        Event Based Functions            #
###########################################


def create_event(company, topic, date):
    """
    Creates an event with the given company, topic, and date. All input values
    should be strings of characters. An eventID is generated by selecting the maximum
    id from the database and adding one to it.

    :param company: The company name e.g. WalMart
    :param topic: The topic for the event. If none is known pass 'unknown'
    :param date: The date for the event. Pass in the format 'DD/MMM/YYYY'.
                SQLite does not have a dedicated date format so this is very important.
    :return: void
    """
    connection = get_connection()
    cursor = connection.cursor()
    data = cursor.execute('SELECT MAX(eventID) FROM Event')
    event_id = data.fetchone()[0]
    if event_id is None:
        event_id = 0
    else:
        event_id += 1
    sql_string = "INSERT INTO Event VALUES("+str(event_id)+", '"+company+"', '"+topic+"', '"+date+"')"
    cursor.execute(sql_string)
    connection.commit()


def delete_event(event_id):
    """
    Deletes an event based on a given eventID
    :param event_id: The event id of the event to be deleted
    :return: void
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "DELETE FROM Event WHERE eventID ="+str(event_id)
    cursor.execute(sql_string)
    connection.commit()


def delete_event_by_company(company):
    """
    Deletes an event based on the given company name.
    :param company: The name of the company e.g. Target
    :return: void
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "DELETE FROM Event WHERE company='"+company+"'"
    cursor.execute(sql_string)
    connection.commit()


def set_topic(event_id, topic):
    """
    Sets the topic value in the db for a given eventID
    :param event_id: The eventID of the event whose topic value is to be set
    :param topic: The actual topic e.g. 'Mobile Development'
    :return: void
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "UPDATE Event SET Topic='"+topic+"' WHERE eventID="+str(event_id)
    cursor.execute(sql_string)
    connection.commit()

###########################################
#        Member Based Functions           #
###########################################


def create_member(net_id):
    """
    Creates a member instance in the Member table.

    :param net_id: The new member's net id
    :return: void
    """
    #TODO put this exception handling in to the presentation layer
    #if ' ' in net_id or '@' in net_id:
    #    raise Exception('Only enter the first portion of the net id => jmrolf@iastate.edu - jmrolf')
    student_html = Info_IaState_Scraper.get_raw_html(net_id)
    student_data = Info_IaState_Scraper.parse_student_data(student_html)
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "INSERT INTO Member VALUES('"+net_id+"', '"+net_id+"@iastate.edu', " \
                 "'"+student_data['classification']+"', '" + student_data['major']+"', " \
                 "'"+student_data['name']+"', 0)"
    cursor.execute(sql_string)
    connection.commit()


def set_major(net_id, major):
    """
    Sets the major attribute for the given net id in the member table.

    :param net_id: The net id of the user whose major is to be set
    :param major: The string value to be set
    :return:
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "UPDATE Member SET major='"+major+"' WHERE netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()


def set_email(net_id, email):
    """
    Sets the email field in the Member table for the given net id.

    :param net_id: The net id of the user whose email is being set
    :param email: The string value that the email is to be set to
    :return: void
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "UPDATE Member SET email='"+email+"' WHERE netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()


def set_name(net_id, name):
    """
    Sets the name field in the Member table for hte given net id.

    :param net_id: The net id of hte user whose email is being set
    :param name: The string value representing the users name
    :return: void
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "UPDATE Member SET name='"+name+"' WHERE netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()


def set_dues(net_id, paid):
    """
    Sets the dues_paid attribute for the given net id to the passed value.
    SQLite is very loose with its typing so it is important that the consumers of this function
    pass in only 0 or 1 else data integrity will become questionable if not unusable.

    :param net_id:
    :param paid:
    :return:
    """
    if paid not in(0, 1):
        raise AttributeError("Paid must be either 0 for false or 1 for true")
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "UPDATE Member SET dues_paid="+str(paid)+" WHERE netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()


def set_classification(net_id, classification):
    """
    Sets the classification for the given net id to the passed classification string
    :param net_id: The net id of the user whose classification is to be set
    :param classification: The string literal of hte classification
    :return: void
    """
    if classification not in ('Freshman', 'Sophomore', 'Junior', 'Senior'):
        raise AttributeError("Classification must be in ('Freshman', 'Sophomore', 'Junior', 'Senior')")
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "UPDATE Member SET classification='"+classification+"' WHERE netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()


def delete_member(net_id):
    """
    Deletes the member with the given net_id

    :param net_id: The net id of the member to be deleted
    :return: void
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "DELETE FROM Member WHERE netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()


def check_member(net_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "SELECT * FROM Member WHERE netID ='"+net_id+"'"
    cursor.execute(sql_string)
    member = cursor.fetchone()
    return member is not None


###########################################
#        Ticket Based Functions           #
###########################################


def create_ticket(event_id, net_id):
    """
    Creates a ticket with the given event_id and net_id

    :param event_id: The event id for the new ticket
    :param net_id: The net_id for the new ticket
    :return: void
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "INSERT INTO Ticket VALUES("+str(event_id)+", '"+net_id+"')"
    cursor.execute(sql_string)
    connection.commit()


def delete_ticket(event_id, net_id):
    """
    Deletes the ticket with the given event_id and net_id

    :param event_id:
    :param net_id:
    :return:
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "DELETE FROM Ticket WHERE eventID="+str(event_id)+" AND netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()

###########################################
#     END OF SEMESTER FUNCTIONS           #
###########################################


#TODO set and test on delete cascade for the ticket table
def run_end_of_semester():
    """
    This function updates the database to ensure that the members semesters paid is
    decremented by one. Run this function once per semester at the END of the semester.

    Running this prematurely may result in members appearing to be unpaid when they are
    in fact paid.

    If a members semester paid (dues_paid) value ever falls below 0 they will be deleted from
    the database.
    :return: None

    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "SELECT netID FROM MEMBER"
    cursor.execute(sql_string)
    entries = cursor.fetchall()
    for entry in entries:
        #example string:
        #UPDATE Member SET dues_paid = (SELECT dues_paid FROM Member WHERE netID = 'jmrolf')-1
        #WHERE netID = 'jmrolf'
        sql_update_string = "UPDATE Member SET dues_paid = (SELECT dues_paid FROM Member WHERE netID = '"+str(entry[0])+ \
            "')-1 WHERE netID = '"+str(entry[0])+"'"
        cursor.execute(sql_update_string)

    cursor.execute('SELECT netID, dues_paid FROM Member')
    to_delete_entries = cursor.fetchall()
    for entry in to_delete_entries:
        if entry[1] < 0:
            cursor.execute("DELETE FROM Member WHERE netID = '"+entry[0]+"'")
    connection.commit()