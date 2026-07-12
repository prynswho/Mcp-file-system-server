this is not a very pretty code , as im new to python so i know the file structure is a mess right now

BUT IT WORKS (I will change it in a few days)

to use this code , you will need to 
1.create a venv first
2.configure you workspace directory , DO NOT GIVE LLMS ACCESS TO THE WHOLE PC :)
3.USE PYTHON 3.12=> , as libraries like mcp , uvicorn are not working with 3.14 ( maybe cause its new)

to run the server -> python -m src.filesystem_mcp.server
and to run docker -> docker compose up

