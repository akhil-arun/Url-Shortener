# URL Shortener
I implemented this project using Python as the langauge, and Flask as the
framework. I also made a database using SQLite to keep track of the mappings
from the encoded url to the original url.

## Running the Project
You can run the project from the command line by typing the following command:

```console
akhilarunachalam@Akhils-MacBook-Air-6 URL_Shortener % python3 url.py
```

After typing in the command, the following output will display information such
as where the script is running on the local machine. This url will be used to 
test if the endpoints work as expected. The following is where the project was
running on in my machine. We will be testing the code by pasting the url and the
specified endpoint on a web browser such as Google Chrome to see if the script
works as expected.

```console
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## `encode` Endpoint
This endpoint expects a parameter, `url`, for the url that is expected to be
encoded. If no `url` parameter is passed in, in an error will be thrown.