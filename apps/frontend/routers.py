from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter(prefix="/frontend", tags=["frontend"])


@router.get("/", response_class=HTMLResponse)
def register_view():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Create User</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f9;
        }
        .form-container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
        }
        h2 {
            text-align: center;
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #007BFF;
            border: none;
            color: white;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .redirect-link {
            text-align: center;
            margin-top: 10px;
        }
    </style>
</head>
<body>

<div class="form-container">
    <h2>Create User</h2>
    <form id="userForm">
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit">Create Account</button>
    </form>
    <div id="response" style="margin-top: 20px; text-align: center;"></div>
    <div class="redirect-link">
        <p>Already have an account? <a href="/frontend/login">Login here</a></p>
    </div>
</div>

<script>
    document.getElementById('userForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the form from reloading the page

        // Gather the input data
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Prepare the POST request for creating a user
        const userResponse = await fetch('http://127.0.0.1:8000/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const responseDiv = document.getElementById('response');

        if (userResponse.ok) {
            // If user creation is successful, proceed to login
            const loginResponse = await fetch('http://127.0.0.1:8000/users/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            if (loginResponse.ok) {
                const tokenData = await loginResponse.json();
                // Save the JWT token to local storage
                localStorage.setItem('jwt_token', tokenData.token);

                // Redirect to the messages page
                window.location.href = '/frontend/messages';
            } else {
                const loginError = await loginResponse.json();
                responseDiv.innerHTML = `<p style="color:red;">Login Error: ${loginError.detail || 'Something went wrong!'}</p>`;
            }
        } else {
            const errorData = await userResponse.json();
            if (userResponse.status === 401) {
                responseDiv.innerHTML = `<p style="color:red;">Error: Username already taken!</p>`;
            } else {
                responseDiv.innerHTML = `<p style="color:red;">Error: ${errorData.detail || 'Something went wrong!'}</p>`;
            }
        }
    });
</script>

</body>
</html>
"""


@router.get("/login", response_class=HTMLResponse)
def login_view():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f9;
        }
        .form-container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
        }
        h2 {
            text-align: center;
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #007BFF;
            border: none;
            color: white;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>

<div class="form-container">
    <h2>Login</h2>
    <form id="loginForm">
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit">Login</button>
    </form>
    <div id="response" style="margin-top: 20px; text-align: center;"></div>
</div>

<script>
    document.getElementById('loginForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the form from reloading the page

        // Gather the input data
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Prepare the POST request for login
        const response = await fetch('http://127.0.0.1:8000/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const responseDiv = document.getElementById('response');
        
        if (response.ok) {
            const tokenData = await response.json();
            // Save the JWT token to local storage
            localStorage.setItem('jwt_token', tokenData.token);
            
            // Redirect to the messages page
            window.location.href = '/frontend/messages';
        } else {
            const errorData = await response.json();
            responseDiv.innerHTML = `<p style="color:red;">Error: ${errorData.detail || 'Invalid username or password!'}</p>`;
        }
    });
</script>

</body>
</html>
"""


@router.get("/messages", response_class=HTMLResponse)
def messages_view():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Application</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            height: 100vh;
            background-color: #f4f4f9;
        }
        .chat-container {
            display: flex;
            width: 100%;
            height: 100vh;
        }
        aside.user-list {
            width: 25%;
            background-color: #2c3e50;
            color: white;
            overflow-y: auto;
            padding: 20px;
        }
        aside.user-list ul {
            list-style-type: none;
            padding: 0;
        }
        aside.user-list li {
            padding: 10px;
            margin: 10px 0;
            cursor: pointer;
            background-color: #34495e;
            border-radius: 5px;
        }
        aside.user-list li:hover {
            background-color: #1abc9c;
        }
        main.chat-window {
            width: 75%;
            display: flex;
            flex-direction: column;
            padding: 20px;
        }
        main.chat-window #messages {
            flex: 1;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 20px;
            background-color: white;
        }
        .message {
            margin: 10px 0;
        }
        .message.sent {
            text-align: right;
        }
        .message.received {
            text-align: left;
        }
        main.chat-window form {
            display: flex;
            justify-content: space-between;
        }
        main.chat-window input[type="text"] {
            width: 80%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        main.chat-window button {
            width: 18%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        main.chat-window button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>

<div class="chat-container">
    <!-- User List -->
    <aside class="user-list">
        <h2>Users</h2>
        <ul id="users"></ul>
    </aside>

    <!-- Chat Window -->
    <main class="chat-window">
        <h2>Chat with: <span id="chat-with">Select a user</span></h2>
        <div id="messages"></div>
        <form id="message-form">
            <input type="text" id="message-input" placeholder="Type your message..." required>
            <button type="submit">Send</button>
        </form>
    </main>
</div>

<script>
    let selectedUserId = null;
    let websocket = null;

    // Function to retrieve the Bearer token from local storage
    function getAuthToken() {
        return 'Bearer ' + localStorage.getItem('jwt_token');
    }

    // Function to fetch the list of users
    async function fetchUsers() {
        const response = await fetch('http://127.0.0.1:8000/users/chat_users', {
            headers: {
                'Authorization': getAuthToken()
            }
        });
        if (response.ok) {
            const users = await response.json();
            populateUserList(users);
        } else {
            console.error('Failed to fetch users');
        }
    }

    // Populate the user list in the UI
    function populateUserList(users) {
        const userList = document.getElementById('users');
        userList.innerHTML = ''; // Clear previous users
        users.forEach(user => {
            const li = document.createElement('li');
            li.textContent = user.username;
            li.addEventListener('click', () => {
                selectUser(user.id, user.username);
            });
            userList.appendChild(li);
        });
    }

    // Function to select a user and fetch previous messages
    async function selectUser(userId, username) {
        selectedUserId = userId;
        document.getElementById('chat-with').textContent = username;
        await fetchPreviousMessages(userId);
        openWebSocketConnection();
    }

    // Function to fetch previous messages with the selected user
    async function fetchPreviousMessages(userId) {
        const response = await fetch(`http://127.0.0.1:8000/messages/with/${userId}`, {
            headers: {
                'Authorization': getAuthToken()
            }
        });
        if (response.ok) {
            const messages = await response.json();
            displayMessages(messages);
        } else {
            console.error('Failed to fetch messages');
        }
    }

    // Display the previous messages in the chat window
    function displayMessages(messages) {
        const messageContainer = document.getElementById('messages');
        // Do not clear the message container here! We're appending messages.

        messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', message.sender_id === selectedUserId ? 'received' : 'sent');
            messageElement.textContent = `${message.content} (${new Date(message.created_at).toLocaleTimeString()})`;
            messageContainer.appendChild(messageElement); // Append new messages
        });

        messageContainer.scrollTop = messageContainer.scrollHeight; // Scroll to the bottom
    }


    // WebSocket connection setup
    function openWebSocketConnection() {
        if (websocket) {
            websocket.close(); // Close any previous connection
        }

        websocket = new WebSocket(`ws://127.0.0.1:8000/messages/ws?token=${localStorage.getItem('jwt_token')}`);

        websocket.onmessage = function(event) {
            const message = JSON.parse(event.data);
            if (message.sender_id === selectedUserId || message.receiver_id === selectedUserId) {
                displayMessages([message]);
            }
        };

        websocket.onclose = function(event) {
            console.log('WebSocket closed:', event);
        };
    }

    // Handle sending messages via WebSocket
    document.getElementById('message-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const input = document.getElementById('message-input');
        const messageContent = input.value;

        if (messageContent && websocket && selectedUserId) {
            const message = {
                content: messageContent,
                receiver_id: selectedUserId
            };
            websocket.send(JSON.stringify(message));
            input.value = ''; // Clear input after sending
        }
    });

    // Fetch users when the page loads
    fetchUsers();
</script>

</body>
</html>
"""
