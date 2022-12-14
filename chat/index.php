<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Чат</title>
    <style>
        .chat_window{
            height: 600px;
            width: 451px;
            border: 2px double grey;
            margin-left: auto;
            margin-right: auto;
            overflow-x: none;
            overflow-y: auto;
            border-radius: 3px;
        }

        .user_txt{
            height: 45px;
            width: 446px;
            margin-left: 245px;
            margin-right: auto;
            font-size: 20px;
            
        }
        .user_name{
            height: 45px;
            width: 446px;
            margin-left: 245px;
            margin-right: auto;
            font-size: 20px;    
        }
        .but{
            height: 45px;
            width: 455px;
            margin-left: 245px;
            margin-right: auto;
            font-size: 20px;    
        }
    </style>
    <script type="text/javascript" src="/app.js"></script>
</head>
<body onload="chat()">
    <div class="chat_window" id="chat"></div>
    <input class="user_name" type="text" id="name" placeholder="Name">
    <input class="user_txt" type="text" id="message" placeholder="Message"><br>
    <input class="but" type="button" id="message" value="SEND" onclick="addMessage();">
</body>
</html>