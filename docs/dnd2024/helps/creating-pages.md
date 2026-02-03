# Creating Pages

<!-- generated-by: scripts/txt_to_mkdocs.py v2026-02-03 -->


Creating new pages may be the single most performed action you will make on your site. This page will serve as a quick guide to creating pages, using a blog site as an example. Important topics include categories, the NewPage module, and autonumbering.
Fold
Unfold
Table of Contents
Categories
NewPage Module
Autonumbering
Categories
Every page on your site has a page
title
(even if that title is blank), but they also have page
names
, which can never be blank. The page name is what is used in the URL of the page. For example, the page name of this page is "help:creating-pages". The category of this page would be "help", since it precedes the colon.
Categories
are used in order to organize page types into meaningful groups. For example, let's say that we had the following pages:
Page Title
Purpose
My First Post
The first blog post on your site
Endless Quarrel
Another blog post on your site
Recent Changes
A system page showing what changes were made on your site recently
Home
The main page of the site where blog posts are listed
Already, we can see possible groupings. The first two pages are "blog" pages, the third is a "system" page, and the last is a "main" page. Therefore, we will put these pages into their respective categories:
Page Title
Page Name
My First Post
blog:my-first-page
Endless Quarrel
blog:endless-quarrel
Recent Changes
system:recent-changes
Home
main:home
Note
: If you have an uncategorized page and would like to add a category to it, simply rename the page (one of the page options at the bottom) and add the category to the beginning of the page name already there. Be sure that there is a colon (:) between the category name and the page name itself!
Categorizing pages like this allow you to do a variety of things. For example, you can now list
only
the "blog" pages using a
ListPages
module. In the
Site Manager
, you can set the edit/view permissions of specific categories. For example, in the Site Manager, you could set a "hidden" category to be private.
Perhaps most importantly, however, is the ability to
template
different categories.
Because of these advantages, we generally recommend that you put your pages into categories whenever possible. In the page creator form in the side bar, you can give a page a category by proceeding the page's title with the category name followed by a colon.
This is just a small overview of categories and their importance. For a more in-depth explanation, see the
Community How-Tos
.
NewPage Module
This site comes with a form on the sidebar that allows you to easily create new pages. These pages will be initially uncategorized unless you provide a category name in the text box (by typing the category name followed by a colon).
Let us say that you are working on a blog on which weekly posts will be made. If we use the scheme above, you may find it to be somewhat annoying to have to type out "blog:TITLE" every time you want to make a new post. Thankfully, Wikidot provides you with a tool that allows you to easily make pages: the
NewPage Module
.
In fact, the form used on the side bar is itself a generic NewPage Module!
The NewPage module allows you to select what category you want new pages to automatically belong in. For instance, we want new posts to be in the "blog" category, so we can make a NewPage module like so:
[[module NewPage category="blog"]]
Now, every time you use that form for creating a new page, it will automatically add your post into the "blog" category.
There are many more options native to the module for you to try out. For more info, read
Wikidot's Documentation
.
Autonumbering
Now, let's say that you are a very active blogger or are running a collaborative site on which multiple people may be posting at a time. You might find yourself running into a
page name collision
problem.
No two pages can have the exact same page name (category included). If a user attempts to create a page that already exists, a new page will
not
be created!
In order to avoid this problem, Wikidot offers the ability to
autonumber
page names. For a given category, Wikidot will automatically assign a page name for each newly created page, and since the process is automatic, running into a page name collision is effectively impossible.
Categories can only be set to autonumber from the
Site Manager
. The below represents a step-by-step process:
From the Dashboard, click on "Appearance & Behavior".
Look for one of the last options called "Autonumbering of pages".
Click on the "+ Add autonumbering" button.
Choose a category for which to add autonumbering.
Click "Save Changes".
After that, you're done! Be sure to explore the Options as well for more customization.
Autonumbering
This is how it appears in the Site Manager
Autonumbering
×
This is how it appears in the Site Manager
