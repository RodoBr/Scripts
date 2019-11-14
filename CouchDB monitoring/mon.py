import requests
import re
import time

db_login = "admin"
db_pass = "1234"
node = "couchdb1.rodo.lan"

r = requests.get("http://"+db_login+":"+db_pass+"@"+node+":5984/_node/couchdb@"+node+"/_stats/couchdb/httpd_request_methods")

tmp = str(r.content)

get1 = re.search('"GET":{"value":(.*?),', tmp)
get1 = get1.group(1)
get1 = int(get1)

head1 = re.search('"HEAD":{"value":(.*?),', tmp)
head1 = head1.group(1)
head1 = int(head1)

post1 = re.search('"POST":{"value":(.*?),', tmp)
post1 = post1.group(1)
post1 = int(post1)

put1 = re.search('"PUT":{"value":(.*?),', tmp)
put1 = put1.group(1)
put1 = int(put1)

delete1 = re.search('"DELETE":{"value":(.*?),', tmp)
delete1 = delete1.group(1)
delete1 = int(delete1)

options1 = re.search('"OPTIONS":{"value":(.*?),', tmp)
options1 = options1.group(1)
options1 = int(options1)

copy1 = re.search('"COPY":{"value":(.*?),', tmp)
copy1 = copy1.group(1)
copy1 = int(copy1)

time.sleep(10)

r = requests.get("http://"+db_login+":"+db_pass+"@"+node+":5984/_node/couchdb@"+node+"/_stats/couchdb/httpd_request_methods")

tmp = str(r.content)

get2 = re.search('"GET":{"value":(.*?),', tmp)
get2 = get2.group(1)
get2 = int(get2)

head2 = re.search('"HEAD":{"value":(.*?),', tmp)
head2 = head2.group(1)
head2 = int(head2)

post2 = re.search('"POST":{"value":(.*?),', tmp)
post2 = post2.group(1)
post2 = int(post2)

put2 = re.search('"PUT":{"value":(.*?),', tmp)
put2 = put2.group(1)
put2 = int(put2)

delete2 = re.search('"DELETE":{"value":(.*?),', tmp)
delete2 = delete2.group(1)
delete2 = int(delete2)

options2 = re.search('"OPTIONS":{"value":(.*?),', tmp)
options2 = options2.group(1)
options2 = int(options2)

copy2 = re.search('"COPY":{"value":(.*?),', tmp)
copy2 = copy2.group(1)
copy2 = int(copy2)

get_per_sec = (get2 - get1) / 10
head_per_sec = (head2 - head1) / 10
post_per_sec = (post2 - post1) / 10
put_per_sec = (put2 - put1) / 10
delete_per_sec = (delete2 - delete1) / 10
options_per_sec = (options2 - options1) / 10
copy_per_sec = (copy2 - copy1) / 10
total_per_sec = get_per_sec + head_per_sec + post_per_sec + put_per_sec + delete_per_sec + options_per_sec + copy_per_sec

get_per_sec = str(get_per_sec)
head_per_sec = str(head_per_sec)
post_per_sec = str(post_per_sec)
put_per_sec = str(put_per_sec)
delete_per_sec = str(delete_per_sec)
options_per_sec = str(options_per_sec)
copy_per_sec = str(copy_per_sec)
total_per_sec = str(total_per_sec)

print("total req/s:"+total_per_sec+" GET:"+get_per_sec+"   HEAD:"+head_per_sec+"   POST:"+post_per_sec+"   PUT:"+put_per_sec+"   DELETE:"+delete_per_sec+"   OPTIONS:"+options_per_sec+"   COPY:"+copy_per_sec+" | total_requests="+total_per_sec+"/s;150;250;0;500 get_requests="+get_per_sec+"/s;150;250;0;500 head_requests="+head_per_sec+"/s;150;250;0;500 post_requests="+post_per_sec+"/s;150;250;0;500 put_requests="+put_per_sec+"/s;150;250;0;500 delete_requests="+delete_per_sec+"/s;150;250;0;500 options_requests="+options_per_sec+"/s;150;250;0;500 copy_requests="+copy_per_sec+"/s;150;250;0;500")
