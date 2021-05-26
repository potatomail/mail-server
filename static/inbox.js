document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
    document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// Send email function
function send_email() {
  // Taking User insertion
  var recipient = document.querySelector('#compose-recipients').value;
  var subject = document.querySelector('#compose-subject').value;
  var body = document.querySelector('#compose-body').value;

    // spliting if more than 1 email
    var recipients  = recipient.split(',')

    //looping over emails
    for (email in recipients){
      fetch('/emails', {
          method: 'POST',
          body: JSON.stringify({
              recipients: recipients[email],
              subject: subject,
              body: body
          })
        })
          .then(response => response.json())
          .then(result => {
            // Print result
           console.log(result);
           if (result['error']){
             document.querySelector('#error_msg').innerHTML =
             `<div class="alert alert-danger" role="alert">
                  ${result.error}
              </div>`;
           }
           else {
              load_mailbox('sent');
           }
        });
    }
}
document.addEventListener('DOMContentLoaded', function(){
  document.querySelector('#submit').addEventListener('click', send_email)
})

// Load emails and pages
function load_mailbox(mailbox) {
  var emails_view = document.querySelector('#emails-view');

  // Show the mailbox and hide other views
  emails_view.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      console.log(emails)
      if(emails.length === 0){
          emails_view.innerHTML += '<p>No emails to see</p>';
      }
      else{
          // Looping over mails
          emails.forEach((element) => {
            // Creating HTML elements to insert email informations
            var mail = document.createElement("div");
            var sender = document.createElement("h5");
            var subject = document.createElement('p');
            var time = document.createElement('p');

            // Inserting mail informations into HTML elements
            sender.innerHTML = element.sender;
            subject.innerHTML = element.subject;
            time.innerHTML = element.timestamp;

            // Appending elements to divs
            emails_view.appendChild(mail);
            mail.appendChild(sender);
            mail.appendChild(subject);
            mail.appendChild(time);

            //Adding class
            mail.classList.add("mail_design")
              console.log(element);
              if(element.read == true){
                mail.style.background = 'white';
              }
              else{
                mail.style.background = '#cccccc';
              }
              mail.addEventListener('click', () => view_email(element.id))
          });

          }
    });
}

function view_email(id) {
  var email_view = document.querySelector('#email-view');

// Show the mail view and hide other views
  email_view.style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);
    // Creating HTML elements to insert email informations
    var upper = document.createElement("div");
    var sender = document.createElement("p");
    var receiver = document.createElement("p");
    var subject = document.createElement('p');
    var time = document.createElement('p');
    var lower = document.createElement("div");
    var body = document.createElement('p');
    var arch = document.createElement('button');
    var rep = document.createElement('button');
    var line = document.createElement('hr');
    // Preventing repetition
    email_view.innerHTML = '';

    // Inserting mail informations into HTML elements
    sender.innerHTML = `<b>From:</b> ${email.sender}`;
    receiver.innerHTML = `<b>To:</b> ${email.recipients}`;
    subject.innerHTML = `<b>Subject:</b> ${email.subject}`;
    time.innerHTML = `<b>Time:</b> ${email.timestamp}`;
    body.innerHTML = `${email.body}`;
    rep.innerText = 'Reply';
    if (email.archived == false){
      arch.innerText = 'Archive';
    }
    else {
      arch.innerText = 'Unarchive';
    }

    // Appending elements to divs
    email_view.appendChild(upper);
    upper.appendChild(sender);
    upper.appendChild(receiver);
    upper.appendChild(subject);
    upper.appendChild(time);
    upper.appendChild(arch);
    upper.appendChild(rep);
    upper.appendChild(line);
    email_view.appendChild(lower);
    lower.appendChild(body);

    //Adding class
    upper.classList.add("upper");
    arch.classList.add("btn","btn-dark");
    rep.classList.add("btn","btn-dark");

    //Specify that it has been readed
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
      read: true
        })
      });
      // Function to Archive and Unarchive
      arch.addEventListener('click', function(){
        if(email.archived == false){
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
            archived: true
              })
            });
          load_mailbox('inbox');
        }
        else {
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
            archived: false
              })
            });
          load_mailbox('inbox');
        }
      });
      rep.addEventListener('click', function() {
        compose_email();
         var re = 'Re: ';
         document.querySelector('#compose-recipients').value = email.sender;
         document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote : ${email.body}`;
         if (email.subject.includes(re)){
            document.querySelector('#compose-subject').value = email.subject;
         }
         else{
           document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
         }

      })
  });
}
