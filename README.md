# PHP-Resume-Maker
This is a simple 2 part program that allows to to make and customize a PHP resume.

Explination: The Resume template i used before was a pain in the but to edit, so i recreated the formating in PHP and use JSON to import data. Additionally i added a python GUI to write the json better. The provided CSS and PHP can be adjusted to your desire.

# How to use 

1. The Json editor
  The json editor is fairly simple to use it depends on PyQT and uses pulls the information from a the project main folder/html/json by default. To run install PyQT and run main.py
2. View the output
  For this you will need nginx or simmilar to compile the PHP and CSS into a usable format. by default the json folder containing all the json files needs to be in the same directory as your php and css file, this could be changed to your liking tho. 

# Issues
  This project is a little rough, i made it somewhat quickly and have not added as much polish as i would like to normally. example currently if your json is malformed such as a , after all the last dataset the python script will fail to open as i have not properly added error handleing yet. Apart from that if used correctly this makes a pretty nice looking resume and allows you to quickly edit it without having to worry about keeping formatting correct. Additionally i gave ChatGPT a look at the resume "flushed out" and it seems to like the formatting and thinks it should be ATS friendly


<!DOCTYPE html>
<!-- saved from url=(0017)http://localhost/ -->
<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        
        <title>First Name Last Name - Resume</title>
        <link rel="stylesheet" href="./First Name Last Name - Resume_files/style.css">
    <link type="text/css" rel="stylesheet" id="dark-mode-custom-link"><link type="text/css" rel="stylesheet" id="dark-mode-general-link"><style lang="en" type="text/css" id="dark-mode-custom-style"></style><style lang="en" type="text/css" id="dark-mode-native-style"></style><style lang="en" type="text/css" id="dark-mode-native-sheet"></style></head>
<body>

<div class="page">

<header>
    <div class="header-left">
    <h1 class="colored">First Name Last Name</h1>
    <p class="noncolored">Professional Title</p>
    </div>

    <div class="header-right">
    <p>Example@domain.com</p>
    <p>(###) ###-####</p>
    </div>
</header>

<!-- Two-column layout for main content -->
<div class="two-col">

    <div class="col-left">

        <section class="skills">
        <h2>Skills</h2>

        
                                    <!-- New schema (skill blocks) -->
                <div class="skills-list">
                                                                    <div class="skill-item">
                            <div class="skill-title-row">
                                <span class="skill-title">Example Skill 1</span>
                                                                    <span class="skill-years">(20 yrs)</span>
                                                            </div>
                                                            <div class="skill-specifics">Specifics 1, Specifics 2</div>
                                                    </div>
                                                                    <div class="skill-item">
                            <div class="skill-title-row">
                                <span class="skill-title">Example Skill 2</span>
                                                                    <span class="skill-years">(1 yrs)</span>
                                                            </div>
                                                    </div>
                                                                    <div class="skill-item">
                            <div class="skill-title-row">
                                <span class="skill-title">Example Skill 3</span>
                                                                    <span class="skill-years">(4 yrs)</span>
                                                            </div>
                                                            <div class="skill-specifics">Specifics</div>
                                                    </div>
                                    </div>
                    </section>

        <section class="skills">
        <h2>Experience</h2>

        
                    <ul>
                                    <!-- New schema -->
                                                                    <li>Example Experience: 6 years</li>
                                                                    <li>Example 2: 5 years</li>
                                                                    <li>Example 3: 3 years</li>
                                                                    <li>Example 4: 3 years</li>
                                                </ul>
        </section>
    
                    <section class="links">
                <h2>Links</h2>
                <div class="skills-list">
                    <ul class="skills-list">
                                                                                                                <li style="margin: 6px 0;">
                                    GitHub :  <br>
                                    <a href="https://github.com/EvenNine" target="_blank" rel="noopener noreferrer">
                                        https://github.com/EvenNine                                    </a>
                                </li>
                                                                        </ul>
                </div>
            </section>
        


    </div>

<div class="col-right">

<section class="about-me">
    <h2>About Me</h2>
            <p>Example About me :D</p>
    </section>

<section class="about-me">
    <h2>Work History</h2>

    
    
                                                    <div class="job">
                    <h3>
                        Example Job 1 |
                        Example Title 1                    </h3>

                    <p class="small-indented">
                        2024-05                         - 2025-10                    </p>

                    <p class="paragraph-text">
                        Example Description                    </p>

                                            <ul>
                                                                                            <li>Highlighted bulletpoint 1</li>
                                                                                            <li>Highlighted bulletpoint 2</li>
                                                                                            <li>Highlighted bulletpoint 3</li>
                                                    </ul>
                    
                                            <div class="job-skill-tags" aria-label="Skills used">
                                                            <span class="job-skill-tag">Skill 1</span>
                                                            <span class="job-skill-tag">Skill 2</span>
                                                            <span class="job-skill-tag">Skill 3</span>
                                                    </div>
                                    </div>
                                            <div class="job">
                    <h3>
                        Example Job 2 |
                        Example Title 2                    </h3>

                    <p class="small-indented">
                        2024-05                         - 2025-10                    </p>

                    <p class="paragraph-text">
                        Example Description                    </p>

                                            <ul>
                                                                                            <li>Highlighted bulletpoint 1</li>
                                                                                            <li>Highlighted bulletpoint 2</li>
                                                                                            <li>Highlighted bulletpoint 3</li>
                                                    </ul>
                    
                                            <div class="job-skill-tags" aria-label="Skills used">
                                                            <span class="job-skill-tag">Skill 1</span>
                                                            <span class="job-skill-tag">Skill 2</span>
                                                            <span class="job-skill-tag">Skill 3</span>
                                                    </div>
                                    </div>
                                            <div class="job">
                    <h3>
                        Example Job 3 |
                        Example Title 3                    </h3>

                    <p class="small-indented">
                        2024-05                         - 2025-10                    </p>

                    <p class="paragraph-text">
                        Example Description                    </p>

                                            <ul>
                                                                                            <li>Highlighted bulletpoint 1</li>
                                                                                            <li>Highlighted bulletpoint 2</li>
                                                                                            <li>Highlighted bulletpoint 3</li>
                                                    </ul>
                    
                                            <div class="job-skill-tags" aria-label="Skills used">
                                                            <span class="job-skill-tag">Skill 1</span>
                                                            <span class="job-skill-tag">Skill 2</span>
                                                            <span class="job-skill-tag">Skill 3</span>
                                                    </div>
                                    </div>
            
        
    </section>

</div>

</div>

<!-- Full-width section for projects -->
<section class="central-box">
    <h2>Projects</h2>

    
    
                                                    <div class="job">
                    <h3>This Resume</h3>
                    <p class="small-indented">
                        2026-03                                            </p>
                    <p class="paragraph-text">
                        This resume was designed with a custom data-driven resume generation system using PHP and structured JSON data sources. To assist with this process I built a Python (PyQt) management tool to edit and validate JSON schema across platforms.                    </p>

                                            <ul>
                                                                                            <li>This is a place to highligh specifics about your resume</li>
                                                    </ul>
                    
                                            <div class="job-skill-tags" aria-label="Project stack">
                                                            <span class="job-skill-tag">Python</span>
                                                            <span class="job-skill-tag">PHP</span>
                                                            <span class="job-skill-tag">CSS</span>
                                                    </div>
                                    </div>
            
        
    </section>

<footer>
<p>© 2026 First Name Last Name</p>
</footer>

</div>



</body></html>
