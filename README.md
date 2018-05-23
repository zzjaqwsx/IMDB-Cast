# IMDB-Cast
This project attempts to create an automated scripting project that functions as a TimePlay program
(If you go to Cineplex often, you should probably know that TimePlay throws audiance all kinds of questions regarding latest movies and correct answer are rewarded with scene points)

This project will primirily utilize the framework provided by OpenCV, FFmpeg, openface under Linux runtime environment.
There are four important phases to the workflow:
1. FFmpeg will extract frames from each film in ./movie directory. There will be a thread instantiated to handle the process for each film
2. Cascaded recognizer will be programmed to take the output frames from the previous step and gives the face detection results
3. Similar faces will be categoried together under one actor/actress's name. This step relies on the computing algorithm powered by openface framework.
4. Django and Postgres will handle the necessary data output from previous computations and display the result on a web application.
