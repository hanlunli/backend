<html>
    <head>
        <title>Typing test</title>
    </head>
    <body>
    <style>
    .headerbutton {
    border: 1px solid #5f73b8;
    background: #424549;
    color: white;
    width: 270px;
    padding: 15px 20px;
    font-weight: bold;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 15px;
    transition-duration: 0.1s;
    cursor: pointer;
    font-family: serif;
    }
    .headerbutton:hover{
    background:  #7e92d6;
    /* color: rgb(78, 3, 66); */
    }
    body {
    text-align: center;
    padding: 25px;
    background-color: #121212;
    color: #7e92d6;
    font-size: 24px;
    font-weight: bold;
    transition-duration: 0.2s;
   }
    </style>
    <script>
        // You can also use JavaScript to programmatically focus the input element
        const autoFocusInput = document.getElementById("auto-focus-input");
        autoFocusInput.focus();
    </script>
<form action="/inputdata" method = "post">
    <input id="auto-focus-input" autofocus color='grey' name='a' type="text" placeholder="Type Here" style="height: 30px;width: 95%;margin-bottom:50px">
</form>
</body>
</html>