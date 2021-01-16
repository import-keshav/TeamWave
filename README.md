# TeamWave
Backend Assignment

<h4> TechStack Used</h4>
1. Python (Programming Language)<br>
2. Django (Web Framework)<br>
3. Sqlite (Database)<br>


<h5> API's Postman ScreenShots</h5>
<h6> Search API (POST Request)</h6>
API for searching questions in StackOverflow
<img src="https://user-images.githubusercontent.com/34139754/104820242-8ca6b000-5859-11eb-911d-762bf7bdca0a.png">

| Status  |   Time  |    Size     |
| ------- | ------- | ------------|
| 200 OK  |   2.03s |    20.23 KB |


<h5> How to setup and run locally </h5>
<p>
  1. Clone the Repository <br>
  2. <a href="https://www.geeksforgeeks.org/python-virtual-environment/"> Create a Activate Python Virtual Environment </a></h5><br>
  3. After activating the virtual enviornment, redirect to project base directory. <br>
  4. Run the following command for installing dependencies.
</p>

    $ pip3 install -r requirements.txt

<br>
  5. Now direct to TeamWave folder for starting the django server.

    $ cd TeamWave

<br>
  6. Now before running the server, we have to setup database, so run.
 
    $ python3 manage.py migrate

<br>
  7. Now run the following command for starting the server

    $ python3 manage.py runserver

<br>

Now run the following api described in the above Postman image.
<br>

