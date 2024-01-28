# Determinator
 ### An undertale-styled inspiring quote generator website that uses LLM.
 ![image](https://github.com/pixol20/Determinator/assets/115364463/b390fe6a-f2d6-4b63-bc68-f0206f5c5fde)
## How to install
**Currently tested only on windows with Nvidia GPU**

You'll need python for this. My version is 3.10.6
1) Download release or run `git clone https://github.com/pixol20/Determinator.git`
2) `cd Determinator`
3) `python -m venv ./venv`
4) `.\venv\Scripts\activate.bat`
5) `pip install -r requirements.txt`
6) `cd src`
7) Then you'll need to download a model for example from [hugging face](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending) and place it in models folder.
8) In model.py file(it's located in Determinator/src) set value of ModelLocation to '../models/"your model folder"'
9) `flask run`

 Your app is ready, but remember. flask run creates a development server. And **you should not use it in deployment**. Also **you must change app.secret_key value**
## Features
 <ul>
  <li>different models support</li>
  <li>sounds from undertale</li>
  <li>flexible templates</li>
  <li>optional logging</li>
 </ul>
 
 ## Showcase
 ![showcase](https://github.com/pixol20/Determinator/assets/115364463/0c52a5ca-c55e-4c3a-b550-4f0fa96789e8)
## Other info
Undertale is a game created by Toby Fox

I used [this font](https://fontstruct.com/fontstructions/show/2368299/determination-40)


This is cs50 final project
