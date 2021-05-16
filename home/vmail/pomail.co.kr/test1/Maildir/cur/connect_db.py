import base64
from io import BytesIO
#import MySQLdb
import eml_parser
import pymysql
# import pymysql


def save_record(sender, receiver, sub, content, attachments, date):
    conn = pymysql.connect(host='pomail.cylslqlklnx0.ap-northeast-2.rds.amazonaws.com', user='root', password='rootoor123', charset='utf8', db='postfix_accounts') #DB 연결
    cur = conn.cursor() #디폴트 커서 생성

    sql = "INSERT INTO inbox_table (sender,receiver,sub,content,attachments,date) VALUES (%s, %s, %s, %s, %s, %s)" % ("'"+str(sender)+"'", "'"+str(receiver)+"'", "'"+str(sub)+"'", "'"+str(content)+"'", "'"+attachments+"'","'"+str(date)+"'")
    cur.execute(sql)
    conn.commit()
    print('rowcount: ', cur.rowcount)

    conn.close() #연결 닫기


with open('1619881539.M847454P1108838.pomail.co.kr,S=3768976,W=3817971:2,S', 'rb') as fhdl:
  raw = fhdl.read()
ep = eml_parser.EmlParser(include_attachment_data = True, include_raw_body = True)
parsed_eml = ep.decode_email('1619881539.M847454P1108838.pomail.co.kr,S=3768976,W=3817971:2,S')

header = parsed_eml.get('header')
body = parsed_eml.get('body')
sender = header.get('from')
receiver = ''.join(header.get('to'))
sub = header.get('subject')
date = header.get('date')
content = body[0].get('content')
attachment = parsed_eml.get('attachment')
attachment = attachment[0].get('raw')
attachment = attachment.decode('UTF-8')

save_record(sender, receiver,sub, content, attachment, date)
#AI
#extensions= ['jpeg','png','jpg']
#for i in range(len(attachment)):
#  if attachment[i].get('extension') in extensions:
#    attachment = attachment[i].get('raw')


