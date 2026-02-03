# Editing Pages

<!-- generated-by: scripts/txt_to_mkdocs.py v2026-02-03 -->


Editing a page seems like a relatively straightforward process, and indeed it is. If all you want to do is edit the page's contents, then simply click the Edit button at the bottom of the page and type away. However, there are many more ways in which you can change a page's information. For instance, you can tag a page with special keywords, attach files, and so on. This page will introduce you to these topics.
Fold
Unfold
Table of Contents
Tagging
Files
Linking to Attachments
Using Images
File Management
Parent Pages
Tagging
Next to the Edit button on the page options is a button that says Tags. If you click on that button, a form will appear that will let you edit the tags on that page. When finished, you can see the list of tags sitting below the content on the lefthand side; you should see that this particular page has a single tag, called "tagged". But, what exactly are tags, and what are they useful for?
Quite simply, a
tag
is simply a keyword used to describe the content on that page. These are keywords that you might type into a search engine. For example, if you have a blog post about how to make boiled eggs, you might tag the page with "cooking", "eggs", "boiling", and "food". All of these words describe the page's contents.
If you precede a tag name with an underscore (_), it is considered a
hidden tag
. Hidden tags are useful for website maintenance (like tagging a page with "_incomplete").
Tagging pages is useful for a variety of reasons. Firstly, these tags can be captured by Wikidot's search engine so that better results may come up. Secondly, tags can serve as an additional parameter for the
ListPages
module. Therefore, you can choose to list pages that have a specific tag.
For example, if you wanted to hide all of your incomplete blog posts that are tagged with "_incomplete", you could use the following ListPages code:
[[module ListPages category="blog" tags="-_incomplete" separate="false"]]
* %%title_linked%%
[[/module]]
The
tags="-_incomplete"
part tells the module to ignore all blog posts tagged with "_incomplete".
You can read more about how the ListPages module works with tags on
Wikidot's Documentation
.
Files
Wikidot allows you to add and remove files from individual pages. If you click the Files button located at the bottom, a button appears asking you to select the files you want to upload along with a list of files already on the page. When you click on the button, a window will appear showing your computer's files so that you can select what to upload.
Multiple files can be uploaded at a time, but you can only delete one file at a time.
Linking to Attachments
When files are uploaded to a page, you can access them by using the following syntax:
[[file
filename
|
custom text
]]
You can read more on this on
Wikidot's Documentation
.
Using Images
If the file you uploaded is an image and you want the page to display it, you can use Wikidot's standard image syntax, all documented on
their Documentation
. In addition,
Timothy Foster
's
Image Box
snippet is integrated into the Standard Template's theme. The snippet can be used to easily add a title and caption to images.
The following image is produced with the below code:
[[inclu
de :snippets:modal-image
|image=:first
|heading=Sulphur
|caption=Sulphur is one of the 118 elements of the Periodic Table of Elements
|max-width=375px
|kind=primary
]]
Sulphur
Sulphur is one of the 118 elements of the Periodic Table of Elements
Sulphur
×
Sulphur is one of the 118 elements of the Periodic Table of Elements
File Management
Since files may end up scattered across pages, it can be difficult to manage files if a few need to be deleted. Unfortunately, Wikidot itself does not offer native file management in the Site Manager. Thankfully, a brilliant person,
tsangk
, developed a tool called the
Wikidot Extension
which comes with a centralized file manager. If you go to his site, you can see how to install this extension if you find yourself needing to move or delete large quantities of files.
Parent Pages
Sometimes, pages come in a rather clear hierarchy. For example, this page is among the many help pages on this site, and the
User Guide
page is the central help page. Therefore, we can consider the User Guide page to be the
parent
of this page and all the other help pages. If we had more pages related to editing, they might all be children of this page, and hence you begin to form a tree structure, with User Guide at the root.
When you set a page's parent, you can begin to see a
pagepath
form at the top of the page. This shows the page's parent, along with the parent's parent, and so on until the root is reached. This can be especially useful for topical wikis in which subjects may branch off a single super-topic (ie. Bears and Lions branching off of Mammal, which itself branches off of Animal).
Setting parents allows for yet another level of organization you can apply to your site. While
categories
group pages of similar structure/purpose, parenting allows you to develop relational hierarchies within (and across) categories. And, as you might expect, the
ListPages Module
allows you to select pages according to parent-child relationships!
To set a page's parent, you need to find the option in the bottom options bar. If you click on "+ Options", you will see more options pop up, and among them is an option that says "Parent". Clicking on that will bring you to the parent page form. If you succeed in setting the parent, you should see the breadcrumb links appear at the top of the page, such as on this page.
