import os


def inject_websocket_client(port):
    """
    Injects a Vanilla JS WebSocket client into an HTML file before the </body> tag.
    """

    # The JavaScript to inject (formatted to accept any port number)
    javascript_to_inject = f"""
    <script>
        // 1. Connect to Python
        const websocket = new WebSocket("ws://localhost:{port}");

        // 2. What to do when Python sends a message
        websocket.onmessage = function(event) {{
            console.log("Receieved message from SERVER");
             location.reload();
        }};

        websocket.onopen = function() {{
            console.log("Successfully connected to WEBSOCKET!");
        }};

        websocket.error = function(error) {{
            console.error("WebSocket error:", error);
        }};

        websocket.onclose = function() {{
            console.log("WebSocket connection closed.");
        }};

    </script>
    """

    file_path = os.path.abspath(os.path.join(
        __file__, "../../../", "requirements.html"))
  
    if not os.path.exists(file_path):
        print(f"Error: Could not find {file_path}")
        return False
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

            updated_html = html_content.replace(
                "</body>", f"{javascript_to_inject}\n</body>")

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(updated_html)

            print(f"Success: JavaScript was injected into {file_path}!")
            return True
    except Exception as e:
        print(f"Error while injecting JavaScript: {e}")
        return False
