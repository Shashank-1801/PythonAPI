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
import urllib
import json
import base64
import MySQLdb


# retrive the Data from Houzify server as per the id provided
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
    print p
    print "----------- URL Extracted "
    return p

# send the url ti Imagga server to get back JSON full of tags
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
    print json_response
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
    print results
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
    if (data == None):
        #need to insert data
        sql_insert = 'INSERT INTO pin_extension (pin_id, tag) VALUES (' + pin_id + ',' + new_json_data + ')'
        try:
           # Execute the SQL command
           cursor.execute(sql_insert)
           # Commit your changes in the database
           db.commit()
        except:
           # Rollback in case there is any error
           db.rollback()
    else:
        #need to update data
        sql_update = 'UPDATE pin_extension SET tag="' + new_json_data +'" WHERE pin_id=' + str(pin_id)
        try:
           # Execute the SQL command
           cursor.execute(sql_update)
           # Commit your changes in the database
           db.commit()
        except:
           # Rollback in case there is any error
           db.rollback()



    # disconnect from server
    db.close()
    print "------------ Disconnected ------------"

def main():
    """
    url_json = getData(366141)
    jj = '{"id":366141,"parent_id":null,"board_id":26866,"category_id":36,"user_id":845,"date_added":"2015-03-31 00:55:31","date_modified":"2015-03-31 00:55:32","likes":8,"comments":0,"repins":0,"title":null,"description":"Earthy Minimal Living ","source_id":null,"from":null,"width":676,"height":1185,"image":"\/uploads\/pins\/2015\/03\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","store":"Local","store_host":"{local}","video":0,"background_color":null,"pinned_from":"Uploaded","gift":0,"price":null,"currency_code":null,"gallery":0,"status":1,"public":1,"liked":0,"user_is_follow":0,"board":"Living Room","username":"Pro_MayaPraxis","firstname":"mayaPRAXIS","lastname":"Design + Architecture","pins":25,"boards":8,"user_likes":0,"followers":0,"image_medium":{"image":"http:\/\/dev.houzify.com\/uploads\/pins\/2015\/03\/medium\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","width":236,"height":414},"image_big":{"image":"http:\/\/dev.houzify.com\/uploads\/pins\/2015\/03\/big\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","width":676,"height":1185},"user":{"id":845,"username":"Pro_MayaPraxis","password":"ceb11da7d9d833e059e71f804ac82432","password_new":null,"password_key":null,"email":"vijay@mayapraxis.com","firstname":"mayaPRAXIS","lastname":"Design + Architecture","pins":25,"likes":0,"comments":0,"boards":8,"followers":0,"following":0,"language_id":1,"status":1,"activate_url":null,"avatar_width":200,"avatar_height":208,"avatar":"\/uploads\/users\/2015\/01\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","avatar_store_host":"{local}","avatar_store":"Local","date_added":"2015-01-21 05:08:57","date_modified":"2015-04-20 01:26:17","cover_width":0,"cover_height":0,"cover_top":0,"cover":null,"cover_store_host":null,"cover_store":null,"about":"Headed by Vijay Narnapatti and Dimple Mittal, MayaPraxis works on Architecture and related design fields. ","is_admin":0,"gender":"unsigned","status_send":null,"country_iso_code_3":"IND","website":"http:\/\/www.mayapraxis.biz","search_engines":1,"city":"Bangalore","first_login":1,"send_daily":1,"repins":0,"notification_comment_pin":1,"notification_mentioned":1,"notification_follow_user":1,"notification_like_pin":1,"notification_repin_pin":1,"notification_group_board":1,"notification_news":1,"last_online":"2015-05-15 04:26:20","activity_open":"2015-04-20 01:26:17","avatar_small":{"image":"http:\/\/dev.houzify.com\/uploads\/users\/2015\/01\/small\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","width":60,"height":60},"avatar_medium":{"image":"http:\/\/dev.houzify.com\/uploads\/users\/2015\/01\/medium\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","width":200,"height":200},"cover_image":{"width":986,"height":348,"bits":8,"mime":"image\/jpeg","extension":"jpeg","image":"http:\/\/dev.houzify.com\/uploads\/noimage\/usercovers\/small.jpeg"}}}'
    url = extractUrl(url_json)
    tags_json = imaggaTags(url)
    #url_json = '{"id":366141,"parent_id":null,"board_id":26866,"category_id":36,"user_id":845,"date_added":"2015-03-31 00:55:31","date_modified":"2015-03-31 00:55:32","likes":8,"comments":0,"repins":0,"title":null,"description":"Earthy Minimal Living ","source_id":null,"from":null,"width":676,"height":1185,"image":"\/uploads\/pins\/2015\/03\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","store":"Local","store_host":"{local}","video":0,"background_color":null,"pinned_from":"Uploaded","gift":0,"price":null,"currency_code":null,"gallery":0,"status":1,"public":1,"liked":0,"user_is_follow":0,"board":"Living Room","username":"Pro_MayaPraxis","firstname":"mayaPRAXIS","lastname":"Design + Architecture","pins":25,"boards":8,"user_likes":0,"followers":0,"image_medium":{"image":"http:\/\/dev.houzify.com\/uploads\/pins\/2015\/03\/medium\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","width":236,"height":414},"image_big":{"image":"http:\/\/dev.houzify.com\/uploads\/pins\/2015\/03\/big\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","width":676,"height":1185},"user":{"id":845,"username":"Pro_MayaPraxis","password":"ceb11da7d9d833e059e71f804ac82432","password_new":null,"password_key":null,"email":"vijay@mayapraxis.com","firstname":"mayaPRAXIS","lastname":"Design + Architecture","pins":25,"likes":0,"comments":0,"boards":8,"followers":0,"following":0,"language_id":1,"status":1,"activate_url":null,"avatar_width":200,"avatar_height":208,"avatar":"\/uploads\/users\/2015\/01\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","avatar_store_host":"{local}","avatar_store":"Local","date_added":"2015-01-21 05:08:57","date_modified":"2015-04-20 01:26:17","cover_width":0,"cover_height":0,"cover_top":0,"cover":null,"cover_store_host":null,"cover_store":null,"about":"Headed by Vijay Narnapatti and Dimple Mittal, MayaPraxis works on Architecture and related design fields. ","is_admin":0,"gender":"unsigned","status_send":null,"country_iso_code_3":"IND","website":"http:\/\/www.mayapraxis.biz","search_engines":1,"city":"Bangalore","first_login":1,"send_daily":1,"repins":0,"notification_comment_pin":1,"notification_mentioned":1,"notification_follow_user":1,"notification_like_pin":1,"notification_repin_pin":1,"notification_group_board":1,"notification_news":1,"last_online":"2015-05-15 04:26:20","activity_open":"2015-04-20 01:26:17","avatar_small":{"image":"http:\/\/dev.houzify.com\/uploads\/users\/2015\/01\/small\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","width":60,"height":60},"avatar_medium":{"image":"http:\/\/dev.houzify.com\/uploads\/users\/2015\/01\/medium\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","width":200,"height":200},"cover_image":{"width":986,"height":348,"bits":8,"mime":"image\/jpeg","extension":"jpeg","image":"http:\/\/dev.houzify.com\/uploads\/noimage\/usercovers\/small.jpeg"}}}'
    #tags_json = '{"results": [{"image": "http://t2.gstatic.com/images?q=tbn:ANd9GcRk9utIiZ5hmk5t5z8ekdt-yYbJWnDU9ya8g5RMtywsfKUR62fy", "tags": [{"confidence": 47.08686082491829, "tag": "sunset"}, {"confidence": 46.91363553498501, "tag": "sky"}, {"confidence": 43.1490476368859, "tag": "sun"}, {"confidence": 41.31448345135119, "tag": "landscape"}, {"confidence": 39.85160210879683, "tag": "clouds"}, {"confidence": 34.87621126919097, "tag": "sunrise"}, {"confidence": 26.95126834903799, "tag": "horizon"}, {"confidence": 25.39227343467552, "tag": "dusk"}, {"confidence": 25.121825381986355, "tag": "cloud"}, {"confidence": 25.117566939543636, "tag": "atmosphere"}, {"confidence": 24.639395035263394, "tag": "orange"}, {"confidence": 23.299212999609274, "tag": "canyon"}, {"confidence": 22.221775911300284, "tag": "scenery"}, {"confidence": 21.110208770363066, "tag": "water"}, {"confidence": 19.29756985801013, "tag": "silhouette"}, {"confidence": 19.147337833859655, "tag": "morning"}, {"confidence": 19.069485433694236, "tag": "outdoor"}, {"confidence": 18.156676965357235, "tag": "travel"}, {"confidence": 17.81546056254988, "tag": "scenic"}, {"confidence": 17.7415730286068, "tag": "summer"}, {"confidence": 17.381986353336913, "tag": "tree"}, {"confidence": 17.238309887860453, "tag": "sunlight"}, {"confidence": 17.212335477657813, "tag": "dawn"}, {"confidence": 17.03842672656182, "tag": "sea"}, {"confidence": 16.54796046224877, "tag": "evening"}, {"confidence": 16.295010473003995, "tag": "color"}, {"confidence": 15.900206879950384, "tag": "natural"}, {"confidence": 15.852309043192724, "tag": "light"}, {"confidence": 15.63183002323272, "tag": "valley"}, {"confidence": 15.250365236239915, "tag": "environment"}, {"confidence": 14.863055702690989, "tag": "reflection"}, {"confidence": 14.369281550702652, "tag": "forest"}, {"confidence": 13.9538244181338, "tag": "mountain"}, {"confidence": 13.761463301778742, "tag": "scene"}, {"confidence": 13.699128734347292, "tag": "outdoors"}, {"confidence": 13.672269586632675, "tag": "season"}, {"confidence": 13.63593980099606, "tag": "vacation"}, {"confidence": 13.462789430591735, "tag": "ravine"}, {"confidence": 13.37747130212052, "tag": "beach"}, {"confidence": 12.936557238314355, "tag": "weather"}, {"confidence": 12.903046235463973, "tag": "star"}, {"confidence": 12.886591930474983, "tag": "lake"}, {"confidence": 12.875298999093573, "tag": "tranquil"}, {"confidence": 12.802573983504171, "tag": "tourism"}, {"confidence": 12.589970843876468, "tag": "yellow"}, {"confidence": 12.391428462916986, "tag": "trees"}, {"confidence": 12.355580732528226, "tag": "ocean"}, {"confidence": 12.22935473922548, "tag": "peaceful"}, {"confidence": 12.155369227122982, "tag": "mountains"}, {"confidence": 11.674272030439779, "tag": "sunshine"}, {"confidence": 11.249414259115508, "tag": "colorful"}, {"confidence": 11.069023486938498, "tag": "coast"}, {"confidence": 10.966675354557767, "tag": "cloudscape"}, {"confidence": 10.853648195621457, "tag": "park"}, {"confidence": 10.725535985046443, "tag": "sunny"}, {"confidence": 10.709447008690637, "tag": "bright"}, {"confidence": 10.344879304838486, "tag": "twilight"}, {"confidence": 10.240432656186947, "tag": "dramatic"}, {"confidence": 9.84525648861287, "tag": "rock"}, {"confidence": 9.694405283698645, "tag": "day"}, {"confidence": 9.659825173981247, "tag": "dark"}, {"confidence": 9.329925518574102, "tag": "sand"}, {"confidence": 9.28491959255318, "tag": "autumn"}, {"confidence": 9.269653895300475, "tag": "heaven"}, {"confidence": 8.920511371977048, "tag": "calm"}, {"confidence": 8.906084744043797, "tag": "spring"}, {"confidence": 8.780604274596508, "tag": "national"}, {"confidence": 8.51244695082663, "tag": "river"}, {"confidence": 8.379716408573156, "tag": "bay"}, {"confidence": 8.37398619155679, "tag": "golden"}, {"confidence": 8.212503105189432, "tag": "relax"}, {"confidence": 8.112, "tag": "celestial body"}, {"confidence": 8.0861978775367, "tag": "peace"}, {"confidence": 8.078925127778374, "tag": "countryside"}, {"confidence": 7.817169039447593, "tag": "night"}, {"confidence": 7.6513470653182845, "tag": "storm"}, {"confidence": 7.568244797074881, "tag": "grass"}, {"confidence": 7.505833220192228, "tag": "coastline"}, {"confidence": 7.47001465320063, "tag": "cloudy"}, {"confidence": 7.467940384735166, "tag": "winter"}, {"confidence": 7.3020540009148265, "tag": "wood"}]}]}'
    tags = extractTags(tags_json)
    new_json = json.loads(url_json)
    new_json["image_tags"] = tags
    new_json = json.dumps(new_json)
    new_json = json.loads(new_json)
    print '----------- New JSON '
    print new_json
    """
    new_json = '{"id":366141,"parent_id":null,"board_id":26866,"category_id":36,"user_id":845,"date_added":"2015-03-31 00:55:31","date_modified":"2015-03-31 00:55:32","likes":8,"comments":0,"repins":0,"title":null,"description":"Earthy Minimal Living ","source_id":null,"from":null,"width":676,"height":1185,"image":"\/uploads\/pins\/2015\/03\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","store":"Local","store_host":"{local}","video":0,"background_color":null,"pinned_from":"Uploaded","gift":0,"price":null,"currency_code":null,"gallery":0,"status":1,"public":1,"liked":0,"user_is_follow":0,"board":"Living Room","username":"Pro_MayaPraxis","firstname":"mayaPRAXIS","lastname":"Design + Architecture","pins":25,"boards":8,"user_likes":0,"followers":0,"image_medium":{"image":"http:\/\/dev.houzify.com\/uploads\/pins\/2015\/03\/medium\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","width":236,"height":414},"image_big":{"image":"http:\/\/dev.houzify.com\/uploads\/pins\/2015\/03\/big\/6b2a9998e3c301b60bdd206b6350cdb9.jpeg","width":676,"height":1185},"user":{"id":845,"username":"Pro_MayaPraxis","password":"ceb11da7d9d833e059e71f804ac82432","password_new":null,"password_key":null,"email":"vijay@mayapraxis.com","firstname":"mayaPRAXIS","lastname":"Design + Architecture","pins":25,"likes":0,"comments":0,"boards":8,"followers":0,"following":0,"language_id":1,"status":1,"activate_url":null,"avatar_width":200,"avatar_height":208,"avatar":"\/uploads\/users\/2015\/01\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","avatar_store_host":"{local}","avatar_store":"Local","date_added":"2015-01-21 05:08:57","date_modified":"2015-04-20 01:26:17","cover_width":0,"cover_height":0,"cover_top":0,"cover":null,"cover_store_host":null,"cover_store":null,"about":"Headed by Vijay Narnapatti and Dimple Mittal, MayaPraxis works on Architecture and related design fields. ","is_admin":0,"gender":"unsigned","status_send":null,"country_iso_code_3":"IND","website":"http:\/\/www.mayapraxis.biz","search_engines":1,"city":"Bangalore","first_login":1,"send_daily":1,"repins":0,"notification_comment_pin":1,"notification_mentioned":1,"notification_follow_user":1,"notification_like_pin":1,"notification_repin_pin":1,"notification_group_board":1,"notification_news":1,"last_online":"2015-05-15 04:26:20","activity_open":"2015-04-20 01:26:17","avatar_small":{"image":"http:\/\/dev.houzify.com\/uploads\/users\/2015\/01\/small\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","width":60,"height":60},"avatar_medium":{"image":"http:\/\/dev.houzify.com\/uploads\/users\/2015\/01\/medium\/23d43e56fcd1c40bf262fb1b3332579b.jpeg","width":200,"height":200},"cover_image":{"width":986,"height":348,"bits":8,"mime":"image\/jpeg","extension":"jpeg","image":"http:\/\/dev.houzify.com\/uploads\/noimage\/usercovers\/small.jpeg"}}}'
    print len(new_json)
    #writeDB(21, new_json)
    pass

if __name__ == '__main__':
    main()

