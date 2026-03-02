<?php
declare(strict_types=1);

/*
 | ----*--*--------------------------------------------------------------------
 | Helper Function
 |--------------------------------------------------------------------------
 */
function loadJson(string $path): array
{
    if (!file_exists($path)) {
        return [];
    }

    $content = file_get_contents($path);
    $data = json_decode($content, true);

    return json_last_error() === JSON_ERROR_NONE ? $data : [];
}

/*
 | ----*--*--------------------------------------------------------------------
 | Load Json files
 |--------------------------------------------------------------------------
 */
$baseDir      = __DIR__;
$contact      = loadJson($baseDir . '/json/contact.json');
$skillsData   = loadJson($baseDir . '/json/skills.json');
$jobsData     = loadJson($baseDir . '/json/jobs.json');
$ProjectsData = loadJson($baseDir . '/json/projects.json');

/*
 | ----*--*--------------------------------------------------------------------
 | Basic Variables (with fallbacks)
 |--------------------------------------------------------------------------
 */
// Old and updated json schema supported. 
$first = '';
$last  = '';

if (isset($contact['name']) && is_array($contact['name'])) {
    $first = is_string($contact['name']['first'] ?? null) ? $contact['name']['first'] : '';
    $last  = is_string($contact['name']['last'] ?? null)  ? $contact['name']['last']  : '';
} else {
    $first = is_string($contact['first_name'] ?? null) ? $contact['first_name'] : '';
    $last  = is_string($contact['last_name'] ?? null)  ? $contact['last_name']  : '';
}

$rawName = trim(trim($first) . ' ' . trim($last));
$name = htmlspecialchars($rawName);

// Title / headline
$rawTitle = '';
if (is_string($contact['headline'] ?? null)) {
    $rawTitle = $contact['headline'];
} elseif (is_string($contact['description'] ?? null)) {
    $rawTitle = $contact['description'];
} elseif (is_string($contact['title'] ?? null)) {
    $rawTitle = $contact['title'];
}
$title = htmlspecialchars($rawTitle);

// Email / phone
$rawEmail = '';
$rawPhone = '';
$rawLinks = '';

if (isset($contact['contact']) && is_array($contact['contact'])) {
    $rawEmail = is_string($contact['contact']['email'] ?? null) ? $contact['contact']['email'] : '';
    $rawPhone = is_string($contact['contact']['phone'] ?? null) ? $contact['contact']['phone'] : '';
} elseif (isset($contact['Contact']) && is_array($contact['Contact'])) { // older capitalized key
    $rawEmail = is_string($contact['Contact']['email'] ?? null) ? $contact['Contact']['email'] : '';
    $rawPhone = is_string($contact['Contact']['phone'] ?? null) ? $contact['Contact']['phone'] : '';
}

$email = htmlspecialchars($rawEmail);
$phone = htmlspecialchars($rawPhone);


// Links
$linksRaw = [];
if (!empty($contact['links']) && is_array($contact['links'])) {
    $linksRaw = $contact['links'];
} elseif (!empty($contact['Links']) && is_array($contact['Links'])) {
    $linksRaw = $contact['Links'];
} elseif (!empty($contact['contact']['links']) && is_array($contact['contact']['links'])) {
    $linksRaw = $contact['contact']['links'];
}


// About Me
$aboutMeRaw = '';
if (is_string($contact['aboutme'] ?? null)) {
    $aboutMeRaw = $contact['aboutme'];
} elseif (is_string($contact['about_me'] ?? null)) {
    $aboutMeRaw = $contact['about_me'];
} elseif (is_string($contact['about'] ?? null)) {
    $aboutMeRaw = $contact['about'];
} elseif (is_string($contact['summary'] ?? null)) {
    $aboutMeRaw = $contact['summary'];
}

$aboutMeRaw = trim($aboutMeRaw);
$aboutMe = $aboutMeRaw !== '' ? nl2br(htmlspecialchars($aboutMeRaw)) : '';

$currentYear = date("Y");
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title><?= $name ?> - Resume</title>
        <link rel="stylesheet" href="style.css">
    </head>
<body>

<div class="page">

<header>
    <div class="header-left">
    <h1 class="colored"><?= $name ?></h1>
    <p class="noncolored"><?= $title ?></p>
    </div>

    <div class="header-right">
    <p><?= $email ?></p>
    <p><?= $phone ?></p>
    </div>
</header>

<!-- Two-column layout for main content -->
<div class="two-col">

    <div class="col-left">

        <section class="skills">
        <h2>Skills</h2>

        <?php
            // Support new skills.json schemas:
            // 1) Old: { "skills": [ "Networking", "Linux: ..." ], ... }
            // 2) New: { "skills": [ { "name": "...", "years": 5, "focused": true, "specifics": ["..."] }, ... ], ... }
            $skillsList = [];
            if (!empty($skillsData['skills']) && is_array($skillsData['skills'])) {
                $skillsList = $skillsData['skills'];
            }
        ?>

        <?php if (!empty($skillsList)): ?>
            <?php if (isset($skillsList[0]) && is_string($skillsList[0])): ?>
                <!-- Old schema (simple bullet list) -->
                <ul>
                    <?php foreach ($skillsList as $skill): ?>
                        <li><?= htmlspecialchars((string)$skill) ?></li>
                    <?php endforeach; ?>
                </ul>
            <?php else: ?>
                <!-- New schema (skill blocks) -->
                <div class="skills-list">
                    <?php foreach ($skillsList as $skill): ?>
                        <?php
                            if (!is_array($skill)) continue;
                            $skillName = trim((string)($skill['name'] ?? ''));
                            if ($skillName === '') continue;

                            $years = $skill['years'] ?? null;
                            $yearsText = '';
                            if (is_int($years) || is_float($years) || (is_string($years) && trim($years) !== '')) {
                                $yearsText = trim((string)$years);
                            }

                            $specifics = $skill['specifics'] ?? null;
                            $specText = '';
                            if (is_array($specifics)) {
                                $parts = array_values(array_filter(array_map('trim', array_map('strval', $specifics))));
                                $specText = implode(', ', $parts);
                            } elseif (is_string($specifics)) {
                                $specText = trim($specifics);
                            }
                        ?>
                        <div class="skill-item">
                            <div class="skill-title-row">
                                <span class="skill-title"><?= htmlspecialchars($skillName) ?></span>
                                <?php if ($yearsText !== ''): ?>
                                    <span class="skill-years">(<?= htmlspecialchars($yearsText) ?> yrs)</span>
                                <?php endif; ?>
                            </div>
                            <?php if ($specText !== ''): ?>
                                <div class="skill-specifics"><?= htmlspecialchars($specText) ?></div>
                            <?php endif; ?>
                        </div>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>
        <?php else: ?>
            <p>No skills found.</p>
        <?php endif; ?>
</section>

        <section class="skills">
        <h2>Experience</h2>

        <?php
            // Support new experience schemas:
            // 1) Old: { "experience": [ { "Tech Support": {"years":"5"}, ... } ] }
            // 2) New: { "experience": [ { "title": "Tech Support", "years": 5 }, ... ] }
            $expList = [];
            if (!empty($skillsData['experience']) && is_array($skillsData['experience'])) {
                $expList = $skillsData['experience'];
            }
        ?>

        <?php if (!empty($expList)): ?>
            <ul>
                <?php if (isset($expList[0]) && is_array($expList[0]) && isset($expList[0]['title'])): ?>
                    <!-- New schema -->
                    <?php foreach ($expList as $exp): ?>
                        <?php
                            if (!is_array($exp)) continue;
                            $t = trim((string)($exp['title'] ?? ''));
                            if ($t === '') continue;
                            $y = $exp['years'] ?? '';
                            $yText = trim((string)$y);
                        ?>
                        <li><?= htmlspecialchars($t) ?><?php if ($yText !== ''): ?>: <?= htmlspecialchars($yText) ?> years<?php endif; ?></li>
                    <?php endforeach; ?>
                <?php else: ?>
                    <!-- Old schema -->
                    <?php foreach ($expList as $expObject): ?>
                        <?php if (!is_array($expObject)) continue; ?>
                        <?php foreach ($expObject as $expName => $details): ?>
                            <?php
                                $y = is_array($details) ? ($details['years'] ?? '') : '';
                                $yText = trim((string)$y);
                            ?>
                            <li><?= htmlspecialchars((string)$expName) ?><?php if ($yText !== ''): ?>: <?= htmlspecialchars($yText) ?> years<?php endif; ?></li>
                        <?php endforeach; ?>
                    <?php endforeach; ?>
                <?php endif; ?>
            </ul>
        <?php else: ?>
            <p>No experience data found.</p>
        <?php endif; ?>
</section>
    
        <?php if (!empty($linksRaw) && is_array($linksRaw)): ?>
            <section class="links">
                <h2>Links</h2>
                <div class="skills-list">
                    <ul class="skills-list">
                        <?php foreach ($linksRaw as $link): ?>
                            <?php
                                $labelRaw = is_string($link['label'] ?? null) ? $link['label'] : '';
                                $urlRaw   = is_string($link['url'] ?? null) ? $link['url'] : '';
                                $label    = htmlspecialchars($labelRaw);
                                $url      = htmlspecialchars($urlRaw);
                            ?>
                            <?php if ($url !== ''): ?>
                                <li style="margin: 6px 0;">
                                    <?= $label . " : " ?> <br>
                                    <a href="<?= $url ?>" target="_blank" rel="noopener noreferrer">
                                        <?= $url!== '' ? $url : $url ?>
                                    </a>
                                </li>
                            <?php endif; ?>
                        <?php endforeach; ?>
                    </ul>
                </div>
            </section>
        <?php endif; ?>



    </div>

<div class="col-right">

<section class="about-me">
    <h2>About Me</h2>
    <?php if ($aboutMe !== ''): ?>
        <p><?= $aboutMe ?></p>
    <?php else: ?>
        <p>About me not provided.</p>
    <?php endif; ?>
</section>

<section class="about-me">
    <h2>Work History</h2>

    <?php
        // Support both jobs.json schemas:
        // 1) Old: { "Company": [ {title,start,end,description,skills...}, ... ], ... }
        // 2) New: { "jobs": [ {company,title,start,end,description,skills...}, ... ] }
        $jobList = [];
        $jobsIsNew = false;

        if (!empty($jobsData['jobs']) && is_array($jobsData['jobs'])) {
            $jobList = $jobsData['jobs'];
            $jobsIsNew = true;
        } elseif (!empty($jobsData) && is_array($jobsData)) {
            $jobList = $jobsData;
        }
    ?>

    <?php if (!empty($jobList)): ?>

        <?php if ($jobsIsNew): ?>
            <?php foreach ($jobList as $job): ?>
                <?php if (!is_array($job)) continue; ?>
                <div class="job">
                    <h3>
                        <?= htmlspecialchars((string)($job['company'] ?? '')) ?> |
                        <?= htmlspecialchars((string)($job['title'] ?? '')) ?>
                    </h3>

                    <p class="small-indented">
                        <?= htmlspecialchars((string)($job['start'] ?? '')) ?>
                        <?php if (!empty($job['end'])): ?> - <?= htmlspecialchars((string)$job['end']) ?><?php endif; ?>
                    </p>

                    <p class="paragraph-text">
                        <?= htmlspecialchars((string)($job['description'] ?? '')) ?>
                    </p>

                    <?php if (!empty($job['highlights']) && is_array($job['highlights'])): ?>
                        <ul>
                            <?php foreach ($job['highlights'] as $b): ?>
                                <?php if (!is_string($b) || trim($b)==='') continue; ?>
                                <li><?= htmlspecialchars($b) ?></li>
                            <?php endforeach; ?>
                        </ul>
                    <?php endif; ?>

                    <?php if (!empty($job['skills']) && is_array($job['skills'])): ?>
                        <div class="job-skill-tags" aria-label="Skills used">
                            <?php foreach ($job['skills'] as $tag): ?>
                                <span class="job-skill-tag"><?= htmlspecialchars((string)$tag) ?></span>
                            <?php endforeach; ?>
                        </div>
                    <?php endif; ?>
                </div>
            <?php endforeach; ?>

        <?php else: ?>
            <?php foreach ($jobList as $company => $entries): ?>
                <?php if (!is_array($entries)) continue; ?>
                <?php foreach ($entries as $job): ?>
                    <?php if (!is_array($job)) continue; ?>
                    <div class="job">
                        <h3>
                            <?= htmlspecialchars((string)$company) ?> |
                            <?= htmlspecialchars((string)($job['title'] ?? '')) ?>
                        </h3>
                        <p class="small-indented">
                            <?= htmlspecialchars((string)($job['start'] ?? '')) ?> -
                            <?= htmlspecialchars((string)($job['end'] ?? '')) ?>
                        </p>
                        <p class="paragraph-text">
                            <?= htmlspecialchars((string)($job['description'] ?? '')) ?>
                        </p>

                        <?php if (!empty($job['skills']) && is_array($job['skills'])): ?>
                            <div class="job-skill-tags" aria-label="Skills used">
                                <?php foreach ($job['skills'] as $tag): ?>
                                    <span class="job-skill-tag"><?= htmlspecialchars((string)$tag) ?></span>
                                <?php endforeach; ?>
                            </div>
                        <?php endif; ?>
                    </div>
                <?php endforeach; ?>
            <?php endforeach; ?>
        <?php endif; ?>

    <?php else: ?>
        <p>No job history found.</p>
    <?php endif; ?>
</section>

</div>

</div>

<!-- Full-width section for projects -->
<section class="central-box">
    <h2>Projects</h2>

    <?php
        // Support new projects.json schemas:
        // 1) Old: { "Project Name": [ {start,end,description,...}, ... ], ... }
        // 2) New: { "projects": [ {name,start,end,summary,highlights,stack,...}, ... ] }
        $projList = [];
        $projectsIsNew = false;

        if (!empty($ProjectsData['projects']) && is_array($ProjectsData['projects'])) {
            $projList = $ProjectsData['projects'];
            $projectsIsNew = true;
        } elseif (!empty($ProjectsData) && is_array($ProjectsData)) {
            $projList = $ProjectsData;
        }
    ?>

    <?php if (!empty($projList)): ?>

        <?php if ($projectsIsNew): ?>
            <?php foreach ($projList as $p): ?>
                <?php if (!is_array($p)) continue; ?>
                <div class="job">
                    <h3><?= htmlspecialchars((string)($p['name'] ?? '')) ?></h3>
                    <p class="small-indented">
                        <?= htmlspecialchars((string)($p['start'] ?? '')) ?>
                        <?php if (!empty($p['end'])): ?> - <?= htmlspecialchars((string)$p['end']) ?><?php endif; ?>
                    </p>
                    <p class="paragraph-text">
                        <?= htmlspecialchars((string)($p['summary'] ?? '')) ?>
                    </p>

                    <?php if (!empty($p['highlights']) && is_array($p['highlights'])): ?>
                        <ul>
                            <?php foreach ($p['highlights'] as $b): ?>
                                <?php if (!is_string($b) || trim($b)==='') continue; ?>
                                <li><?= htmlspecialchars($b) ?></li>
                            <?php endforeach; ?>
                        </ul>
                    <?php endif; ?>

                    <?php if (!empty($p['stack']) && is_array($p['stack'])): ?>
                        <div class="job-skill-tags" aria-label="Project stack">
                            <?php foreach ($p['stack'] as $tag): ?>
                                <span class="job-skill-tag"><?= htmlspecialchars((string)$tag) ?></span>
                            <?php endforeach; ?>
                        </div>
                    <?php endif; ?>
                </div>
            <?php endforeach; ?>

        <?php else: ?>
            <?php foreach ($projList as $projectName => $entries): ?>
                <?php if (!is_array($entries)) continue; ?>
                <?php foreach ($entries as $projectinfo): ?>
                    <?php if (!is_array($projectinfo)) continue; ?>
                    <div class="job">
                        <h3><?= htmlspecialchars((string)$projectName) ?></h3>
                        <p class="small-indented">
                            <?= htmlspecialchars((string)($projectinfo['start'] ?? '')) ?> -
                            <?= htmlspecialchars((string)($projectinfo['end'] ?? '')) ?>
                        </p>
                        <p class="paragraph-text">
                            <?= htmlspecialchars((string)($projectinfo['description'] ?? '')) ?>
                        </p>
                    </div>
                <?php endforeach; ?>
            <?php endforeach; ?>
        <?php endif; ?>

    <?php else: ?>
        <p>No projects found.</p>
    <?php endif; ?>
</section>

<footer>
<p>&copy; <?= $currentYear ?> <?= $name ?></p>
</footer>

</div>

</body>
</html>
