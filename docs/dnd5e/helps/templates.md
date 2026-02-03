# Templates

<!-- generated-by: scripts/txt_to_mkdocs.py v2026-02-03 -->


help page, you were introduced to the usefulness of categories, especially when working in tandem with the ListPages module. Yet, we can ask an additional question: if pages in a category are meant to be related to one another, then is it possible to automatically force each page to have the same layout? Of course, the answer is yes!
Fold
Unfold
Table of Contents
Live Templates
Static Templates
Data Forms
Live Templates
Wikidot offers support for what are called Live Templates. Live Templates on a per category basis force all pages in a particular category to be formatted the same general way. For example, if you wanted for all pages in the "article" category to have a byline, then live templates will allow you to accomplish that without your users/writers needing to write the byline themselves.
If you recall from the
Using Modules
help page, this is is similar to how you format the results of the ListPages module.
So, let's go ahead and see how we can make a live template with a byline.
In order to access the live template for a category, you must go to the
category
:_template
page. For example, the live template for this "help" category is located at
help:_template
. You can edit this page like any normal wiki page, and every category has its own distinct live template.
For our "article" category, located at
article:_template
, we want to format the page as such:
By AUTHOR
Published DATE

CONTENT
The question is, how do we replace the all-caps words with their respective ideas? Live templates use what are called
page variables
, which are the same as used for the ListPages module. A page variable, like
%%created_by%%
, will be replaced by whoever created the page in question. Therefore, your live template page will have
By %%created_by%%
on the first line, but your individual pages will suddenly have "By Timothy Foster" at the top of the page.
Using page variables, our live template for the "article" category will now look like this:
By %%created_by%%
Published %%created_at%%

%%content%%
Now, if you have a page called
article:first-post
, you will see the following:
Page Source
This is my first post!

**I am excited!**
Result
By Timothy Foster
Published 23 Jul 2014, 10:57
This is my first post!
I am excited!
To find out all the possible page variables you can use, be sure to visit the
Wikidot Documentation
.
Static Templates
Static templates are different from live templates. Live templates will automatically conform page data to a format. Static templates, on the other hand, pre-fill the edit box with code that will achieve a particular format. If you have a template and set it to a category, then every page created in that category will start off with code determined by the template. Since this code resides in the edit box, the user creating the page may, if desired, remove all the code and start off on a clean slate, though merely having the code there encourages otherwise.
Therefore, unlike live templates, page content is
not
automatically conformed to a format. Live templates force a format, whereas static templates merely suggest. Static templates allows for some user customization, which may be desired in some cases.
In order to define a template, you must create a page in the "template" category. You then edit this page like any normal pages, but since the template is static (not live), using page variables (like
%%content%%
) will not do anything. Instead, you would need to somehow alert the user where pieces of information ought to go.
The below represents an example of a static template page,
template:article
:
By AUTHOR
Published DATE

YOUR CONTENT HERE
In order to set a template page to a category, though, you need to access the
Site Manager
. The below represents a step by step process:
From the Dashboard, click on "Appearance & Behavior".
Look for the "Page templates" option.
Select the category for which you want to apply a static template.
Select the static template you want to use.
Click "Save", and you're done!
Templates
This is what it looks like in the Site Manager
Templates
×
This is what it looks like in the Site Manager
Data Forms
Using a live template gives you a good degree of control over a page's format, but it does not give you very much control over the user's page content. Data forms, however, allow you to customize the edit field itself so that users are prompted to input the precise information you want them to. If, for instance, you want your users to input a name, date of birth, and short biography, then using dataforms would be perfect.
Sample Form
This is what a typical form edit field looks like
Data Forms work on a per-category basis, just like live templates. In fact, establishing Data Forms requires the use of the live template page! The start of every data form is always the same; on the live template page, the following code is pasted at the bottom of the edit field:
====
[[form]]
fields:

[[/form]]
After the word "fields:", you specify what kind of edit fields you want to be present. The above image, for example, uses the below code:
fields:
  author:
    type: text
    label: Author
  date:
    type: date
    label: Date
  content:
    type: wiki
    height: 8
    label: Content
In total, there are 11 different field types (ranging from standard text to file attachments), and each type has a variety of options. All these field types and options are specified on the live template page using the format above. This page serves only as an introduction, so to learn more, be sure to visit
Wikidot's Documentation
or ask
the Community
.
In order to use the values that a user places, you can use
form variables
. Form variables work just like page variables. In the above example, if I wanted to use the value inputted into the
author
field, I would use
%%form_data{author}%%
. To use the
content
field, I would use
%%form_data{content}%%
. You can learn more about these on the
documentation
.
