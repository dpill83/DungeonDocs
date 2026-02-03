# Using Modules

<!-- generated-by: scripts/txt_to_mkdocs.py v2026-02-03 -->


Wikidot offers a variety of Modules that help make certain tasks much easier and more convenient. Using these modules in the right ways can help make your site dynamic and much easier to maintain. Below, we want to introduce you to some of the most widely used modules and demonstrate how you can use them on your site.
For detailed information over all the modules, see
Wikidot's Documentation
.
Fold
Unfold
Table of Contents
Quick Reference
ListPages
Criteria
Ordering
Format
Live Example
NewPage
NewPage Alternative
Quick Reference
Here is a quick reference to some of these modules. Certain ones are explained in greater depth later.
Module
Description
ListPages
Lists all the pages on the site meeting given criteria.
TagCloud
Generates a cloud of tags used on your site for a given category.
PageCalendar
Lists the number of pages per year and month matching given criteria.
PageTree
Lists all descendent pages of a root page.
Join
Generates a button that allows users to apply or join your site.
CSS
Creates on-the-fly CSS rules and definitions for a single page.
NewPage
Generates a form that allows you to easily create new pages with a given title.
Redirect
Redirects the user to a different page or website.
Comments
Inserts page comments onto a page.
Rate
Creates a little rate page widget that allows users to vote or rate page content.
Files
Lists all the files on a given page.
ListPages
The ListPages module is perhaps the single most useful module Wikidot offers. All it does is list pages that fit a certain list of criteria. What makes it so powerful is the vast range of criteria you can specify and the ability to format each entry in any way you need.
The module follows the basic format below:
[[module ListPages CRITERIA...]]
FORMAT
[[/module]]
Criteria
ListPages allows you to select pages given a wide range of specifiers. You can list pages given…
Specific categories
Specific tags
Specific date created
Specific parent page
Specific rating
Specific page author
Specific data form values
As an example, let's say that you are running a blog, and you want to list all of your blog entries. All of your posts are located in the "blog" category, but you do not want to list pages tagged with "_incomplete" or "_deleted". You can use the following ListPages criteria to do this easily:
[[module ListPages category="blog" tags="-_incomplete -_deleted"]]
FORMAT
[[/module]]
For more information about each of the criteria, see
Wikidot's Documentation
.
Ordering
You are also able to specify the order in which pages are listed. By default, pages will be listed according to which was updated first, but you may want to list pages alphabetically or by creation date. By using the
order=
criterion, you can choose exactly how you want your pages ordered.
Among the options are:
Title
Creation date
Update date
Author
Page size
Page rating
Number of comments
Page name
Random
Data Form values
For more information about each of the ordering options, see
Wikidot's Documentation
.
Format
ListPages allows you to format your entries however you like. To do this effectively, though, requires some knowledge about page variables. For instance, let us say that you are making a blog site, and you want to use the following format for your post listing on the front page:
+ Page Title

Preview of the Content

[[[link to page | Read More]]]
How can you replace the "Page Title" with the actual page's title? Wikidot allows you to use a very large number of variables that change on a per-page basis. For example, the
%%title%%
variable, when seen in the code, will be replaced by the page's title.
For our blog, we would use the following code:
[[module ListPages category="blog" tags="-_incomplete -_deleted"]]
+ %%title%%

%%preview(400)%%

[[[%%fullname%% | Read More]]]
[[/module]]
The list of variables is too vast to cover here, but you can see
Wikidot's Documentation
for a comprehensive list.
Live Example
Here is an example of ListPages in action. Our goal is to list all of the help pages on this site in alphabetical order alongside the page's size.
Title
Size
Creating Pages
40
CSS Themes
36
Editing Pages
39
First Time User
7467
Navigation Bars
41
Quick Reference
41
Templates
35
Using Modules
39
[[module ListPages category="help" order="title" prependLine="||~ Title||~ Size||" separate="false"]]
||%%title_linked%%||%%size%%||
[[/module]]
Note that some of these page sizes are small since the help pages actually import code from another site.
NewPage
The NewPage module stands right beside the ListPages module in terms of usefulness; this is especially true for collaboration sites and wikis.
The NewPage module will generate form that allows users to easily create pages. The form looks like the below:
The text field allows you to type in the title of the page you want to create, and pressing "Example" will actually create the page and take you to an editing window.
The NewPage module is important since it allows you as the administrator to control how pages are created. Because of the criteria options the module comes with, you can essentially organize your site as pages are created. For example, lets say you are building a wiki, and you expect users to be creating and editing articles. You want all of your article pages to be in the "article" category so that you can easily list them (using ListPages) elsewhere.
The NewPage module allows you to create a field that members can use to create pages that are automatically stored into the "article" category. This can be done with the following code:
[[module NewPage category="article" button="Add Article"]]
The NewPage module also allows you to add initial tags or automatically set the pages' parents. For a comprehensive description of the module, see
Wikidot's Documentation
.
NewPage Alternative
As powerful as the NewPage module is, it still has a few limitations. Fortunately, a brilliant person named
James Kanjo
developed a code snippet that
extends the NewPage module
and eliminates the limitations. His NewPage Extension serves as a more powerful version of Wikidot's native module and provides you, the administrator, with many more options. If you are not afraid of a little exploration, Jame's snippet is worth investigating!
