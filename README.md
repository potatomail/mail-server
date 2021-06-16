# POMAIL
- Sensitive information detection and automatic encryption services in e-mail using AI

## Overview
- Ewha Woman's University cyber security capstone project
- 20.09 ~ 21.06

Most people are probably using email services. However, hacking attempts at each portal site like Naver, Google are frequent, and there are quite a few cases of actual leaks. 
We focused on the email service on the portal site. Due to the leakage of personal information, we have become aware of the possibility of leakage of email information such as persual or deletion of personal emails without permission.

### Threat model
The main threat model we assume is that the attacker has access to the incoming mailbox and a lunchtime attack.
It is limited to cases where the recipient's account is exposed through various hacking methods, causing personal information infringement.

### Why did we build our own server?
In order to provide security services that correspond to our assumed threat model, we need to access the db on the mail server and encrypt/decrypt the original file. 
However, if we use the API of gmail and Naver mail, we cannot directly access the DB of the platform. 
Therefore, we have established our own mail server to explain the concept of our service and will add deletion recommendations or provide solutions to improve compatibility 
with existing mail.

## Mail server
![image](https://user-images.githubusercontent.com/58061467/122188254-bf1d0d80-ceca-11eb-9999-663816c48b71.png)
![image](https://user-images.githubusercontent.com/52912896/122201479-09a48700-ced7-11eb-9d8b-c0ab45a106f7.png)

- Linux CentOS
- Postfix, Dovecot
- protocol : SMTP, IMAP
- DB : RDS
- Django

## AI Models
#### Datasets
- 주민등록증, 학생증, 운전면허증, 그 외 데이터 각 2000장씩
![image](https://user-images.githubusercontent.com/58061467/122189335-d14b7b80-cecb-11eb-900b-7eabf9aa7bb8.png)

#### Models
- CNN

#### Server
- Flask

## Process
![image](https://user-images.githubusercontent.com/52912896/122201725-4d978c00-ced7-11eb-9c16-324f33b5d978.png)
![image](https://user-images.githubusercontent.com/58061467/122189747-28515080-cecc-11eb-9837-fa1c2f1537cd.png)
1. Use Watchdog to detect real-time email reception
2. Parses the received eml file when mail is received.
3. Among them, if the attached file is an image, send it to the AI server to determine whether it is sensitive information.
4. If it is sensitive information, encrypt the secondary password entered when signing up as a key and save it in the DB.
5. After that, you can check the original file by decrypting it by entering the secondary password when viewing the sensitive attachment.

## Prototype
[![Video Label](http://img.youtube.com/vi/GmYDR-eOB4E/0.jpg)](https://youtu.be/GmYDR-eOB4E?t=0s)
- Click the image

