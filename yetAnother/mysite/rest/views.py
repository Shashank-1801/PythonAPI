from django.http import HttpResponse
import urllib2
import json
import base64
import MySQLdb


def index(request):
    return HttpResponse("Invalid page")

def generate_tags(request):
    """
    a./rest/pin/generate_tags?id=<value>
    This API call should update read the pin, extract its image_medium field and use that
    URL to tag the image with its contents.
    """
    id = request.GET.get('id', '')
    pin_id = int(id)
    if(not pin_id):
        return HttpResponse('Please pass a vaild id')
    #if(type(id) != int):
     #   return HttpResponse('Please pass a vaild id as integer')

    #if id is passed as int
    url_json = getData(pin_id)
    url = extractUrl(url_json)
    tags_json = imaggaTags(url)
    tags = extractTags(tags_json)
    new_json = json.loads(url_json)
    new_json["image_tags"] = tags
    new_json = json.dumps(new_json)
    writeDB(pin_id, new_json)
    return HttpResponse(new_json, content_type="application/json")
    #return HttpResponse("This is the rest app --> generate_tags" + str(id))

def tags(request):
    """
    b./rest/pin/tags?id=366141
    This API call should find a pin by its id and return all the tags about the pin in JSON
    format.
    """
    id = request.GET.get('id', '')
    pin_id = int(id)
    if(not pin_id):
        return HttpResponse('Please pass a vaild id')
    #if(type(id) != int):
     #   return HttpResponse('Please pass a vaild id as integer')

    #if id is passed as int
    url_json = getData(pin_id)
    url = extractUrl(url_json)
    tags_json = imaggaTags(url)
    tags = extractTags(tags_json)
    tags = json.dumps(tags)
    return HttpResponse(tags, content_type="application/json")

def find(request):
    """
    c. /rest/pin/find?tag=<value
    This API call should find a pin by using the tag data which is stored and return the
    complete data about a pin in JSON format. It should also include all the tags for that pin in the
    result.
    """
    tag = request.GET.get('tag', '')
    res = findTag(tag)
    return HttpResponse(res, content_type="application/json")



"""
Helper methods that will be used
"""
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

# find tags in the DB
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
            for p in (json.loads(x[0])['image_tags']):
                try:
                    if(tag == str(p['tag'])):
                        result.append(x)
                except:
                    print "Data not found in this row"
    except:
        print "Error in QUERY"

    return result
    # disconnect from server
    db.close()
    print "------------ Disconnected ------------"
