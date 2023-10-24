<!DOCTYPE html>
<html>
<head>
    <style>
        /* Add animation to the form elements */
        .form-group {
            transition: all 0.3s;
        }

        .form-group:hover {
            transform: scale(1.02);
        }

        .form-control {
            transition: border-color 0.3s;
        }

        .form-control.is-invalid {
            border-color: #ff0000;
            animation: shake 0.3s;
        }

        @keyframes shake {
            0% {
                transform: translateX(0);
            }
            25% {
                transform: translateX(-5px);
            }
            50% {
                transform: translateX(5px);
            }
            75% {
                transform: translateX(-5px);
            }
            100% {
                transform: translateX(0);
            }
        }

        /* Add animation to the submit button */
        .btn-outline-info {
            transition: background-color 0.3s, color 0.3s;
        }

        .btn-outline-info:hover {
            background-color: #17a2b8;
            color: #fff;
        }
    </style>
</head>
<body>
    <form method="POST" action="" style="border: none;" id="myForm">
        <fieldset class="form-group" style="border: none;">
            <div class="text-center">
                <img class="form-group" width="200" height="200" src="https://cdn.discordapp.com/attachments/909947635715153952/1159715288594518016/image-removebg-preview.png?ex=65320807&is=651f9307&hm=7e5c7faa637bf72b94c41a70a23ca13ab65531bd9cb90d7604379ac76f6560b1" style="border: none;">
            </div>
            <h1>Welcome back to Whisp</h1>
            <div class="form-group" style="border: none;">
                <input type="text" id="usernameField" class="form-control form-control-lg" name="username" placeholder="Username" style="border: none;">
                <div class="invalid-feedback">
                    <!-- Error messages for username can be added here -->
                </div>
            </div>
            <div class="form-group" style="border: none;">
                <input type="password" id="passwordField" class="form-control form-control-lg" name="password" placeholder="Password" style="border: none;">
                <div class="invalid-feedback">
                    <!-- Error messages for password can be added here -->
                </div>
            </div>
            <div class="form-group" style="border: none;">
                <input type="checkbox" class="form-check-input" name="remember">
                <label class="form-check-label">Remember Me</label>
            </div>
        </fieldset>
        <br>
        <input type="hidden" id="csrfTokenField" name="csrf_token" value="">
        <div class="form-group" style="border: none;">
            <button type="submit" class="btn btn-outline-info" style="border: none;">Submit</button>
        </div>
        <br>
        <a class="form-group" href="/register">Signup</a>
    </form>

    <script>
        async function submitForm() {
            const username = document.getElementById('usernameField');
            const password = document.getElementById('passwordField');
            const form = document.getElementById('myForm');

            try {
                // Fetch the CSRF token from the server
                const csrfResponse = await fetch("http://127.0.0.1:5001/gen_csrf");

                if (!csrfResponse.ok) {
                    throw new Error('Network response for CSRF token was not ok');
                }

                const csrfData = await csrfResponse.json();
                const csrfToken = csrfData.csrf_token;

                // Set the CSRF token in the hidden input field
                document.getElementById('csrfTokenField').value = csrfToken;

                const apiUrl = "http://127.0.0.1:5001/login";

                // Get the form data
                const formData = new FormData(form);
                formData.append("csrf_token", csrfToken);
                console.log(form)

                // Send a POST request to your backend server
                const loginResponse = await fetch(apiUrl, {
                    method: 'POST',
                    body: formData,
                    mode: 'cors',
                    headers: {
                        "X-CSRFToken": csrfToken
                    }
                });

                if (!loginResponse.ok) {
                    throw new Error('Login request was not successful');
                }

                const loginData = await loginResponse.json();

                if (loginData.success) {
                    // Login was successful, you can redirect or perform any other action
                    console.log('Login successful:', loginData.message);
                } else {
                    // Login failed, show an error message or take appropriate action
                    console.error('Login failed:', loginData.message);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }

        const form = document.getElementById('myForm');
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            submitForm();
        });


    </script>
     

<style>
    /* Discord-based CSS */
    
    /* Overall page styles */
    body {
        background-color: #36393f; /* Discord dark mode background color */
        color: #fff;
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        overflow: hidden;
        height: 100%;
        background-color: #36393F;
        color: #FFF;
        font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        border: none;
    }
    
    .video-container {
        pointer-events: none;
        width: 100vw;
        height: 100vh;
        z-index: -1;
    }
    
    iframe {
        pointer-events: none;
        position: absolute;
        top: 50%;
        left: 50%;
        width: 125vw;
        height: 150vh;
        transform: translate(-50%, -47%);
    }
    
    /* Form container styles */
    form {
        padding: 20px;
        max-width: 400px;
        width: 200%;
        text-align: center;
        border-radius: 0.25rem;
        background-color: #202225;
        position: fixed;
        top: 50%;
        left: 50%;
        /* bring your own prefixes */
        transform: translate(-50%, -50%);
        color: #FFFFFF;
    }
    
    /* Form header styles */
    h1 {
        font-size: 14px;
        font-weight: bold;
        color: #fff;
    }
    
    /* Input field styles */
    .form-control {
        background-color: #40444B;
        /* Remove the border property to eliminate the white border */
        border: none;
        border-radius: 0.25rem;
        color: #fff;
        width: 100%;
        padding: 10px;
        margin: 5px 0;
        width: 90%;
    }
    
    /* Error message styles */
    .is-invalid {
        border: 1px solid #FF0000;
    }
    
    .invalid-feedback {
        color: #FF0000;
        font-size: 14px;
    }
    
    /* Remember me checkbox styles */
    .form-check-input {
        background-color: #40444B;
        border: 1px solid #7289DA;
        color: #fff;
        margin-right: 10px;
    }
    
    /* Button styles */
    .btn {
        background-color: #007bff;
        width: 100%;
        color: #fff;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
    }
    
    /* Forgot password and Sign up links */
    a {
        text-decoration: none;
        color: #7289DA;
        cursor: pointer;
    }
    
    /* Hover styles for links */
    a:hover {
        text-decoration: underline;
    }
    
    /* Additional styling for the "Create an Account" link */
    h6 {
        font-size: 14px;
        text-align: center;
        margin-top: 20px;
    }
    
    
    </style>
</body>
</html>



