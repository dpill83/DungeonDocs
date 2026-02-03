# Navigation Bars

<!-- generated-by: scripts/txt_to_mkdocs.py v2026-02-03 -->


Wikidot allows you to have two navigation bars that can appear on every page. These bars are located on the top of the page and to the side, known as the Top Bar and Side Bar respectively. These are commonly used as navigational tools for users so that they may access various portions of your site with ease.
You may, of course, edit these to fit the purposes of your site. This page will give you a few tips and instructions when editing these bars.
Fold
Unfold
Table of Contents
The Top Bar
Dropdown Menues
The Side Bar
Hiding the Side Bar
Specialized Navigation Bars
The Top Bar
The Top Bar is likely the more important of the two navigational bars, as it is the one that will appear most obvious and intuitive for tablet and phone users. In order to access and alter this bar, you need to go to the
nav:top
page, linked to
here
and in the default top bar that comes with this template. Then, you may edit it like any normal wiki page.
When you edit it, you may see what appears to be a bunch of jumbled code. Do not become intimidated, though! We will walk you through how to interpret it.
The top bar is organized like a bulleted list, though to be compatible with Bootstrap, it uses a special syntax. The following would be a very simple top bar with just two links:
[[ul class="nav navbar-nav"]]
  [[li]][/ Home][[/li]]
  [[li]][[[help:navigation-bars|Navigation Bars]]][[/li]]
[[/ul]]
If you want to add another link, simply add the
[[li]] [[/li]]
code in and insert your link in the middle. See, that's not too bad, right?
Dropdown Menues
The primary reason the code on the default top bar looks so convoluted has to do with dropdown menues. As you may notice, whenever you click on "Help Docs", a list of the various help pages appears. You may find this necessary for your purposes as well, so we'll touch on how to format a dropdown menu.
Dropdown menues consist of two parts:
The Activation Link
The List of actual links
Therefore, the code accounts for both of these parts.
The Activation Link is what is seen at the top bar itself. To place this, use the following template code:
[[li class="dropdown"]]
[[a href="#" class="dropdown-toggle" data-toggle="dropdown"]]TEXT[[/a]][[ul class="dropdown-menu"]]
Simply replace
TEXT
with whatever you want the link to state.
As you may begin to notice, by declaring a separate
[[ul]]
element at the end, the List of links is simply another specially formatted list of links like before. You can now add your links in like normal, being sure to encase each within
[[li]]
tags.
Finally, end the list with the following code:
[[/ul]][[/li]]
The Side Bar
The Side Bar is the navigation bar that appears on the side of the site. On tablets and phones, however, there generally is not enough room on the screen to fit an entire side bar; therefore, the Standard Template moves the side bar to be directly over the content when viewed on mobile devices.
In order to edit the side bar, you need to access the
nav:side
page, linked to
here
and in the default top bar that comes with this template. Then, you may edit it like any normal wiki page.
Unlike the top bar, the side bar need not follow any particular format. In general, though, it is best if you use a simple bulleted list like the one below:
* [[[link | Item 1]]]
* [[[link | Item 2]]]
* [[[link | Item 3]]]
Many themes naturally account for a bulleted list in the side bar and have special code to handle it.
Hiding the Side Bar
You may find that the Top Bar is entirely sufficient for your needs. In this case, you may not even desire having a side bar, and therefore you can have more room for your content. Thankfully, the Standard Template offers a very simple way to remove the side bar on a per-category basis.
The below represents a step-by-step process:
Go to the
Site Manager
.
From the Dashboard, click on "Appearance & Behavior".
Look for the first option, called "Themes".
After it completely loads, click on the tab called "Custom".
Find the name of the theme you are using and click "Edit"
Uncheck the box that says "Use side menu bar"
Click the "Save Theme" button
After that, you're done!
No Side Bar
This is how it appears in the Site Manager
No Side Bar
×
This is how it appears in the Site Manager
Specialized Navigation Bars
In reality, you can actually have many different navigation bars, though only two may be used at a time per category. Wikidot allows you to specify different navigation bars for each category if you desire it. For example, if you want to have a different side bar for the "blog" category, you can create a new page called
nav:side-blog
and put the code for the customized side bar. Then, in the
Site Manager
under "Appearance & Behavior" and "Navigation elements", you can set the "blog" category to use
nav:side-blog
as its side bar.
