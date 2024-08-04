# Music-subscription-web-application-using-AWS-services

------------------------------------------Description-----------------------------------------------------------------------
Cloud based web application is deployed using AWS services like EC2, Dynamodb,
S3, lambda and API gateway. The music data such as music name, author name, year 
are stored in dynamodb. Author Images are stored in s3 bucket. 

Frontend is built using html and javascript in which Ajax is used to connect with 
AWS lambda through AWS API gateway. AWS lambda is used to access dynamodb, S3 to access data
and transmit the data back to the html webpage which is hosted on AWS EC2 instance.

----------------------------------------------------------------------------------------------------------------------------
Files:
  * index.html - contains login and register webpage which gets and add new data into dynamodb
  * main.html - contains the music subscription list of user and music search results that are retrived from dynamodb
  * lambda_msc_login - lambda code to authenticate the existing user with corresponding dynamodb table
  * lambda_msc_reg - lambda code to to add new user to the corresponding dynamodb table
  * lambda_msc_main - lambda code to add, remove subscription music and query music details by year, title and author name
  * data.json - contains data of music title, author, image url and year which is loaded onto dynamodb table
  * readme file

----------------------------------------------------------------------------------------------------------------------------

    
