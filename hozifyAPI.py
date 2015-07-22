#-------------------------------------------------------------------------------
# Name:        HouzifyAPI
# Purpose:     Implement a extension for exisiting API
#
# Author:      shekhar
#
# Created:     18/07/2015
# Copyright:   (c) shekhar 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import urllib2
import json
import base64
import MySQLdb


# retrieve the Data from Houzify server as per the id provided
def getData(data_id):
    username = 'recruiting_shashank'
    password = 'apipassword'
    request = urllib2.Request('http://dev.houzify.com/rest/pin/find?id=' + str(data_id))
    base64string = base64.b64encode(username + ':' + password)
    request.add_header("Authorization", "Basic " + base64string)
    print "----------- Fetching data from Houzify "
    respo = urllib2.urlopen(request)
    print "----------- Data fetched from Houzify "
    return respo.read()

# method to extract URL form JSON data as provided by Houzify API
def extractUrl(json_data):
    print "----------- Extracting URL "
    json_decode = json.loads(json_data)
    p = json_decode['image_medium']['image']
    #print p
    print "----------- URL Extracted "
    return p

# send the url to Imagga server to get back JSON full of tags
def imaggaTags(url):
    img = "http://t2.gstatic.com/images?q=tbn:ANd9GcRk9utIiZ5hmk5t5z8ekdt-yYbJWnDU9ya8g5RMtywsfKUR62fy"
    encoded_img = img
    request = urllib2.Request('http://api.imagga.com/v1/tagging?url=' + encoded_img)
    request.add_header('version','1')
    request.add_header('accept','application/json')
    request.add_header('authorization', 'Basic YWNjXzcyYWQ3MDRhYmQwMTcwOTo3MWFkYTkyNzAzNzdmNDc3MmJjMzQ1Y2JlNTZlYThkMA==')
    print "----------- Fetching data from Imagga Server "
    res = urllib2.urlopen(request)
    json_response =  res.read()
    #print json_response
    print "----------- Data fetched from Imagga Server "
    return json_response

# method to extract tags form JSON data as provided by Imagga Server
def extractTags(json_data):
    print "----------- Extracting tags "
    json_decode = json.loads(json_data)
    results =[]
    p = json_decode['results'][0]
    for x in p['tags']:
        results.append(dict(tag=x["tag"]))
    results_json = json.dumps(results)
    results_json = json.loads(results_json)
    print "----------- Tags Extracted "
    #print results
    return results

def writeDB(pin_id, new_json_data):
    #connecting to the remote MySQL DB
    db = MySQLdb.connect('50.116.7.149','recruit_shashank','dbpassword','hzpintastic')
    print "------------ DB Connected ------------"
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # execute SQL query using execute() method.
    sql_pin = 'SELECT * FROM pin_extension WHERE pin_id=' + str(pin_id)
    cursor.execute(sql_pin)
    # Fetch a single row using fetchone() method.
    data = cursor.fetchall()
    if (data):
            #need to update data
        sql_update = 'UPDATE pin_extension SET tag=\'' + new_json_data +'\' WHERE pin_id=' + str(pin_id)
        try:
            # Execute the SQL command
            cursor.execute(sql_update)
            # Commit your changes in the database
            db.commit()
            print "UPDATE complete"
        except:
            # Rollback in case there is any error
            print "Error in UPDATE"
            db.rollback()

    else:
        #need to insert data
        sql_insert = 'INSERT INTO pin_extension (pin_id, tag) VALUES (' + str(pin_id) + ',\'' + new_json_data + '\')'
        try:
            # Execute the SQL command
            cursor.execute(sql_insert)
            # Commit your changes in the database
            db.commit()
            print "INSERT complete"
        except:
            # Rollback in case there is any error
            print "Error in INSERT"
            db.rollback()
    # disconnect from server
    db.close()
    print "------------ Disconnected ------------"

def findTag(tag):
    #connecting to the remote MySQL DB
    db = MySQLdb.connect('50.116.7.149','recruit_shashank','dbpassword','hzpintastic')
    print "------------ DB Connected ------------"
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # execute SQL query using execute() method.
    sql_query = 'SELECT tag FROM pin_extension'
    result = []
    try:
        cursor.execute(sql_query)
        # Execute the SQL command
        data = cursor.fetchall()
        for x in data:
            try:
                for p in (json.loads(x[0])['image_tags']):
                    print (json.loads(x[0])['id'])
                    try:
                        if(tag == str(str(p['tag']))):
                            result.append(x)
                    except:
                        print "Data not found in this row"
            except:
                print "Some error while processing DB row"
    except:
        print "Error in QUERY"

    return result
    # disconnect from server
    db.close()
    print "------------ Disconnected ------------"



def main():
    """
    pin_id = 366141
    url_json = getData(pin_id)
    url = extractUrl(url_json)
    tags_json = imaggaTags(url)
    tags = extractTags(tags_json)
    new_json = json.loads(url_json)
    new_json["image_tags"] = tags
    new_json = json.dumps(new_json)
    #new_json = json.loads(new_json)
    #print '----------- New JSON '
    #print new_json
    #new_json = '{"id":366141,"parent_id":null,"board_id":26866,"category_id":36,"user_id":845,"date_added":"2015-03-31 00:55:31","date_modified":"2015-03-31 00:55:32","likes":8,"comments":0,"repins":0,"title":null,"description":"Earthy Minimal Living ","source_id":null,"from":null,"width":676,"height":1185,"image":"\/uploads\/pins\/2015\/03\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","store":"Local","store_host":"{local}","video":0,"background_color":null,"pinned_from":"Uploaded","gift":0,"price":null,"currency_code":null,"gallery":0,"status":1,"public":1,"liked":0,"user_is_follow":0,"board":"Living Room","username":"Pro_MayaPraxis","firstname":"mayaPRAXIS","lastname":"Design + Architecture","pins":25,"boards":8,"user_likes":0,"followers":0,"image_medium":{"image":"http:\/\/dev.houzify.com\/uploads\/pins\/2015\/03\/medium\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","width":236,"height":414},"image_big":{"image":"http:\/\/dev.houzify.com\/uploads\/pins\/2015\/03\/big\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","width":676,"height":1185},"user":{"id":845,"username":"Pro_MayaPraxis","password":"ceb11da7d9d833e059e71f804ac82432","password_new":null,"password_key":null,"email":"vijay@mayapraxis.com","firstname":"mayaPRAXIS","lastname":"Design + Architecture","pins":25,"likes":0,"comments":0,"boards":8,"followers":0,"following":0,"language_id":1,"status":1,"activate_url":null,"avatar_width":200,"avatar_height":208,"avatar":"\/uploads\/users\/2015\/01\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","avatar_store_host":"{local}","avatar_store":"Local","date_added":"2015-01-21 05:08:57","date_modified":"2015-04-20 01:26:17","cover_width":0,"cover_height":0,"cover_top":0,"cover":null,"cover_store_host":null,"cover_store":null,"about":"Headed by Vijay Narnapatti and Dimple Mittal, MayaPraxis works on Architecture and related design fields. ","is_admin":0,"gender":"unsigned","status_send":null,"country_iso_code_3":"IND","website":"http:\/\/www.mayapraxis.biz","search_engines":1,"city":"Bangalore","first_login":1,"send_daily":1,"repins":0,"notification_comment_pin":1,"notification_mentioned":1,"notification_follow_user":1,"notification_like_pin":1,"notification_repin_pin":1,"notification_group_board":1,"notification_news":1,"last_online":"2015-05-15 04:26:20","activity_open":"2015-04-20 01:26:17","avatar_small":{"image":"http:\/\/dev.houzify.com\/uploads\/users\/2015\/01\/small\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","width":60,"height":60},"avatar_medium":{"image":"http:\/\/dev.houzify.com\/uploads\/users\/2015\/01\/medium\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","width":200,"height":200},"cover_image":{"width":986,"height":348,"bits":8,"mime":"image\/jpeg","extension":"jpeg","image":"http:\/\/dev.houzify.com\/uploads\/noimage\/usercovers\/small.jpeg"}}}'
    #print new_json
    writeDB(pin_id, new_json)
    """
    print (findTag('holiday'))
    #print (findTag('abcasjcka'))

if __name__ == '__main__':
    main()

