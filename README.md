# PHP-Resume-Maker
This is a simple 2 part program that allows to to make and customize a PHP resume.
You can download the First Name Last Name - Resume.html and open it in any web browser to see how it looks 

Explination: The Resume template i used before was a pain in the but to edit, so i recreated the formating in PHP and use JSON to import data. Additionally i added a python GUI to write the json better. The provided CSS and PHP can be adjusted to your desire.

# How to use 

1. The Json editor
  The json editor is fairly simple to use it depends on PyQT and uses pulls the information from a the project main folder/html/json by default. To run install PyQT and run main.py
2. View the output
  For this you will need nginx or simmilar to compile the PHP and CSS into a usable format. by default the json folder containing all the json files needs to be in the same directory as your php and css file, this could be changed to your liking tho. 

# Issues
  This project is a little rough, i made it somewhat quickly and have not added as much polish as i would like to normally. example currently if your json is malformed such as a , after all the last dataset the python script will fail to open as i have not properly added error handleing yet. Apart from that if used correctly this makes a pretty nice looking resume and allows you to quickly edit it without having to worry about keeping formatting correct. Additionally i gave ChatGPT a look at the resume "flushed out" and it seems to like the formatting and thinks it should be ATS friendly.

  Additionally when making the php i was in between json formats and as such decieded to blow the project out of preportion by adding handling for both rather then just choosing one. The PHP can very much be simplified by removing this bsically useless code. If you plan on giving this a try i would **HIGHLY** reccomend redoing the PHP and CSS. When i get the time to come back to this in the future ill attmept to clean it up a little. But for now its functional 
