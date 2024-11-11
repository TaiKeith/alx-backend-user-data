# 0x01. Basic authentication
`Back-end` `Authentification`

## Background Context
In this project, we will learn what the authentication process means and implement a **Basic Authentication** on a simple API.

In the industry, you should **not** implement your own Basic authentication system and use a module or framework that doing it for you (like in Python-Flask: [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/)). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

![Image](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2020/5/6ccb363443a8f301bc2bc38d7a08e9650117de7c.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20241111%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241111T095320Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=c266c5d8c7d3dc37dc313527481e82276d580dddd346a86d1dcfa809937ba483)

## Resources
**Read or watch:**
* [REST API Authentication Mechanisms](https://www.youtube.com/watch?v=501dpx2IjGY)
* [Base64 in Python](https://docs.python.org/3.7/library/base64.html)
* [HTTP header Authorization](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
* [Flask](https://palletsprojects.com/projects/flask/)
* [Base64 - concept](https://en.wikipedia.org/wiki/Base64)

## Learning Objectives
* What authentication means
* What Base64 is
* How to encode a string in Base64
* What Basic authentication means
* How to send the Authorization header
